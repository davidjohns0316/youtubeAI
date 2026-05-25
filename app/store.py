import json
from pathlib import Path
from threading import Lock


class VideoStore:
    def __init__(self, path: Path = Path("videos/videos.json")):
        self.path = path
        self._lock = Lock()
        self._ensure_file()

    def _ensure_file(self):
        self.path.parent.mkdir(exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]")

    def _read(self) -> list:
        return json.loads(self.path.read_text())

    def _write(self, data: list):
        self.path.write_text(json.dumps(data, indent=2))

    def get_all(self) -> list:
        with self._lock:
            return self._read()

    def get(self, video_id: str) -> dict | None:
        return next((v for v in self.get_all() if v["id"] == video_id), None)

    def add(self, video: dict):
        with self._lock:
            videos = self._read()
            videos.insert(0, video)
            self._write(videos)

    def update(self, video_id: str, updates: dict):
        with self._lock:
            videos = self._read()
            for v in videos:
                if v["id"] == video_id:
                    v.update(updates)
                    break
            self._write(videos)

    def delete(self, video_id: str):
        with self._lock:
            videos = [v for v in self._read() if v["id"] != video_id]
            self._write(videos)


video_store = VideoStore()
