import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config import settings
from app.services.runway import runway_service
from app.store import video_store

router = APIRouter(prefix="/api", tags=["generate"])


@router.post("/generate")
async def generate_video(
    prompt: str = Form(...),
    duration: int = Form(5),
    ratio: str = Form("1280:768"),
    seed: int = Form(None),
    image: UploadFile = File(None),
):
    if not settings.runway_api_key:
        raise HTTPException(status_code=400, detail="RUNWAY_API_KEY not set in .env")

    video_id = str(uuid.uuid4())
    image_path: str | None = None

    if image and image.filename:
        suffix = Path(image.filename).suffix or ".jpg"
        tmp_path = settings.videos_dir / f"{video_id}_ref{suffix}"
        with open(tmp_path, "wb") as f:
            f.write(await image.read())
        image_path = str(tmp_path)

    try:
        task = await runway_service.generate(
            prompt=prompt,
            image_path=image_path,
            duration=duration,
            ratio=ratio,
            seed=seed,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Runway API error: {e}")

    task_id = task.get("id") or task.get("task_id", "")

    video_store.add(
        {
            "id": video_id,
            "runway_task_id": task_id,
            "prompt": prompt,
            "duration": duration,
            "ratio": ratio,
            "status": "generating",
            "progress": 0,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "filename": None,
            "youtube_url": None,
            "tiktok_publish_id": None,
        }
    )

    return {"video_id": video_id, "task_id": task_id, "status": "generating"}


@router.get("/tasks/{video_id}")
async def poll_task(video_id: str):
    video = video_store.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video["status"] in ("completed", "failed"):
        return video

    task_id = video.get("runway_task_id")
    if not task_id:
        raise HTTPException(status_code=400, detail="No Runway task ID")

    try:
        task = await runway_service.get_task(task_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    status = (task.get("status") or "").upper()

    if status == "SUCCEEDED":
        output = task.get("output") or []
        if output:
            save_path = settings.videos_dir / f"{video_id}.mp4"
            try:
                await runway_service.download_video(output[0], save_path)
                video_store.update(video_id, {"status": "completed", "filename": f"{video_id}.mp4", "progress": 1})
            except Exception as e:
                video_store.update(video_id, {"status": "failed", "error": str(e)})
        else:
            video_store.update(video_id, {"status": "failed", "error": "No output URL from Runway"})
    elif status in ("FAILED", "CANCELLED"):
        video_store.update(video_id, {"status": "failed"})
    else:
        progress = task.get("progressRatio") or task.get("progress") or 0
        video_store.update(video_id, {"progress": float(progress)})

    return video_store.get(video_id)


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

    if video.get("filename"):
        (settings.videos_dir / video["filename"]).unlink(missing_ok=True)

    for ref in settings.videos_dir.glob(f"{video_id}_ref.*"):
        ref.unlink(missing_ok=True)

    video_store.delete(video_id)
    return {"status": "deleted"}
