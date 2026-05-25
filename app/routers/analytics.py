from fastapi import APIRouter, HTTPException

from app.services.youtube import youtube_service
from app.store import video_store

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/youtube")
async def youtube_analytics():
    """Return live YouTube stats for every video that has been posted."""
    videos = video_store.get_all()
    posted = [v for v in videos if v.get("youtube_url")]

    if not posted:
        return []

    if not youtube_service.is_connected():
        raise HTTPException(status_code=400, detail="YouTube not connected")

    results = []
    for video in posted:
        try:
            stats = youtube_service.get_video_stats(video["youtube_url"])
            results.append({
                "video_id": video["id"],
                "prompt": video.get("prompt", ""),
                "local_created_at": video.get("created_at", ""),
                **stats,
            })
        except Exception as e:
            # Include the entry but flag the error so the UI can show it
            results.append({
                "video_id": video["id"],
                "prompt": video.get("prompt", ""),
                "local_created_at": video.get("created_at", ""),
                "youtube_url": video.get("youtube_url", ""),
                "error": str(e),
            })

    return results


@router.get("/youtube/{video_id}")
async def youtube_analytics_single(video_id: str):
    """Refresh stats for one video by its local store ID."""
    video = video_store.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not video.get("youtube_url"):
        raise HTTPException(status_code=400, detail="Video has not been posted to YouTube")
    if not youtube_service.is_connected():
        raise HTTPException(status_code=400, detail="YouTube not connected")

    try:
        stats = youtube_service.get_video_stats(video["youtube_url"])
        return {
            "video_id": video["id"],
            "prompt": video.get("prompt", ""),
            "local_created_at": video.get("created_at", ""),
            **stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
