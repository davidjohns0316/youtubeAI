import base64
import struct
import zlib
from pathlib import Path

import httpx

from app.config import settings

RUNWAY_BASE = "https://api.dev.runwayml.com/v1"
RUNWAY_VERSION = "2024-11-06"

# Runway ratio → (width, height) for placeholder image
RATIO_SIZES = {
    "1280:768": (1280, 768),
    "768:1280": (768, 1280),
    "1024:1024": (1024, 1024),
}


def _make_placeholder_png(width: int, height: int) -> bytes:
    """Solid dark-gray PNG used when no reference image is supplied.
    Runway's image_to_video endpoint requires promptImage — this satisfies
    the requirement while letting promptText drive the actual content."""
    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    row = b"\x00" + bytes([18, 18, 26] * width)   # dark blue-gray, one row
    raw = row * height
    idat = chunk(b"IDAT", zlib.compress(raw, 1))
    iend = chunk(b"IEND", b"")
    return b"\x89PNG\r\n\x1a\n" + ihdr + idat + iend


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
        }
        if seed is not None:
            payload["seed"] = seed

        if image_path:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            ext = Path(image_path).suffix.lower().lstrip(".")
            mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                        "png": "image/png", "webp": "image/webp"}
            mime = mime_map.get(ext, "image/jpeg")
            payload["promptImage"] = f"data:{mime};base64,{img_b64}"
        else:
            # Runway's image_to_video requires promptImage — use a neutral
            # placeholder so the text prompt drives all the content.
            w, h = RATIO_SIZES.get(ratio, (1280, 768))
            png_bytes = _make_placeholder_png(w, h)
            b64 = base64.b64encode(png_bytes).decode()
            payload["promptImage"] = f"data:image/png;base64,{b64}"

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{RUNWAY_BASE}/image_to_video",
                headers=self._headers(),
                json=payload,
            )
            if not resp.is_success:
                # Surface the actual Runway error message
                try:
                    detail = resp.json()
                except Exception:
                    detail = resp.text
                raise Exception(f"Runway {resp.status_code}: {detail}")
            return resp.json()

    async def get_task(self, task_id: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{RUNWAY_BASE}/tasks/{task_id}",
                headers=self._headers(),
            )
            if not resp.is_success:
                try:
                    detail = resp.json()
                except Exception:
                    detail = resp.text
                raise Exception(f"Runway {resp.status_code}: {detail}")
            return resp.json()

    async def download_video(self, url: str, save_path: Path) -> None:
        async with httpx.AsyncClient(timeout=300, follow_redirects=True) as client:
            async with client.stream("GET", url) as resp:
                resp.raise_for_status()
                with open(save_path, "wb") as f:
                    async for chunk in resp.aiter_bytes(8192):
                        f.write(chunk)


runway_service = RunwayService()
