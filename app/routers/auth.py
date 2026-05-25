from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.config import settings
from app.services.tiktok import tiktok_service
from app.services.youtube import youtube_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── YouTube ──────────────────────────────────────────────────────────────────

@router.get("/youtube")
async def youtube_auth():
    try:
        url = youtube_service.get_auth_url()
        return RedirectResponse(url)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/youtube/callback")
async def youtube_callback(code: str, state: str = ""):
    try:
        youtube_service.handle_callback(code=code)
        return RedirectResponse(f"{settings.app_base_url}/?yt=connected")
    except Exception as e:
        return RedirectResponse(f"{settings.app_base_url}/?yt=error&msg={str(e)[:200]}")


@router.get("/youtube/status")
async def youtube_status():
    return {"connected": youtube_service.is_connected()}


@router.post("/youtube/disconnect")
async def youtube_disconnect():
    youtube_service.disconnect()
    return {"status": "disconnected"}


# ── TikTok ───────────────────────────────────────────────────────────────────

@router.get("/tiktok")
async def tiktok_auth():
    try:
        url = tiktok_service.get_auth_url()
        return RedirectResponse(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tiktok/callback")
async def tiktok_callback(code: str, state: str = ""):
    try:
        await tiktok_service.handle_callback(code=code)
        return RedirectResponse(f"{settings.app_base_url}/?tt=connected")
    except Exception as e:
        return RedirectResponse(f"{settings.app_base_url}/?tt=error&msg={str(e)[:200]}")


@router.get("/tiktok/status")
async def tiktok_status():
    return {"connected": tiktok_service.is_connected()}


@router.post("/tiktok/disconnect")
async def tiktok_disconnect():
    tiktok_service.disconnect()
    return {"status": "disconnected"}
