from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    runway_api_key: str = ""
    anthropic_api_key: str = ""
    elevenlabs_api_key: str = ""

    google_client_id: str = ""
    google_client_secret: str = ""

    tiktok_client_key: str = ""
    tiktok_client_secret: str = ""

    app_base_url: str = "http://localhost:8000"

    videos_dir: Path = Path("videos")
    credentials_dir: Path = Path("credentials")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
settings.videos_dir.mkdir(exist_ok=True)
settings.credentials_dir.mkdir(exist_ok=True)
