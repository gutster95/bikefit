"""Analysis pipeline: track -> metrics -> result.

The stored result holds numbers and message keys only. localize() turns it
into text in the requested language, so a result can be shown in German or
English and always uses the current advice rules.
"""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from . import metrics, targets
from .i18n import AnalysisError, DEFAULT_LANG, render, t
from .profile import Bike, Profile, Rider, adjusted_targets, plausibility
from .tracks import Track

RESULT_VERSION = 2


@dataclass
class Result:
    track: Track
    angles: dict
    crank: metrics.Crank
    cycles: list
    rows: list
    summary: dict
    segments: dict
    targets: dict
    profile: str  # road | tt
    warnings: list  # i18n messages
    rider: Profile


def analyze_track(track: Track, crank_length_mm: float | None, profile: str | None = None,
                  rider: Profile | None = None) -> Result:
    """profile: target set name; defaults to the bike type in the rider
    profile. crank_length_mm defaults to the profile's crank length."""
    rider = rider or Profile()
    profile = profile or rider.bike.type
    crank_length_mm = crank_length_mm or rider.bike.crank_mm
    target_set = adjusted_targets(targets.PROFILES[profile], rider.rider)
    angles = metrics.frame_angles(track)
    crank = metrics.estimate_crank(track, crank_length_mm)
    cycles = metrics.detect_cycles(angles["knee_flexion"], track.fps)
    if len(cycles) < 3:
        raise AnalysisError("error.few_cycles", cycles=len(cycles))
    rows = metrics.cycle_metrics(track, angles, crank, cycles)
    summary = metrics.summarize(rows)
    segments = metrics.segment_lengths(track)
    warnings = []

    def warn(key, **params):
        warnings.append({"key": key, "params": params})

    if track.coverage < 0.9:
        warn("warn.coverage", coverage=track.coverage)
    if crank.fit_rms_px > 0.15 * crank.radius_px:
        warn("warn.crank_fit")
    if summary["knee_extension"]["std"] > 4:
        warn("warn.knee_std")
    if summary["elbow_flexion"]["std"] > 8:
        warn("warn.elbow_std")
    if len(cycles) < 15:
        warn("warn.few_cycles", cycles=len(cycles))
    if crank.mm_per_px:
        thigh = segments["thigh_px"] * crank.mm_per_px
        if not 300 <= thigh <= 600:
            warn("warn.thigh", thigh=thigh)
    if metrics.crank_center_drift(track, cycles) > 0.15 * crank.radius_px:
        warn("warn.camera_moved")
    return Result(track, angles, crank, cycles, rows, summary, segments, target_set, profile, warnings, rider)


def result_data(res: Result) -> dict:
    """Language-neutral result as stored in result.json."""
    return {
        "version": RESULT_VERSION,
        "side": res.track.side, "facing": res.track.facing, "fps": res.track.fps,
        "offset_s": res.track.offset / res.track.fps, "duration_s": len(res.track) / res.track.fps,
        "cycles": len(res.cycles), "cadence_rpm": res.summary["cadence_rpm"]["median"],
        "mm_per_px": res.crank.mm_per_px, "segments_px": res.segments,
        "summary": res.summary, "profile": res.profile,
        "targets": {k: list(v) for k, v in res.targets.items()},
        "warnings": res.warnings, "cleaning": res.track.corrections,
        "rider": asdict(res.rider.rider), "bike": asdict(res.rider.bike),
    }


