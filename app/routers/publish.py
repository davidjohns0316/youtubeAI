import asyncio
import shutil
import subprocess
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.services.tiktok import tiktok_service
from app.services.youtube import youtube_service
from app.store import video_store

router = APIRouter(prefix="/api/publish", tags=["publish"])

SHORTS_W, SHORTS_H = 1080, 1920   # 9:16 portrait


class YouTubePublishRequest(BaseModel):
    video_id: str
    title: str
    description: str = ""
    tags: List[str] = []
    privacy: str = "public"
    category_id: str = "22"


class TikTokPublishRequest(BaseModel):
    video_id: str
    title: str
    hashtags: List[str] = []
    privacy: str = "PUBLIC_TO_EVERYONE"


def _ffmpeg() -> str:
    return shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"

def _ffprobe() -> str:
    return shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"


def _get_dimensions(video_path: str) -> tuple[int, int]:
    """Return (width, height) of video, or (0, 0) on error."""
    result = subprocess.run(
        [_ffprobe(), "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=s=x:p=0", video_path],
        capture_output=True, text=True,
    )
    try:
        w, h = result.stdout.strip().split("x")
        return int(w), int(h)
    except Exception:
        return 0, 0


def _convert_to_shorts(input_path: str, output_path: str) -> bool:
    """
    Re-encode video to 1080×1920 (9:16 portrait) for YouTube Shorts.
    Scales to fit, pads with black bars if needed (e.g. landscape input).
    """
    result = subprocess.run(
        [
            _ffmpeg(),
            "-i", input_path,
            "-vf",
            f"scale={SHORTS_W}:{SHORTS_H}:force_original_aspect_ratio=decrease,"
            f"pad={SHORTS_W}:{SHORTS_H}:(ow-iw)/2:(oh-ih)/2:black,"
            f"setsar=1",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-c:a", "copy",
            "-movflags", "+faststart",
            "-y", output_path,
        ],
        capture_output=True,
    )
    return result.returncode == 0


def _get_ready_video(video_id: str) -> dict:
    video = video_store.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if video["status"] != "completed" or not video.get("filename"):
        raise HTTPException(status_code=400, detail="Video is not ready for publishing")
    return video


@router.post("/youtube")
async def publish_to_youtube(req: YouTubePublishRequest):
    if not youtube_service.is_connected():
        raise HTTPException(status_code=401, detail="YouTube not connected. Go to Settings to authenticate.")

    video = _get_ready_video(req.video_id)
    original_path = str(settings.videos_dir / video["filename"])
    upload_path = original_path
    temp_file: Path | None = None

    # ── Ensure 9:16 portrait dimensions for Shorts ───────────────────
    w, h = await asyncio.to_thread(_get_dimensions, original_path)
    is_portrait_916 = (h > w) and (w > 0)

    if not is_portrait_916:
        # Convert to 1080×1920 before uploading
        tmp = settings.videos_dir / f"{video['id']}_shorts_upload.mp4"
        ok = await asyncio.to_thread(_convert_to_shorts, original_path, str(tmp))
        if ok:
            upload_path = str(tmp)
            temp_file = tmp

    # ── Force #Shorts metadata ────────────────────────────────────────
    title = req.title
    if "#Shorts" not in title and "#shorts" not in title:
        title = f"{title} #Shorts"

    description = req.description  # intentionally blank per user preference

    tags = list(req.tags)
    if "Shorts" not in tags and "shorts" not in tags:
        tags = ["Shorts", "YouTubeShorts"] + tags

    try:
        yt_url = await asyncio.to_thread(
            youtube_service.upload_video,
            upload_path, title, description, tags, req.privacy, req.category_id,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"YouTube upload failed: {e}")
    finally:
        if temp_file:
            temp_file.unlink(missing_ok=True)

    video_store.update(req.video_id, {"youtube_url": yt_url})
    return {"url": yt_url}


@router.post("/tiktok")
async def publish_to_tiktok(req: TikTokPublishRequest):
    if not tiktok_service.is_connected():
        raise HTTPException(status_code=401, detail="TikTok not connected. Go to Settings to authenticate.")

    video = _get_ready_video(req.video_id)
    video_path = str(settings.videos_dir / video["filename"])

    try:
        publish_id = await tiktok_service.upload_video(
            video_path=video_path,
            title=req.title,
            hashtags=req.hashtags,
            privacy=req.privacy,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TikTok upload failed: {e}")

    video_store.update(req.video_id, {"tiktok_publish_id": publish_id})
    return {"publish_id": publish_id, "status": "submitted"}
