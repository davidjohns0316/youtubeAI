import asyncio
import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import auth, compose, generate, publish

app = FastAPI(title="YouTubeAI", version="1.0.0", description="AI video generation and publishing")

app.include_router(auth.router)
app.include_router(compose.router)
app.include_router(generate.router)
app.include_router(publish.router)

frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/restart")
async def restart_server():
    """Re-exec the uvicorn process in place — re-reads .env and all credentials."""
    async def _restart():
        await asyncio.sleep(0.4)   # let the response reach the browser first
        os.execv(sys.argv[0], sys.argv)
    asyncio.create_task(_restart())
    return {"status": "restarting"}
