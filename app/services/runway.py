import base64
from pathlib import Path

import httpx

from app.config import settings

RUNWAY_BASE = "https://api.dev.runwayml.com/v1"
RUNWAY_VERSION = "2024-11-06"


class RunwayService:
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {settings.runway_api_key}",
            "X-Runway-Version": RUNWAY_VERSION,
            "Content-Type": "application/json",
        }

    async def generate(
        self,
        prompt: str,
        image_path: str | None = None,
        duration: int = 5,
        ratio: str = "1280:768",
        seed: int | None = None,
    ) -> dict:
        payload: dict = {
            "model": "gen3a_turbo",
            "promptText": prompt,
            "duration": duration,
            "ratio": ratio,
            "watermark": False,
        }
        if seed is not None:
            payload["seed"] = seed

        if image_path:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            ext = Path(image_path).suffix.lower().lstrip(".")
            mime_map = {
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "webp": "image/webp",
            }
            mime = mime_map.get(ext, "image/jpeg")
            payload["promptImage"] = f"data:{mime};base64,{img_b64}"

        # Runway uses /image_to_video for both text-only and image+text
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{RUNWAY_BASE}/image_to_video",
                headers=self._headers(),
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()

    async def get_task(self, task_id: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{RUNWAY_BASE}/tasks/{task_id}",
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()

    async def download_video(self, url: str, save_path: Path) -> None:
        async with httpx.AsyncClient(timeout=300, follow_redirects=True) as client:
            async with client.stream("GET", url) as resp:
                resp.raise_for_status()
                with open(save_path, "wb") as f:
                    async for chunk in resp.aiter_bytes(8192):
                        f.write(chunk)


runway_service = RunwayService()
