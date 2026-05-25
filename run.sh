#!/usr/bin/env bash
set -e

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "No virtual environment found. Run ./setup.sh first."
    exit 1
fi

echo "Starting YouTubeAI on http://localhost:8000"
echo "Press Ctrl+C to stop."
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
