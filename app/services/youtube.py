import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app.config import settings

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]
SECRETS_FILE = settings.credentials_dir / "youtube_client_secrets.json"
TOKEN_FILE = settings.credentials_dir / "youtube_token.json"
STATE_FILE = settings.credentials_dir / "youtube_oauth_state.txt"


class YouTubeService:
    @property
    def _redirect_uri(self) -> str:
        return f"{settings.app_base_url}/api/auth/youtube/callback"

    def get_auth_url(self) -> str:
        if not SECRETS_FILE.exists():
            raise FileNotFoundError(
                "credentials/youtube_client_secrets.json not found. "
                "Download it from Google Cloud Console and place it there."
            )
        flow = Flow.from_client_secrets_file(
            str(SECRETS_FILE),
            scopes=SCOPES,
            redirect_uri=self._redirect_uri,
        )
        auth_url, state = flow.authorization_url(prompt="consent", access_type="offline")
        STATE_FILE.write_text(state)
        return auth_url

    def handle_callback(self, code: str) -> None:
        flow = Flow.from_client_secrets_file(
            str(SECRETS_FILE),
            scopes=SCOPES,
            redirect_uri=self._redirect_uri,
        )
        flow.fetch_token(code=code)
        creds = flow.credentials
        token_data = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": list(creds.scopes) if creds.scopes else SCOPES,
        }
        TOKEN_FILE.write_text(json.dumps(token_data, indent=2))

    def is_connected(self) -> bool:
        return TOKEN_FILE.exists()

    def _get_credentials(self) -> Credentials:
        if not TOKEN_FILE.exists():
            raise ValueError("YouTube not connected. Authenticate in Settings first.")
        data = json.loads(TOKEN_FILE.read_text())
        return Credentials(
            token=data["token"],
            refresh_token=data.get("refresh_token"),
            token_uri=data["token_uri"],
            client_id=data["client_id"],
            client_secret=data["client_secret"],
            scopes=data["scopes"],
        )

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list[str],
        privacy: str = "public",
        category_id: str = "22",
    ) -> str:
        creds = self._get_credentials()
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": {"privacyStatus": privacy},
        }
        media = MediaFileUpload(
            video_path,
            chunksize=50 * 1024 * 1024,
            resumable=True,
            mimetype="video/mp4",
        )
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            _, response = request.next_chunk()

        return f"https://www.youtube.com/watch?v={response['id']}"

    def disconnect(self):
        TOKEN_FILE.unlink(missing_ok=True)
        STATE_FILE.unlink(missing_ok=True)


youtube_service = YouTubeService()
