#!/usr/bin/env bash
set -e

echo "=== YouTubeAI Setup ==="

# Check Python version
python3 --version || { echo "Python 3 is required. Install it from python.org"; exit 1; }

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and install
source .venv/bin/activate
echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env from .env.example — add your API keys before running."
fi

# Ensure directories exist
mkdir -p videos credentials

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your RUNWAY_API_KEY"
echo "  2. For YouTube: add credentials/youtube_client_secrets.json (see README)"
echo "  3. For TikTok: add TIKTOK_CLIENT_KEY and TIKTOK_CLIENT_SECRET to .env"
echo "  4. Run: ./run.sh"
echo ""
