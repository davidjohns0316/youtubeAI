import base64
import hashlib
import json
import secrets
from pathlib import Path
from urllib.parse import parse_qs, urlparse

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
VERIFIER_FILE = settings.credentials_dir / "youtube_code_verifier.txt"


def _make_pkce() -> tuple[str, str]:
    """Return (code_verifier, code_challenge) for S256 PKCE."""
    verifier = secrets.token_urlsafe(64)          # 86-char URL-safe string
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


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

        verifier, challenge = _make_pkce()
        VERIFIER_FILE.write_text(verifier)          # persist for callback

        flow = Flow.from_client_secrets_file(
            str(SECRETS_FILE),
            scopes=SCOPES,
            redirect_uri=self._redirect_uri,
        )
        auth_url, state = flow.authorization_url(
            prompt="consent",
            access_type="offline",
            code_challenge=challenge,
            code_challenge_method="S256",
        )
        STATE_FILE.write_text(state)
        return auth_url

    def handle_callback(self, code: str) -> None:
        # Load the verifier that was saved during get_auth_url()
        if not VERIFIER_FILE.exists():
            raise RuntimeError("OAuth session expired — please try connecting again.")
        verifier = VERIFIER_FILE.read_text().strip()
        VERIFIER_FILE.unlink(missing_ok=True)       # single-use

        flow = Flow.from_client_secrets_file(
            str(SECRETS_FILE),
            scopes=SCOPES,
            redirect_uri=self._redirect_uri,
        )
        flow.fetch_token(code=code, code_verifier=verifier)
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

    def get_video_stats(self, youtube_url: str) -> dict:
        """Fetch live stats for a posted video via YouTube Data API v3."""
        # Extract video ID from URL
        parsed = urlparse(youtube_url)
        yt_id = parse_qs(parsed.query).get("v", [None])[0]
        if not yt_id:
            raise ValueError(f"Could not extract YouTube video ID from: {youtube_url}")

        creds = self._get_credentials()
        youtube = build("youtube", "v3", credentials=creds)
        resp = youtube.videos().list(
            part="statistics,snippet",
            id=yt_id,
        ).execute()

        items = resp.get("items", [])
        if not items:
            raise ValueError(f"Video {yt_id} not found on YouTube")

        item = items[0]
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        thumbnails = snippet.get("thumbnails", {})
        thumb = (thumbnails.get("medium") or thumbnails.get("default") or {}).get("url", "")

        return {
            "youtube_id": yt_id,
            "youtube_url": youtube_url,
            "title": snippet.get("title", ""),
            "published_at": snippet.get("publishedAt", ""),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "thumbnail": thumb,
        }

    def disconnect(self):
        TOKEN_FILE.unlink(missing_ok=True)
        STATE_FILE.unlink(missing_ok=True)
        VERIFIER_FILE.unlink(missing_ok=True)


youtube_service = YouTubeService()
