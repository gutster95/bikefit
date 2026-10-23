"""One-time migration of data written by the first, German-named version
(profil.json, daten/, ergebnisse/) to the English names. Runs at start-up
and does nothing once the old files are gone."""
from __future__ import annotations

import json
import re
import traceback
from pathlib import Path

RIDER_KEYS = {"groesse_cm": "height_cm", "schrittlaenge_cm": "inseam_cm", "beweglichkeit": "flexibility",
              "ziel": "goal", "beschwerden": "complaints"}
BIKE_KEYS = {"typ": "type", "marke": "brand", "modell": "model", "rahmengroesse": "frame_size",
             "sitzwinkel_grad": "seat_angle_deg", "kurbel_mm": "crank_mm", "sattelhoehe_mm": "saddle_height_mm",
             "sattelversatz_mm": "saddle_setback_mm", "vorbau_mm": "stem_mm",
             "vorbau_winkel_grad": "stem_angle_deg"}
VALUES = {
    "flexibility": {"gering": "low", "mittel": "medium", "gut": "high"},
    "goal": {"komfort": "comfort", "rennen": "race"},
    "type": {"rennrad": "road", "zeitfahren": "tt"},
}
COMPLAINTS = {"knie_vorne": "knee_front", "knie_hinten": "knee_back", "ruecken": "lower_back", "nacken": "neck",
              "taube_haende": "numb_hands", "taube_fuesse": "numb_feet", "sitzbeschwerden": "saddle_pain"}
STATUS = {"wartet": "queued", "laeuft": "running", "fertig": "done", "fehler": "error"}
FILES = {"analyse.mp4": "analysis.mp4", "bericht.txt": "report.txt", "umdrehungen.csv": "cycles.csv"}


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _rename_keys(d: dict, keys: dict) -> dict:
    out = {keys.get(k, k): v for k, v in d.items()}
    for field, mapping in VALUES.items():
        if field in out:
            out[field] = mapping.get(out[field], out[field])
    if "complaints" in out:
        out["complaints"] = [COMPLAINTS.get(c, c) for c in out["complaints"]]
    return out


def rider(d: dict) -> dict:
    return _rename_keys(d, RIDER_KEYS)


def bike(d: dict) -> dict:
    return _rename_keys(d, BIKE_KEYS)


def result(old: dict, rider_data: dict, bike_data: dict) -> dict:
    """Old ergebnis.json (texts in German) to the language-neutral result."""
    scale = old.get("mm_per_px")
    rows = old.get("evaluation", [])
    cleaning = {}
    for note in old.get("notes", []):
        m = re.search(r"(\d+) Bilder mit vertauschten Beinen, (\d+) Sprünge, (\d+)", note)
        if m:
            cleaning = dict(zip(("leg_swaps", "jumps", "bad_segments"), map(int, m.groups())))
    return {
        "version": 2, "side": old.get("side", "left"), "facing": old.get("facing", 1), "fps": old.get("fps", 30),
        "offset_s": old.get("offset_s", 0), "duration_s": old.get("duration_s", 0),
        "cycles": old.get("cycles", 0), "cadence_rpm": old.get("cadence_rpm", 0), "mm_per_px": scale,
        "segments_px": {k: v / scale for k, v in (old.get("segments_mm") or {}).items()} if scale else {},
        "summary": old["summary"],
        "profile": "tt" if any(r["key"] == "torso_angle" and r["hi"] <= 30 for r in rows) else "road",
        "targets": {r["key"]: [r["lo"], r["hi"], r["unit"]] for r in rows},
        "warnings": [{"text": w} for w in old.get("warnings", [])],  # German only, kept as written
        "cleaning": cleaning, "rider": rider_data, "bike": bike_data,
    }


def _migrate_data(old_dir: Path, new_dir: Path):
    old_dir.rename(new_dir)
    rider_data = {}
    if (new_dir / "fahrer.json").exists():
        rider_data = rider(_read(new_dir / "fahrer.json"))
        _write(new_dir / "rider.json", rider_data)
        (new_dir / "fahrer.json").unlink()
    bikes = []
    if (new_dir / "raeder.json").exists():
        bikes = [bike(b) for b in _read(new_dir / "raeder.json")]
        _write(new_dir / "bikes.json", bikes)
        (new_dir / "raeder.json").unlink()
    sessions = new_dir / "sitzungen"
    if not sessions.exists():
        return
    sessions = sessions.rename(new_dir / "sessions")
    for folder in sessions.iterdir():
        meta = folder / "sitzung.json"
        if not meta.exists():
            continue
        s = _read(meta)
        bike_data = next((b for b in bikes if b.get("id") == s.get("rad_id")), {})
        rounds = []
        for r in s.get("runden", []):
            status = STATUS.get(r.get("status"), r.get("status"))
            new_round = {"nr": r["nr"], "created": r.get("erstellt"), "change": r.get("aenderung", ""),
                         "video": r.get("video"), "lang": "de", "status": status,
                         "progress": r.get("fortschritt", 0.0), "message": "progress.done"}
            if status == "error":
                new_round["error"] = {"text": r.get("meldung", "")}
            elif status in ("queued", "running"):
                new_round.update(status="queued", message="progress.queued")
            rounds.append(new_round)
            rdir = folder / f"runde_{r['nr']}"
            if rdir.exists():
                rdir = rdir.rename(folder / f"round_{r['nr']}")
                for old_name, new_name in FILES.items():
                    if (rdir / old_name).exists():
                        (rdir / old_name).rename(rdir / new_name)
                if (rdir / "ergebnis.json").exists():
                    _write(rdir / "result.json", result(_read(rdir / "ergebnis.json"), rider_data, bike_data))
                    (rdir / "ergebnis.json").unlink()
        _write(folder / "session.json", {"id": s["id"], "bike_id": s.get("rad_id"),
                                         "created": s.get("erstellt"), "rounds": rounds})
        meta.unlink()


def migrate_project(root: Path):
    try:
        if (root / "profil.json").exists() and not (root / "profile.json").exists():
            old = _read(root / "profil.json")
            _write(root / "profile.json", {"rider": rider(old.get("fahrer", {})), "bike": bike(old.get("rad", {}))})
            (root / "profil.json").unlink()
        if (root / "daten").exists() and not (root / "data").exists():
            _migrate_data(root / "daten", root / "data")
            print("Data moved from daten/ to data/.")
        if (root / "ergebnisse").exists() and not (root / "results").exists():
            (root / "ergebnisse").rename(root / "results")
    except Exception:  # never block the start; the old files stay where they are
        traceback.print_exc()
        print("Could not migrate old data automatically.")
