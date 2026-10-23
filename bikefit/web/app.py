"""Local web app: guided bike fit in the browser.

Start with `python -m bikefit web`; everything runs on this computer.
Every endpoint that returns text takes ?lang=de|en.
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

from ..analysis import localize
from ..i18n import AnalysisError, lang_or_default, render, t
from ..video import analyze_file
from .brands import BRANDS
from .geometry import presets
from .store import Store

STATIC = Path(__file__).parent / "static"
SETTING_FIELDS = ("saddle_height_mm", "saddle_setback_mm", "stem_mm", "spacer_mm")


class Analyzer:
    """One background worker: pose detection uses all CPU cores, so videos
    are analysed one after another."""

    def __init__(self, store: Store):
        self.store = store
        self.progress: dict[tuple[str, int], tuple[float, str]] = {}  # fraction, message key
        self.jobs: queue.Queue = queue.Queue()
        threading.Thread(target=self._run, daemon=True).start()

    def submit(self, sid: str, nr: int):
        self.progress[(sid, nr)] = (0.0, "progress.queued")
        self.jobs.put((sid, nr))

    def _run(self):
        while True:
            sid, nr = self.jobs.get()
            self._analyze(sid, nr)

    def _analyze(self, sid: str, nr: int):
        store = self.store
        session = store.session(sid)
        if not session:  # deleted while queued
            return
        rnd = session["rounds"][nr - 1]
        folder = store.round_dir(sid, nr)
        store.update_round(sid, nr, status="running", message="progress.running")

        def report(fraction, key):
            self.progress[(sid, nr)] = (fraction, key)

        try:
            analyze_file(folder / rnd["video"], folder, crank_mm=None, rider=store.profile_for(session["bike_id"]),
                         progress=report, quiet=True, lang=rnd.get("lang", "en"))
            store.update_round(sid, nr, status="done", progress=1.0, message="progress.done")
        except AnalysisError as e:
            store.update_round(sid, nr, status="error", error={"key": e.key, "params": e.params})
        except Exception as e:  # details go to the console
            traceback.print_exc()
            store.update_round(sid, nr, status="error", error={"key": "error.unexpected", "params": {"detail": str(e)}})
        self.progress.pop((sid, nr), None)


def create_app(data_dir: Path) -> FastAPI:
    store = Store(data_dir)
    analyzer = Analyzer(store)
    app = FastAPI(title="Bikefit")

    # Rounds that were running when the app stopped are started again.
    for s in store.sessions():
        for r in s["rounds"]:
            if r["status"] in ("queued", "running"):
                analyzer.submit(s["id"], r["nr"])

    def round_view(sid: str, r: dict, lang: str) -> dict:
        r = dict(r)
        if (sid, r["nr"]) in analyzer.progress:
            r["progress"], r["message"] = analyzer.progress[(sid, r["nr"])]
        r["message"] = t(r.get("message") or "progress.queued", lang)
        if r.get("error"):
            r["message"] = render(r["error"], lang)
        if r["status"] == "done":
            data = store.result(sid, r["nr"])
            r["result"] = localize(data, lang) if data else None
        return r

    @app.get("/api/rider")
    def get_rider():
        return store.rider()

    @app.put("/api/rider")
    def put_rider(data: dict):
        return store.save_rider(data)

    @app.get("/api/brands")
    def brands():
        return BRANDS

    @app.get("/api/models")
    def models():
        return presets()

    @app.get("/api/bikes")
    def bikes():
        return store.bikes()

    @app.post("/api/bikes")
    def save_bike(data: dict):
        return store.save_bike(data)

    @app.get("/api/sessions")
    def sessions(lang: str = "en"):
        lang = lang_or_default(lang)
        return [{**s, "rounds": [round_view(s["id"], r, lang) | {"result": None} for r in s["rounds"]]}
                for s in store.sessions()]

    @app.post("/api/sessions")
    def new_session(data: dict, lang: str = "en"):
        if not store.bike(data.get("bike_id", "")):
            raise HTTPException(400, t("api.unknown_bike", lang_or_default(lang)))
        return store.create_session(data["bike_id"])

    @app.get("/api/sessions/{sid}")
    def session(sid: str, lang: str = "en"):
        lang = lang_or_default(lang)
        s = store.session(sid)
        if not s:
            raise HTTPException(404, t("api.no_session", lang))
        return {**s, "rounds": [round_view(sid, r, lang) for r in s["rounds"]], "bike": store.bike(s["bike_id"])}

    @app.delete("/api/sessions/{sid}")
    def delete_session(sid: str, lang: str = "en"):
        lang = lang_or_default(lang)
        s = store.session(sid)
        if not s:
            raise HTTPException(404, t("api.no_session", lang))
        if any(r["status"] in ("queued", "running") for r in s["rounds"]):
            raise HTTPException(409, t("api.still_running", lang))
        store.delete_session(sid)
        return {"deleted": sid}

    @app.post("/api/sessions/{sid}/rounds")
    def new_round(sid: str, video: UploadFile = File(...), change: str = Form(""), lang: str = Form("en"),
                  saddle_height_mm: float | None = Form(None), saddle_setback_mm: float | None = Form(None),
                  stem_mm: float | None = Form(None), spacer_mm: float | None = Form(None)):
        s = store.session(sid)
        if not s:
            raise HTTPException(404, t("api.no_session", lang_or_default(lang)))
        # settings the rider changed since the last round go into the bike profile
        store.update_bike_settings(s["bike_id"], dict(zip(SETTING_FIELDS, (
            saddle_height_mm, saddle_setback_mm, stem_mm, spacer_mm))))
        nr = len(s["rounds"]) + 1
        folder = store.round_dir(sid, nr)
        folder.mkdir(parents=True, exist_ok=True)
        name = "original" + (Path(video.filename or "").suffix.lower() or ".mp4")
        with open(folder / name, "wb") as f:
            shutil.copyfileobj(video.file, f, length=4 * 1024 * 1024)
        rnd = store.add_round(sid, name, change, lang_or_default(lang))
        analyzer.submit(sid, rnd["nr"])
        return rnd

    @app.get("/media/{sid}/{nr}/analysis.mp4")
    def media(sid: str, nr: int):
        path = store.round_dir(sid, nr) / "analysis.mp4"
        if not path.exists():
            raise HTTPException(404)
        return FileResponse(path, media_type="video/mp4")

    @app.get("/")
    def index():
        return FileResponse(STATIC / "index.html")

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app
