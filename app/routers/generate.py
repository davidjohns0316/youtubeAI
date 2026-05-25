import asyncio
import math
import shutil
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import httpx
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config import settings
from app.services.runway import runway_service
from app.store import video_store

router = APIRouter(prefix="/api", tags=["generate"])

CLIP_DURATION = 10  # Runway Gen-3 max seconds per generation


# ── Helpers ───────────────────────────────────────────────────────────────

def _ffmpeg_bin() -> str:
    return shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg" or "/usr/local/bin/ffmpeg"


def _extract_last_frame(clip_path: Path, frame_path: Path) -> bool:
    """Pull the last frame from a clip for use as the next clip's starting image."""
    result = subprocess.run(
        [_ffmpeg_bin(), "-sseof", "-0.1", "-i", str(clip_path),
         "-frames:v", "1", "-q:v", "2", "-y", str(frame_path)],
        capture_output=True,
    )
    return result.returncode == 0 and frame_path.exists() and frame_path.stat().st_size > 0


def _stitch_clips(clip_paths: list[Path], output_path: Path) -> tuple[bool, str]:
    """Concatenate clips into one video using ffmpeg."""
    if len(clip_paths) == 1:
        clip_paths[0].rename(output_path)
        return True, ""

    filelist = output_path.parent / f"{output_path.stem}_filelist.txt"
    filelist.write_text("\n".join(f"file '{p.resolve()}'" for p in clip_paths))

    result = subprocess.run(
        [_ffmpeg_bin(), "-f", "concat", "-safe", "0", "-i", str(filelist),
         "-c:v", "libx264", "-preset", "fast", "-crf", "22",
         "-movflags", "+faststart", "-y", str(output_path)],
        capture_output=True, text=True,
    )
    filelist.unlink(missing_ok=True)
    return result.returncode == 0, result.stderr[-400:] if result.returncode != 0 else ""


RATIO_DIMS = {"1280:768": (1280, 768), "768:1280": (768, 1280), "1024:1024": (1024, 1024)}


async def _fetch_starting_frame(prompt: str, ratio: str, save_dir: Path) -> str | None:
    """
    Generate a real starting frame from Pollinations.ai (free, no API key).
    This gives Runway actual visual content to animate instead of a blank placeholder.
    Returns the saved image path, or None if it fails (Runway will use its own placeholder).
    """
    w, h = RATIO_DIMS.get(ratio, (1280, 768))
    # Truncate prompt — Pollinations has URL length limits
    short_prompt = prompt[:300]
    url = (
        f"https://image.pollinations.ai/prompt/{quote(short_prompt)}"
        f"?width={w}&height={h}&nologo=true&model=flux&seed=42"
    )
    try:
        async with httpx.AsyncClient(timeout=45, follow_redirects=True) as client:
            resp = await client.get(url)
            if resp.is_success and resp.headers.get("content-type", "").startswith("image/"):
                frame_path = save_dir / f"start_{uuid.uuid4().hex[:8]}.jpg"
                frame_path.write_bytes(resp.content)
                return str(frame_path)
    except Exception:
        pass
    return None


# ── Background task: frame-chained multi-clip generation ─────────────────

