"""File-based storage for the web app: rider, bike garage and fitting sessions.

Everything lives as JSON next to the videos in one data folder, so it can be
read, backed up or deleted by hand.
"""
from __future__ import annotations

import json
import shutil
import threading
import uuid
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from ..profile import Bike, Profile, Rider

_lock = threading.Lock()


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class Store:
    def __init__(self, root: Path):
        self.root = root
        (root / "sessions").mkdir(parents=True, exist_ok=True)

    # -- helpers -------------------------------------------------------------
    def _read(self, path: Path, default):
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def _write(self, path: Path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)

    # -- rider ---------------------------------------------------------------
    def rider(self) -> dict:
        return self._read(self.root / "rider.json", asdict(Rider()))

    def save_rider(self, data: dict) -> dict:
        rider = asdict(Rider.from_dict(data))
        self._write(self.root / "rider.json", rider)
        return rider

    # -- garage --------------------------------------------------------------
    def bikes(self) -> list[dict]:
        return self._read(self.root / "bikes.json", [])

    def bike(self, bike_id: str) -> dict | None:
        return next((b for b in self.bikes() if b["id"] == bike_id), None)

    def save_bike(self, data: dict) -> dict:
        with _lock:
            bikes = self.bikes()
            bike = {"id": data.get("id") or uuid.uuid4().hex[:8], **asdict(Bike.from_dict(data))}
            bikes = [b for b in bikes if b["id"] != bike["id"]] + [bike]
            self._write(self.root / "bikes.json", bikes)
        return bike

    def update_bike_settings(self, bike_id: str, changes: dict):
        """Applies changed settings (e.g. new saddle height) to a bike."""
        bike = self.bike(bike_id)
        if bike:
            bike.update({k: v for k, v in changes.items() if v is not None})
            self.save_bike(bike)

    def profile_for(self, bike_id: str) -> Profile:
        bike = self.bike(bike_id) or {}
        return Profile(rider=Rider.from_dict(self.rider()), bike=Bike.from_dict(bike))

    # -- sessions ------------------------------------------------------------
    def session_dir(self, sid: str) -> Path:
        return self.root / "sessions" / sid

    def session(self, sid: str) -> dict | None:
        return self._read(self.session_dir(sid) / "session.json", None)

    def sessions(self) -> list[dict]:
        out = []
        for d in sorted((self.root / "sessions").iterdir(), reverse=True):
            s = self._read(d / "session.json", None)
            if s:
                out.append(s)
        return out

    def create_session(self, bike_id: str) -> dict:
        sid = datetime.now().strftime("%Y%m%d-%H%M%S")
        s = {"id": sid, "bike_id": bike_id, "created": _now(), "rounds": []}
        self._write(self.session_dir(sid) / "session.json", s)
        return s

    def delete_session(self, sid: str) -> bool:
        """Removes the session folder with its videos and results."""
        folder = self.session_dir(sid)
        if not (folder / "session.json").exists() or folder.parent != self.root / "sessions":
            return False
        shutil.rmtree(folder)
        return True

    def add_round(self, sid: str, video_name: str, change: str, lang: str) -> dict:
        with _lock:
            s = self.session(sid)
            nr = len(s["rounds"]) + 1
            r = {"nr": nr, "created": _now(), "change": change, "video": video_name, "lang": lang,
                 "status": "queued", "progress": 0.0, "message": "progress.queued"}
            s["rounds"].append(r)
            self._write(self.session_dir(sid) / "session.json", s)
        return r

    def update_round(self, sid: str, nr: int, **fields):
        with _lock:
            s = self.session(sid)
            s["rounds"][nr - 1].update(fields)
            self._write(self.session_dir(sid) / "session.json", s)

    def round_dir(self, sid: str, nr: int) -> Path:
        return self.session_dir(sid) / f"round_{nr}"

    def result(self, sid: str, nr: int) -> dict | None:
        return self._read(self.round_dir(sid, nr) / "result.json", None)