def localize(data: dict, lang: str = DEFAULT_LANG, bike: Bike | None = None) -> dict:
    """Adds evaluation, recommendations, notes and warnings as text. bike
    overrides the stored bike, e.g. with settings changed since."""
    tset = {k: tuple(v) for k, v in data["targets"].items()}
    summary, segments, scale = data["summary"], data["segments_px"], data["mm_per_px"]
    bike = bike or Bike.from_dict(data.get("bike") or {})
    rider = Profile(rider=Rider.from_dict(data.get("rider") or {}), bike=bike)
    evaluation = targets.evaluate(summary, tset)
    targets.corrections(evaluation, summary, segments, scale, bike, tt=data["profile"] == "tt", lang=lang)
    for row in evaluation:
        row["label"] = t(f"metric.{row['key']}", lang)
    seg_mm = ({"thigh": segments["thigh_px"] * scale, "shank": segments["shank_px"] * scale} if scale else None)
    notes = plausibility(rider, seg_mm, lang)
    c = data.get("cleaning") or {}
    if sum(c.values()):
        notes.append(t("note.cleaned", lang, leg_swaps=c.get("leg_swaps", 0), jumps=c.get("jumps", 0),
                       bad_segments=c.get("bad_segments", 0)))
    return {**data, "lang": lang, "evaluation": evaluation,
            "recommendations": targets.recommend(summary, segments, scale, tset, bike, lang),
            "done": targets.is_done(summary, segments, scale, tset),
            "notes": notes, "warnings": [render(w, lang) for w in data["warnings"]]}


def report_text(data: dict, lang: str = DEFAULT_LANG) -> str:
    r = localize(data, lang)
    s = r["summary"]
    side = lambda right: t("word.right" if right else "word.left", lang)  # noqa: E731
    lines = [
        t("report.title", lang),
        "=" * 60,
        t("report.side", lang, side=side(r["side"] == "right"), facing=side(r["facing"] > 0)),
        t("report.cycles", lang, cycles=r["cycles"], cadence=r["cadence_rpm"]),
        t("report.window", lang, start=r["offset_s"], end=r["offset_s"] + r["duration_s"]),
    ]
    if r["mm_per_px"]:
        lines.append(t("report.scale", lang, scale=r["mm_per_px"], thigh=r["segments_px"]["thigh_px"] * r["mm_per_px"],
                       shank=r["segments_px"]["shank_px"] * r["mm_per_px"]))
    lines += ["", f"{t('report.header', lang):<42}{t('report.value', lang):>9}{'±':>6}   {t('report.target', lang):<12}", "-" * 80]
    for e in r["evaluation"]:
        lines.append(f"{e['label']:<42}{e['value']:>8.1f}{e['unit']:<1}{e['std']:>5.1f}   "
                     f"{e['lo']:.0f}–{e['hi']:.0f} {e['unit']:<5}{t('status.' + e['status'], lang)}")
    info = t("report.info_only", lang)
    if "kops_mm" in s and not any(e["key"] == "kops_mm" for e in r["evaluation"]):
        lines.append(f"{t('metric.kops_mm', lang) + ' ' + info:<42}{s['kops_mm']['median']:>8.1f}mm")
    if "hip_rock_mm" in s:
        # markerless hip points move with the thigh, so this overstates real hip rocking
        lines.append(f"{t('metric.hip_rock_mm', lang) + ' ' + info:<42}{s['hip_rock_mm']['median']:>8.1f}mm")
    lines += ["", t("report.advice", lang), "-" * 60] + [f"- {tip}" for tip in r["recommendations"]]
    if r["notes"]:
        lines += ["", t("report.notes", lang), "-" * 60] + [f"- {n}" for n in r["notes"]]
    if r["warnings"]:
        lines += ["", t("report.warnings", lang), "-" * 60] + [f"- {w}" for w in r["warnings"]]
    lines += ["", t("report.footer", lang)]
    return "\n".join(lines)


def write_outputs(res: Result, out_dir: Path, lang: str = DEFAULT_LANG) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    data = result_data(res)
    (out_dir / "result.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "report.txt").write_text(report_text(data, lang), encoding="utf-8")
    with open(out_dir / "cycles.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res.rows[0].keys()))
        w.writeheader()
        w.writerows(res.rows)
    with open(out_dir / "frames.csv", "w", newline="") as f:
        w = csv.writer(f)
        joints = list(res.track.points)
        w.writerow(["frame"] + [f"{j}_{c}" for j in joints for c in "xy"] + list(res.angles))
        for i in range(len(res.track)):
            w.writerow([i] + [round(float(res.track.points[j][i, c]), 2) for j in joints for c in (0, 1)]
                       + [round(float(res.angles[k][i]), 2) for k in res.angles])
    return data
