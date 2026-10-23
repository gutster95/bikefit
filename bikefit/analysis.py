"""Analysis pipeline: track -> metrics -> report."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from . import metrics, targets
from .profile import Profile, adjusted_targets, plausibility
from .tracks import Track

SIDE_DE = {"left": "links", "right": "rechts"}


@dataclass
class Result:
    track: Track
    angles: dict
    crank: metrics.Crank
    cycles: list
    rows: list
    summary: dict
    segments: dict
    evaluation: list
    tips: list
    warnings: list
    notes: list
    targets: dict
    done: bool  # nothing left to change


def analyze_track(track: Track, crank_length_mm: float | None, profile: str | None = None,
                  rider: Profile | None = None) -> Result:
    """profile: target set name; defaults to the bike type in the rider
    profile. crank_length_mm defaults to the profile's crank length."""
    rider = rider or Profile()
    profile = profile or rider.rad.typ
    crank_length_mm = crank_length_mm or rider.rad.kurbel_mm
    target_set = adjusted_targets(targets.PROFILES[profile], rider.fahrer)
    angles = metrics.frame_angles(track)
    crank = metrics.estimate_crank(track, crank_length_mm)
    cycles = metrics.detect_cycles(angles["knee_flexion"], track.fps)
    if len(cycles) < 3:
        raise ValueError(f"Nur {len(cycles)} Kurbelumdrehungen erkannt. "
                         "Bitte mindestens 30 Sekunden gleichmäßig treten und filmen.")
    rows = metrics.cycle_metrics(track, angles, crank, cycles)
    summary = metrics.summarize(rows)
    segments = metrics.segment_lengths(track)
    warnings = []
    if track.coverage < 0.9:
        warnings.append(f"Person nur in {track.coverage:.0%} der Bilder erkannt (Licht, Kleidung, Bildausschnitt prüfen).")
    if crank.fit_rms_px > 0.15 * crank.radius_px:
        warnings.append("Pedalkreis unsauber erkannt, mm-Werte und KOPS sind unsicher.")
    if summary["knee_extension"]["std"] > 4:
        warnings.append("Kniewinkel schwankt stark zwischen den Umdrehungen (Tracking-Rauschen oder unruhiges Treten).")
    if summary["elbow_flexion"]["std"] > 8:
        warnings.append("Armwinkel schwanken stark (Hände bewegt oder Griffposition gewechselt). Arm-Werte mit Vorsicht lesen.")
    if len(cycles) < 15:
        warnings.append(f"Nur {len(cycles)} Umdrehungen. Für belastbare Werte mindestens 30 Sekunden aufnehmen.")
    if crank.mm_per_px:
        thigh = segments["thigh_px"] * crank.mm_per_px
        if not 300 <= thigh <= 600:
            warnings.append(f"Oberschenkellänge {thigh:.0f} mm wirkt unplausibel, Maßstab prüfen.")
    drift = metrics.crank_center_drift(track, cycles)
    if drift > 0.15 * crank.radius_px:
        warnings.append("Das Bild bewegt sich (Kamera geschwenkt oder gezoomt?). Kamera muss fest stehen, "
                        "sonst sind Pedalkreis, mm-Werte und Hüftbewegung falsch.")
    evaluation = targets.evaluate(summary, target_set)
    tips = targets.recommend(summary, segments, crank.mm_per_px, target_set, rider.rad)
    seg_mm = ({"thigh": segments["thigh_px"] * crank.mm_per_px, "shank": segments["shank_px"] * crank.mm_per_px}
              if crank.mm_per_px else None)
    notes = plausibility(rider, seg_mm)
    fixed = sum(track.corrections.values())
    if fixed:
        c = track.corrections
        notes.append(f"Automatisch korrigiert: {c.get('beine_vertauscht', 0)} Bilder mit vertauschten Beinen, "
                     f"{c.get('spruenge', 0)} Sprünge, {c.get('segmentlaenge', 0)} unplausible Segmentlängen.")
    done = tips == [targets.ALL_GOOD]
    return Result(track, angles, crank, cycles, rows, summary, segments, evaluation, tips, warnings,
                  notes, target_set, done)


def report_text(res: Result) -> str:
    t = res.track
    s = res.summary
    lines = [
        "BIKEFIT ANALYSE",
        "=" * 60,
        f"Analysierte Körperseite: {SIDE_DE[t.side]}   Blickrichtung im Bild: {'rechts' if t.facing > 0 else 'links'}",
        f"Kurbelumdrehungen: {len(res.cycles)}   Trittfrequenz: {s['cadence_rpm']['median']:.0f} U/min",
        f"Ausgewertet: Sekunde {t.offset / t.fps:.1f} bis {(t.offset + len(t)) / t.fps:.1f} des Videos",
    ]
    if res.crank.mm_per_px:
        lines.append(f"Maßstab aus Kurbellänge: {res.crank.mm_per_px:.2f} mm pro Pixel   "
                     f"Oberschenkel {res.segments['thigh_px'] * res.crank.mm_per_px:.0f} mm, "
                     f"Unterschenkel {res.segments['shank_px'] * res.crank.mm_per_px:.0f} mm")
    lines += ["", f"{'Messwert':<38}{'Wert':>9}{'±':>6}   {'Ziel':<12}Status", "-" * 76]
    for e in res.evaluation:
        lines.append(f"{e['label']:<38}{e['value']:>8.1f}{e['unit']:<1}{e['std']:>5.1f}   "
                     f"{e['lo']:.0f}–{e['hi']:.0f} {e['unit']:<5}{e['status']}")
    if "kops_mm" in s and not any(e["key"] == "kops_mm" for e in res.evaluation):
        lines.append(f"{'Knie vor Pedalachse bei 3 Uhr (nur Info)':<38}{s['kops_mm']['median']:>8.1f}mm")
    if "hip_rock_mm" in s:
        # markerless hip points move with the thigh, so this overstates real hip rocking
        lines.append(f"{'Hüftbewegung vertikal (nur Info)':<38}{s['hip_rock_mm']['median']:>8.1f}mm")
    lines += ["", "EMPFEHLUNG", "-" * 60] + [f"- {tip}" for tip in res.tips]
    if res.notes:
        lines += ["", "INFO", "-" * 60] + [f"- {n}" for n in res.notes]
    if res.warnings:
        lines += ["", "HINWEISE ZUR MESSQUALITÄT", "-" * 60] + [f"- {w}" for w in res.warnings]
    lines += ["", "Werte sind Mediane über alle Umdrehungen, ± ist die Streuung.",
              "Die Software ersetzt keine medizinische Beratung."]
    return "\n".join(lines)


def write_outputs(res: Result, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "bericht.txt").write_text(report_text(res), encoding="utf-8")
    with open(out_dir / "umdrehungen.csv", "w", newline="") as f:
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
    data = {
        "side": res.track.side, "fps": res.track.fps, "cycles": len(res.cycles),
        "mm_per_px": res.crank.mm_per_px, "summary": res.summary, "evaluation": res.evaluation,
        "recommendations": res.tips, "warnings": res.warnings, "notes": res.notes,
        "done": res.done, "offset_s": res.track.offset / res.track.fps,
        "cadence_rpm": res.summary["cadence_rpm"]["median"],
        "segments_mm": ({k: v * res.crank.mm_per_px for k, v in res.segments.items()}
                        if res.crank.mm_per_px else None),
    }
    (out_dir / "ergebnis.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