async def _generate_clips(
    video_id: str,
    prompt: str,
    image_path: str | None,
    total_duration: int,
    ratio: str,
    seed: int | None,
):
    """
    Generate clips sequentially using frame chaining:
      clip 0 → extract last frame → use as input for clip 1
      clip 1 → extract last frame → use as input for clip 2  ...
    This keeps the scene visually continuous across the entire video.
    """
    num_clips = math.ceil(total_duration / CLIP_DURATION)
    clip_paths: list[Path] = []
    frame_paths: list[Path] = []

    # If no user image supplied, generate a real starting frame from Pollinations.ai
    # so Runway has actual visual content to animate (dark placeholder = black video)
    current_image: str | None = image_path
    if not current_image:
        video_store.update(video_id, {"status_label": "Generating starting frame from prompt..."})
        generated_frame = await _fetch_starting_frame(prompt, ratio, settings.videos_dir)
        if generated_frame:
            current_image = generated_frame
            frame_paths.append(Path(generated_frame))  # track for cleanup

    for i in range(num_clips):
        is_chained = i > 0
        video_store.update(video_id, {
            "clips_done": i,
            "progress": i / num_clips,
            "status_label": (
                f"Generating clip {i + 1} of {num_clips} (continuing from previous scene)..."
                if is_chained
                else f"Generating clip 1 of {num_clips}..."
            ),
        })

        # Start Runway generation for this clip
        try:
            task = await runway_service.generate(
                prompt=prompt,
                image_path=current_image,   # last frame keeps the scene alive
                duration=CLIP_DURATION,
                ratio=ratio,
                seed=seed,                  # same seed = same visual style throughout
            )
        except Exception as e:
            video_store.update(video_id, {"status": "failed", "error": f"Runway error (clip {i + 1}): {e}"})
            return

        task_id = task.get("id", "")

        # Poll until Runway finishes this clip
        while True:
            await asyncio.sleep(6)
            try:
                t = await runway_service.get_task(task_id)
            except Exception:
                continue

            status = (t.get("status") or "").upper()

            if status == "SUCCEEDED":
                output = t.get("output") or []
                if not output:
                    video_store.update(video_id, {"status": "failed", "error": f"No output URL for clip {i + 1}"})
                    return
                clip_path = settings.videos_dir / f"{video_id}_clip{i}.mp4"
                try:
                    await runway_service.download_video(output[0], clip_path)
                except Exception as e:
                    video_store.update(video_id, {"status": "failed", "error": f"Download failed (clip {i + 1}): {e}"})
                    return
                clip_paths.append(clip_path)
                break

            elif status in ("FAILED", "CANCELLED"):
                video_store.update(video_id, {"status": "failed", "error": f"Clip {i + 1} {status.lower()} on Runway"})
                return

        # Extract last frame to chain into the next clip
        if i < num_clips - 1:
            video_store.update(video_id, {
                "status_label": f"Extracting last frame to continue scene for clip {i + 2}...",
            })
            frame_path = settings.videos_dir / f"{video_id}_frame{i}.jpg"
            success = await asyncio.to_thread(_extract_last_frame, clip_paths[-1], frame_path)
            if success:
                current_image = str(frame_path)
                frame_paths.append(frame_path)
            else:
                # Extraction failed — carry forward the same image (still coherent via prompt)
                current_image = image_path

    # ── Stitch all clips into one video ───────────────────────────────────
    video_store.update(video_id, {"status_label": "Stitching clips into final video...", "progress": 0.95})

    final_path = settings.videos_dir / f"{video_id}.mp4"
    ok, err = await asyncio.to_thread(_stitch_clips, clip_paths, final_path)

    # Clean up clips and frame images
    for cp in clip_paths:
        cp.unlink(missing_ok=True)
    for fp in frame_paths:
        fp.unlink(missing_ok=True)

    if not ok:
        video_store.update(video_id, {"status": "failed", "error": f"ffmpeg stitch failed: {err}"})
        return

    video_store.update(video_id, {
        "status": "completed",
        "filename": f"{video_id}.mp4",
        "clips_done": num_clips,
        "clips_total": num_clips,
        "progress": 1.0,
        "status_label": "Complete",
    })


# ── Endpoints ─────────────────────────────────────────────────────────────

@router.post("/generate")
async def generate_video(
    background_tasks: BackgroundTasks,
    prompt: str = Form(...),
    duration: int = Form(5),
    ratio: str = Form("1280:768"),
    seed: int = Form(None),
    image: UploadFile = File(None),
):
    if not settings.runway_api_key:
        raise HTTPException(status_code=400, detail="RUNWAY_API_KEY not set in .env")

    duration = max(5, min(duration, 60))
    video_id = str(uuid.uuid4())
    image_path: str | None = None

    if image and image.filename:
        suffix = Path(image.filename).suffix or ".jpg"
        tmp = settings.videos_dir / f"{video_id}_ref{suffix}"
        with open(tmp, "wb") as f:
            f.write(await image.read())
        image_path = str(tmp)

    num_clips = math.ceil(duration / CLIP_DURATION)

    video_store.add({
        "id": video_id,
        "runway_task_id": None,
        "prompt": prompt,
        "duration": duration,
        "ratio": ratio,
        "status": "generating",
        "status_label": "Starting...",
        "progress": 0,
        "clips_total": num_clips,
        "clips_done": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "filename": None,
        "youtube_url": None,
        "tiktok_publish_id": None,
    })

    background_tasks.add_task(
        _generate_clips, video_id, prompt, image_path, duration, ratio, seed
    )

    return {"video_id": video_id, "status": "generating", "clips_total": num_clips}


@router.get("/tasks/{video_id}")
async def poll_task(video_id: str):
    video = video_store.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/videos")
async def list_videos():
    return video_store.get_all()


@router.get("/videos/{filename}")
async def serve_video(filename: str):
    path = settings.videos_dir / filename
    if not path.exists() or path.suffix not in (".mp4", ".mov", ".webm"):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path, media_type="video/mp4")


@router.delete("/videos/{video_id}")
async def delete_video(video_id: str):
    video = video_store.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    for leftover in settings.videos_dir.glob(f"{video_id}*"):
        leftover.unlink(missing_ok=True)
    video_store.delete(video_id)
    return {"status": "deleted"}
