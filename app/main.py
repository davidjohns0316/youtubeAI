from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import auth, generate, publish

app = FastAPI(title="YouTubeAI", version="1.0.0", description="AI video generation and publishing")

app.include_router(auth.router)
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
