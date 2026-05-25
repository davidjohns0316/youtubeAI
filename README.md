# YouTubeAI — AI Video Studio

A local web app that generates AI videos with **Runway ML Gen-3** and publishes them directly to **YouTube** and **TikTok**.

## Features

- **AI video generation** — text prompt or image-to-video via Runway Gen-3 Alpha Turbo
- **YouTube publishing** — full OAuth2 integration, privacy control, categories & tags
- **TikTok publishing** — Content Posting API with PKCE OAuth2
- **Video library** — browse, preview, and manage all generated videos
- **Local-first** — everything runs on your machine, no cloud dependencies

## Quick Start

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd youtubeAI
chmod +x setup.sh run.sh
./setup.sh

# 2. Add your Runway API key to .env
echo "RUNWAY_API_KEY=your_key_here" >> .env

# 3. Run
./run.sh
# Open http://localhost:8000
```

## API Setup

### Runway ML (Required)

1. Sign in at [app.runwayml.com](https://app.runwayml.com)
2. Go to **Settings → API Keys** → create a new key
3. Add to `.env`:
   ```
   RUNWAY_API_KEY=your_key_here
   ```

### YouTube (Optional)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → enable **YouTube Data API v3**
3. Create **OAuth 2.0 credentials** → Web application type
4. Add authorized redirect URI:
   ```
   http://localhost:8000/api/auth/youtube/callback
   ```
5. Download the credentials JSON → save as `credentials/youtube_client_secrets.json`
6. Open the app → Settings → **Connect YouTube**

### TikTok (Optional)

> ⚠️ TikTok API access requires business account approval and can take several weeks.

1. Apply at [developers.tiktok.com](https://developers.tiktok.com)
2. Create an app → request `video.upload` and `video.publish` scopes
3. Add redirect URI: `http://localhost:8000/api/auth/tiktok/callback`
4. Add to `.env`:
   ```
   TIKTOK_CLIENT_KEY=your_client_key
   TIKTOK_CLIENT_SECRET=your_client_secret
   ```
5. Open the app → Settings → **Connect TikTok**

## Project Structure

```
youtubeAI/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings from .env
│   ├── store.py             # JSON-based video metadata store
│   ├── routers/
│   │   ├── auth.py          # OAuth routes (YouTube + TikTok)
│   │   ├── generate.py      # Video generation + polling
│   │   └── publish.py       # Publishing endpoints
│   └── services/
│       ├── runway.py        # Runway ML API client
│       ├── youtube.py       # YouTube Data API v3
│       └── tiktok.py        # TikTok Content Posting API
├── frontend/
│   ├── index.html           # Single-page UI
│   ├── style.css            # Dark theme styles
│   └── app.js               # Vanilla JS app logic
├── credentials/             # OAuth tokens + secrets (gitignored)
├── videos/                  # Generated video files (gitignored)
├── .env                     # Your API keys (gitignored)
├── .env.example             # Template
├── requirements.txt
├── setup.sh
└── run.sh
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate` | Start video generation |
| GET | `/api/tasks/{video_id}` | Poll generation status |
| GET | `/api/videos` | List all videos |
| GET | `/api/videos/{filename}` | Stream a video file |
| DELETE | `/api/videos/{video_id}` | Delete a video |
| POST | `/api/publish/youtube` | Upload to YouTube |
| POST | `/api/publish/tiktok` | Upload to TikTok |
| GET | `/api/auth/youtube` | Start YouTube OAuth |
| GET | `/api/auth/tiktok` | Start TikTok OAuth |
| GET | `/api/auth/youtube/status` | YouTube connection status |
| GET | `/api/auth/tiktok/status` | TikTok connection status |

## Notes

- Videos are stored in `videos/` — delete them manually to free disk space
- Runway Gen-3 Alpha Turbo takes 1–3 minutes per video
- YouTube uploads are resumable and support files of any size
- The TikTok uploader submits videos for review; they may take a few minutes to appear publicly
