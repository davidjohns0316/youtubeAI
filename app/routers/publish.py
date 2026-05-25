from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.services.tiktok import tiktok_service
from app.services.youtube import youtube_service
from app.store import video_store

router = APIRouter(prefix="/api/publish", tags=["publish"])


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
    video_path = str(settings.videos_dir / video["filename"])

    # ── Force YouTube Shorts classification ──────────────────────────
    # Ensure #Shorts is in the title (YouTube uses this as the primary signal)
    title = req.title
    if "#Shorts" not in title and "#shorts" not in title:
        title = f"{title} #Shorts"

    # Ensure #Shorts is in description too (belt-and-suspenders)
    description = req.description
    if "#Shorts" not in description and "#shorts" not in description:
        description = f"{description}\n\n#Shorts".strip()

    # Add shorts to tags list
    tags = list(req.tags)
    if "Shorts" not in tags and "shorts" not in tags:
        tags = ["Shorts", "YouTubeShorts"] + tags

    try:
        yt_url = youtube_service.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy=req.privacy,
            category_id=req.category_id,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"YouTube upload failed: {e}")

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
