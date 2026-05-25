import asyncio
import subprocess
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.config import settings
from app.services.news import search_news
from app.services.script import generate_script
from app.store import video_store
from app.services.tts import (
    generate_tts_edge, generate_tts_mac, generate_tts_elevenlabs,
    get_audio_duration, list_voices, EDGE_VOICES, MAC_VOICES, ELEVENLABS_VOICES,
)

router = APIRouter(prefix="/api", tags=["compose"])


def _ffmpeg_bin() -> str:
    return shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"


class ScriptRequest(BaseModel):
    topic: str
    category: str = "Finance"
    duration_seconds: int = 60


class TTSRequest(BaseModel):
    text: str
    voice_key: str = "edge:Aria (US Female) ⭐"


class CombineRequest(BaseModel):
    video_id: str
    audio_filename: str


@router.get("/voices")
async def get_voices():
    return list_voices()


@router.post("/script/generate")
async def generate_script_endpoint(req: ScriptRequest):
    # Search for real news articles on the topic first
    articles = await search_news(req.topic, max_results=5)

    try:
        result = await asyncio.to_thread(
            generate_script, req.topic, req.category, req.duration_seconds, articles
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation failed: {e}")

    sources = [
        {"title": a["title"], "source": a["source"], "url": a["source_url"], "date": a.get("date", "")}
        for a in articles[:3]
    ]
    return {
        "script": result["script"],
        "video_prompt": result["video_prompt"],
        "sources": sources,
        "articles_found": len(articles),
    }


@router.post("/tts/generate")
async def generate_tts_endpoint(req: TTSRequest):
    audio_id = str(uuid.uuid4())
    output_mp3 = settings.videos_dir / f"{audio_id}.mp3"

    if req.voice_key.startswith("edge:"):
        display_name = req.voice_key[5:]
        voice_id = EDGE_VOICES.get(display_name, "en-US-AriaNeural")
        try:
            await generate_tts_edge(req.text, output_mp3, voice_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif req.voice_key.startswith("mac:"):
        display_name = req.voice_key[4:]
        voice_name = MAC_VOICES.get(display_name, "Samantha")
        try:
            await asyncio.to_thread(generate_tts_mac, req.text, output_mp3, voice_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif req.voice_key.startswith("el:"):
        display_name = req.voice_key[3:]
        voice_id = ELEVENLABS_VOICES.get(display_name)
        if not voice_id:
            raise HTTPException(status_code=400, detail=f"Unknown ElevenLabs voice: {display_name}")
        try:
            await generate_tts_elevenlabs(req.text, output_mp3, voice_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="voice_key must start with 'edge:', 'mac:', or 'el:'")

    duration = await asyncio.to_thread(get_audio_duration, output_mp3)
    return {"audio_filename": output_mp3.name, "duration_seconds": duration}


@router.post("/compose/combine")
async def combine_video_audio(req: CombineRequest):
    """Merge a generated video with a TTS audio track using ffmpeg."""
    video_path = settings.videos_dir / f"{req.video_id}.mp4"
    audio_path = settings.videos_dir / req.audio_filename

    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"Video file not found: {req.video_id}.mp4")
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail=f"Audio file not found: {req.audio_filename}")

    combined_id = str(uuid.uuid4())
    output_path = settings.videos_dir / f"{combined_id}.mp4"

    def _merge():
        result = subprocess.run(
            [
                _ffmpeg_bin(),
                "-i", str(video_path),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                "-movflags", "+faststart",
                "-y", str(output_path),
            ],
            capture_output=True, text=True,
        )
        return result.returncode, result.stderr[-600:] if result.returncode != 0 else ""

    returncode, err = await asyncio.to_thread(_merge)
    if returncode != 0:
        raise HTTPException(status_code=500, detail=f"ffmpeg combine failed: {err}")

    # Look up original video metadata to copy prompt etc.
    original = video_store.get(req.video_id) or {}

    # Register the combined video in the store so it shows up in the library
    video_store.add({
        "id": combined_id,
        "prompt": original.get("prompt", "Combined video"),
        "duration": original.get("duration", 0),
        "ratio": original.get("ratio", "1280:768"),
        "status": "completed",
        "status_label": "Complete",
        "progress": 1.0,
        "clips_total": original.get("clips_total", 1),
        "clips_done": original.get("clips_total", 1),
        "filename": f"{combined_id}.mp4",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "youtube_url": None,
        "tiktok_publish_id": None,
        "runway_task_id": None,
        "has_audio": True,
    })

    return {"combined_filename": output_path.name, "video_id": combined_id}


@router.get("/audio/{filename}")
async def serve_audio(filename: str):
    path = settings.videos_dir / filename
    if not path.exists() or path.suffix != ".mp3":
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(path, media_type="audio/mpeg")
