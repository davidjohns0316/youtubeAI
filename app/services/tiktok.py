import hashlib
import json
import secrets
import base64
from pathlib import Path
from urllib.parse import urlencode

import httpx

from app.config import settings

TOKEN_FILE = settings.credentials_dir / "tiktok_token.json"
PKCE_FILE = settings.credentials_dir / "tiktok_pkce.json"

TIKTOK_AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
TIKTOK_VIDEO_INIT_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"


class TikTokService:
    @property
    def _redirect_uri(self) -> str:
        return f"{settings.app_base_url}/api/auth/tiktok/callback"

    def get_auth_url(self) -> str:
        if not settings.tiktok_client_key:
            raise ValueError("TIKTOK_CLIENT_KEY not set in .env")

        code_verifier = secrets.token_urlsafe(64)
        code_challenge = (
            base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
            .rstrip(b"=")
            .decode()
        )
        state = secrets.token_urlsafe(16)

        PKCE_FILE.write_text(json.dumps({"code_verifier": code_verifier, "state": state}))

        params = {
            "client_key": settings.tiktok_client_key,
            "scope": "video.upload,video.publish",
            "response_type": "code",
            "redirect_uri": self._redirect_uri,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        return f"{TIKTOK_AUTH_URL}?{urlencode(params)}"

    async def handle_callback(self, code: str) -> None:
        pkce = json.loads(PKCE_FILE.read_text())
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                TIKTOK_TOKEN_URL,
                data={
                    "client_key": settings.tiktok_client_key,
                    "client_secret": settings.tiktok_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self._redirect_uri,
                    "code_verifier": pkce["code_verifier"],
                },
            )
            resp.raise_for_status()
            TOKEN_FILE.write_text(json.dumps(resp.json(), indent=2))
        PKCE_FILE.unlink(missing_ok=True)

    def is_connected(self) -> bool:
        return TOKEN_FILE.exists()

    def _get_token(self) -> str:
        if not TOKEN_FILE.exists():
            raise ValueError("TikTok not connected. Authenticate in Settings first.")
        return json.loads(TOKEN_FILE.read_text()).get("access_token", "")

    async def upload_video(
        self,
        video_path: str,
        title: str,
        hashtags: list[str],
        privacy: str = "PUBLIC_TO_EVERYONE",
    ) -> str:
        token = self._get_token()
        file_size = Path(video_path).stat().st_size

        caption = title
        if hashtags:
            caption += " " + " ".join(f"#{h.lstrip('#')}" for h in hashtags)

        async with httpx.AsyncClient(timeout=300) as client:
            init_resp = await client.post(
                TIKTOK_VIDEO_INIT_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json; charset=UTF-8",
                },
                json={
                    "post_info": {
                        "title": caption[:2200],
                        "privacy_level": privacy,
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                    },
                    "source_info": {
                        "source": "FILE_UPLOAD",
                        "video_size": file_size,
                        "chunk_size": file_size,
                        "total_chunk_count": 1,
                    },
                },
            )
            init_resp.raise_for_status()
            data = init_resp.json()["data"]
            publish_id = data["publish_id"]
            upload_url = data["upload_url"]

            with open(video_path, "rb") as f:
                video_bytes = f.read()

            upload_resp = await client.put(
                upload_url,
                content=video_bytes,
                headers={
                    "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
                    "Content-Length": str(file_size),
                    "Content-Type": "video/mp4",
                },
            )
            upload_resp.raise_for_status()

        return publish_id

    def disconnect(self):
        TOKEN_FILE.unlink(missing_ok=True)
        PKCE_FILE.unlink(missing_ok=True)


tiktok_service = TikTokService()
