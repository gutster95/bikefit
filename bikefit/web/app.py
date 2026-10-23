"""Local web app: guided bike fit in the browser.

Start with `python -m bikefit web`; everything runs on this computer.
"""
from __future__ import annotations

import queue
import shutil
import threading
import traceback
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .. import targets
from ..profile import Bike
from ..video import analyze_file
from .brands import BRANDS
from .geometry import presets
from .store import Store

STATIC = Path(__file__).parent / "static"
SETTING_FIELDS = ("sattelhoehe_mm", "sattelversatz_mm", "vorbau_mm", "spacer_mm")


class Analyzer:
    """One background worker: pose detection uses all CPU cores, so videos
    are analysed one after another."""

    def __init__(self, store: Store):
        self.store = store
        self.progress: dict[tuple[str, int], tuple[float, str]] = {}
        self.jobs: queue.Queue = queue.Queue()
        threading.Thread(target=self._run, daemon=True).start()

    def submit(self, sid: str, nr: int):
        self.progress[(sid, nr)] = (0.0, "In der Warteschlange")
        self.jobs.put((sid, nr))

    def _run(self):
        while True:
            sid, nr = self.jobs.get()
            self._analyze(sid, nr)

    def _analyze(self, sid: str, nr: int):
        store = self.store
        session = store.session(sid)
        rnd = session["runden"][nr - 1]
        folder = store.round_dir(sid, nr)
        store.update_round(sid, nr, status="laeuft")

        def report(fraction, message):
            self.progress[(sid, nr)] = (fraction, message)

        try:
            analyze_file(folder / rnd["video"], folder, crank_mm=None,
                         rider=store.profile_for(session["rad_id"]), progress=report, quiet=True)
            store.update_round(sid, nr, status="fertig", fortschritt=1.0, meldung="Fertig")
        except Exception as e:  # shown to the user, details go to the console
            traceback.print_exc()
            store.update_round(sid, nr, status="fehler", meldung=str(e))
        self.progress.pop((sid, nr), None)


def create_app(data_dir: Path) -> FastAPI:
    store = Store(data_dir)
    analyzer = Analyzer(store)
    app = FastAPI(title="Bikefit")

    # Rounds that were running when the app stopped are started again.
    for s in store.sessions():
        for r in s["runden"]:
            if r["status"] in ("wartet", "laeuft"):
                analyzer.submit(s["id"], r["nr"])

    @app.get("/api/fahrer")
    def get_rider():
        return store.rider()

    @app.put("/api/fahrer")
    def put_rider(data: dict):
        return store.save_rider(data)

    @app.get("/api/marken")
    def brands():
        return BRANDS

    @app.get("/api/modelle")
    def models():
        return presets()

    @app.get("/api/raeder")
    def bikes():
        return store.bikes()

    @app.post("/api/raeder")
    def save_bike(data: dict):
        return store.save_bike(data)

    @app.get("/api/sitzungen")
    def sessions():
        return store.sessions()

    @app.post("/api/sitzungen")
    def new_session(data: dict):
        if not store.bike(data.get("rad_id", "")):
            raise HTTPException(400, "Unbekanntes Rad")
        return store.create_session(data["rad_id"])

    @app.get("/api/sitzungen/{sid}")
    def session(sid: str):
        s = store.session(sid)
        if not s:
            raise HTTPException(404, "Sitzung nicht gefunden")
        for r in s["runden"]:
            if (sid, r["nr"]) in analyzer.progress:
                r["fortschritt"], r["meldung"] = analyzer.progress[(sid, r["nr"])]
            if r["status"] == "fertig":
                r["ergebnis"] = store.result(sid, r["nr"])
        s["rad"] = store.bike(s["rad_id"])
        for r in s["runden"]:
            _add_corrections(r.get("ergebnis"), s["rad"])
        return s

    @app.delete("/api/sitzungen/{sid}")
    def delete_session(sid: str):
        s = store.session(sid)
        if not s:
            raise HTTPException(404, "Sitzung nicht gefunden")
        if any(r["status"] in ("wartet", "laeuft") for r in s["runden"]):
            raise HTTPException(409, "Die Auswertung läuft noch. Bitte warten, bis sie fertig ist.")
        store.delete_session(sid)
        return {"geloescht": sid}

    @app.post("/api/sitzungen/{sid}/runden")
    def new_round(sid: str, video: UploadFile = File(...), aenderung: str = Form(""),
                  sattelhoehe_mm: float | None = Form(None), sattelversatz_mm: float | None = Form(None),
                  vorbau_mm: float | None = Form(None), spacer_mm: float | None = Form(None)):
        s = store.session(sid)
        if not s:
            raise HTTPException(404, "Sitzung nicht gefunden")
        # settings the rider changed since the last round go into the bike profile
        store.update_bike_settings(s["rad_id"], dict(zip(SETTING_FIELDS, (
            sattelhoehe_mm, sattelversatz_mm, vorbau_mm, spacer_mm))))
        nr = len(s["runden"]) + 1
        folder = store.round_dir(sid, nr)
        folder.mkdir(parents=True, exist_ok=True)
        name = "original" + (Path(video.filename or "").suffix.lower() or ".mp4")
        with open(folder / name, "wb") as f:
            shutil.copyfileobj(video.file, f, length=4 * 1024 * 1024)
        rnd = store.add_round(sid, name, aenderung)
        analyzer.submit(sid, rnd["nr"])
        return rnd

    @app.get("/medien/{sid}/{nr}/analyse.mp4")
    def media(sid: str, nr: int):
        path = store.round_dir(sid, nr) / "analyse.mp4"
        if not path.exists():
            raise HTTPException(404)
        return FileResponse(path, media_type="video/mp4")

    @app.get("/")
    def index():
        return FileResponse(STATIC / "index.html")

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app


def _add_corrections(res: dict | None, bike: dict | None) -> None:
    """Results stored before per-metric corrections existed get them on read."""
    if not res or all("korrektur" in e for e in res.get("evaluation", [])):
        return
    scale = res.get("mm_per_px")
    segments = {k: v / scale for k, v in (res.get("segments_mm") or {}).items()} if scale else {}
    tt = any(e["key"] == "torso_angle" and e["hi"] <= 30 for e in res["evaluation"])
    targets.corrections(res["evaluation"], res.get("summary", {}), segments, scale,
                        Bike.from_dict(bike) if bike else None, tt=tt)
