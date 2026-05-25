import shutil
import subprocess
from pathlib import Path

import edge_tts
import httpx

from app.config import settings

# Microsoft Edge neural voices — natural, human-sounding, free
EDGE_VOICES = {
    "Aria (US Female) ⭐": "en-US-AriaNeural",
    "Jenny (US Female)": "en-US-JennyNeural",
    "Guy (US Male)": "en-US-GuyNeural",
    "Christopher (US Male)": "en-US-ChristopherNeural",
    "Sonia (British Female)": "en-GB-SoniaNeural",
    "Ryan (British Male)": "en-GB-RyanNeural",
    "Natasha (Australian Female)": "en-AU-NatashaNeural",
    "William (Australian Male)": "en-AU-WilliamNeural",
}

# macOS built-in voices (fallback / no-internet option)
MAC_VOICES = {
    "Samantha (macOS Female)": "Samantha",
    "Alex (macOS Male)": "Alex",
    "Daniel (macOS British)": "Daniel",
}

ELEVENLABS_VOICES = {
    "Rachel (Female)": "21m00Tcm4TlvDq8ikWAM",
    "Adam (Male)": "pNInz6obpgDQGcFmaJgB",
    "Josh (Deep Male)": "TxGEqnHWrfWFTfGW9XjX",
    "Bella (Soft Female)": "EXAVITQu4vr4xnSDxMaL",
    "Antoni (Warm Male)": "ErXwobaYiN019PkySvjV",
}


def _ffmpeg() -> str:
    return shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"


def list_voices() -> dict:
    voices = {}
    voices.update({f"edge:{k}": k for k in EDGE_VOICES})
    voices.update({f"mac:{k}": k for k in MAC_VOICES})
    if settings.elevenlabs_api_key:
        voices.update({f"el:{k}": f"{k} ✨" for k in ELEVENLABS_VOICES})
    return voices


# ── SRT helpers ────────────────────────────────────────────────────────────

def _srt_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _words_to_srt(words: list[dict], words_per_card: int = 5) -> str:
    """
    Group word-boundary events into subtitle cards (N words each) and
    return SRT-formatted text.
    Each word dict: {"word": str, "start": float (sec), "duration": float (sec)}
    """
    if not words:
        return ""

    srt_blocks = []
    idx = 1
    i = 0
    while i < len(words):
        chunk = words[i : i + words_per_card]
        text = " ".join(w["word"] for w in chunk)
        start = chunk[0]["start"]
        end = chunk[-1]["start"] + chunk[-1]["duration"]
        # Tiny gap to avoid overlapping the next card
        end = min(end, start + 3.0)
        srt_blocks.append(
            f"{idx}\n{_srt_timestamp(start)} --> {_srt_timestamp(end)}\n{text}\n"
        )
        idx += 1
        i += words_per_card

    return "\n".join(srt_blocks)


# ── TTS generators ─────────────────────────────────────────────────────────

async def generate_tts_edge(
    text: str,
    output_mp3: Path,
    voice: str = "en-US-AriaNeural",
) -> Path | None:
    """
    Generate TTS using Microsoft Edge neural voices.
    Returns the path to a companion .srt subtitle file (word-accurate timing),
    or None if word boundaries aren't available.
    """
    communicate = edge_tts.Communicate(text, voice)
    word_boundaries: list[dict] = []

    with open(output_mp3, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                word_boundaries.append({
                    "word": chunk["text"],
                    "start": chunk["offset"] / 10_000_000,    # 100-ns units → seconds
                    "duration": chunk["duration"] / 10_000_000,
                })

    if not word_boundaries:
        return None

    srt_content = _words_to_srt(word_boundaries, words_per_card=5)
    srt_path = output_mp3.with_suffix(".srt")
    srt_path.write_text(srt_content, encoding="utf-8")
    return srt_path


def generate_tts_mac(text: str, output_mp3: Path, voice_name: str = "Samantha") -> None:
    """Generate TTS using macOS say command (fallback, no subtitle timing)."""
    aiff = output_mp3.with_suffix(".aiff")
    try:
        subprocess.run(
            ["say", "-v", voice_name, "-r", "160", "-o", str(aiff), text],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"macOS say failed: {e.stderr}")

    result = subprocess.run(
        [_ffmpeg(), "-i", str(aiff), "-c:a", "libmp3lame", "-q:a", "2", "-y", str(output_mp3)],
        capture_output=True,
    )
    aiff.unlink(missing_ok=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg audio conversion failed")


async def generate_tts_elevenlabs(text: str, output_mp3: Path, voice_id: str) -> None:
    """Generate TTS using ElevenLabs API (premium, no subtitle timing)."""
    if not settings.elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY not set in .env")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            url,
            headers={"xi-api-key": settings.elevenlabs_api_key, "Content-Type": "application/json"},
            json={
                "text": text,
                "model_id": "eleven_turbo_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
            },
        )
        if not resp.is_success:
            raise RuntimeError(f"ElevenLabs error {resp.status_code}: {resp.text[:200]}")
        output_mp3.write_bytes(resp.content)


def get_audio_duration(audio_path: Path) -> float:
    """Return audio duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0
