"""Joint angles, crank-cycle detection and per-cycle fit metrics."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import find_peaks

from .i18n import AnalysisError
from .tracks import Track


def included_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    """Angle ABC in degrees for arrays of points, shape (N, 2)."""
    v1, v2 = a - b, c - b
    cos = np.sum(v1 * v2, axis=1) / (np.linalg.norm(v1, axis=1) * np.linalg.norm(v2, axis=1))
    return np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))


def frame_angles(t: Track) -> dict[str, np.ndarray]:
    p = t.points
    torso = p["shoulder"] - p["hip"]
    return {
        # flexion: 0 deg = straight leg
        "knee_flexion": 180.0 - included_angle(p["hip"], p["knee"], p["ankle"]),
        # included angle torso / thigh
        "hip_angle": included_angle(p["shoulder"], p["hip"], p["knee"]),
        # included angle shank / foot
        "ankle_angle": included_angle(p["knee"], p["ankle"], p["toe"]),
        # included angle torso / upper arm
        "shoulder_angle": included_angle(p["hip"], p["shoulder"], p["elbow"]),
        "elbow_flexion": 180.0 - included_angle(p["shoulder"], p["elbow"], p["wrist"]),
        # torso to horizontal; image y points down
        "torso_angle": np.degrees(np.arctan2(-torso[:, 1], np.abs(torso[:, 0]))),
    }


def fit_circle(pts: np.ndarray) -> tuple[np.ndarray, float, float]:
    """Algebraic least-squares circle fit. Returns center, radius, rms error."""
    x, y = pts[:, 0], pts[:, 1]
    A = np.column_stack([x, y, np.ones_like(x)])
    sol, *_ = np.linalg.lstsq(A, x**2 + y**2, rcond=None)
    cx, cy = sol[0] / 2, sol[1] / 2
    r = np.sqrt(sol[2] + cx**2 + cy**2)
    rms = float(np.sqrt(np.mean((np.hypot(x - cx, y - cy) - r) ** 2)))
    return np.array([cx, cy]), float(r), rms


def estimate_period(signal: np.ndarray, fps: float, rpm_range=(40, 140)) -> float:
    """Pedalling period in frames from the autocorrelation of the signal."""
    s = signal - np.mean(signal)
    ac = np.correlate(s, s, mode="full")[len(s) - 1:]
    lo = int(fps * 60 / rpm_range[1])
    hi = min(int(fps * 60 / rpm_range[0]), len(ac) - 1)
    if hi <= lo:
        raise AnalysisError("error.too_short")
    return float(lo + np.argmax(ac[lo:hi]))


@dataclass
class Crank:
    center: np.ndarray  # bottom bracket estimate, px
    radius_px: float
    fit_rms_px: float
    mm_per_px: float | None  # known when the crank length was given


def estimate_crank(t: Track, crank_length_mm: float | None) -> Crank:
    center, r, rms = fit_circle(t.points["pedal"])
    scale = crank_length_mm / r if crank_length_mm else None
    return Crank(center=center, radius_px=r, fit_rms_px=rms, mm_per_px=scale)


def detect_cycles(knee_flexion: np.ndarray, fps: float) -> list[tuple[int, int]]:
    """Cycles run from one knee-extension point (leg most straight, near
    bottom dead center) to the next."""
    period = estimate_period(knee_flexion, fps)
    minima, _ = find_peaks(-knee_flexion, distance=max(1, int(0.6 * period)),
                           prominence=5.0)
    return [(int(a), int(b)) for a, b in zip(minima[:-1], minima[1:])
            if 0.6 * period < b - a < 1.5 * period]


def cycle_metrics(t: Track, angles: dict, crank: Crank, cycles) -> list[dict]:
    p = t.points
    scale = crank.mm_per_px
    rows = []
    for a, b in cycles:
        sl = slice(a, b)
        knee = angles["knee_flexion"][sl]
        ankle = angles["ankle_angle"][sl]
        row = {
            "start": a, "end": b,
            "cadence_rpm": 60.0 * t.fps / (b - a),
            "knee_extension": float(knee.min()),
            "knee_flexion_max": float(knee.max()),
            "hip_closed": float(angles["hip_angle"][sl].min()),
            "ankle_range": float(ankle.max() - ankle.min()),
            "ankle_at_extension": float(angles["ankle_angle"][a]),
            "torso_angle": float(np.median(angles["torso_angle"][sl])),
            "shoulder_angle": float(np.median(angles["shoulder_angle"][sl])),
            "elbow_flexion": float(np.median(angles["elbow_flexion"][sl])),
            "hip_rock_px": float(np.ptp(p["hip"][sl, 1])),
        }
        # Crank at 3 o'clock: pedal straight ahead of the bottom bracket.
        vec = p["pedal"][sl] - crank.center
        ang = np.arctan2(vec[:, 1], vec[:, 0] * t.facing)
        i3 = a + int(np.argmin(np.abs(ang)))
        kops_px = (p["knee"][i3, 0] - p["pedal"][i3, 0]) * t.facing
        row["kops_px"] = float(kops_px)
        if scale:
            row["kops_mm"] = float(kops_px * scale)
            row["hip_rock_mm"] = row["hip_rock_px"] * scale
        rows.append(row)
    return rows


def crank_center_drift(t: Track, cycles) -> float:
    """Largest distance between per-cycle pedal-circle centers. A steady
    camera keeps the bottom bracket in place; pans or zooms move it."""
    centers = [fit_circle(t.points["pedal"][a:b])[0] for a, b in cycles]
    if len(centers) < 2:
        return 0.0
    c = np.array(centers)
    return float(np.max(np.linalg.norm(c - np.median(c, axis=0), axis=1)))


def segment_lengths(t: Track) -> dict[str, float]:
    p = t.points
    return {
        "thigh_px": float(np.median(np.linalg.norm(p["hip"] - p["knee"], axis=1))),
        "shank_px": float(np.median(np.linalg.norm(p["knee"] - p["ankle"], axis=1))),
        "arm_px": float(np.median(np.linalg.norm(p["shoulder"] - p["wrist"], axis=1))),
    }


def summarize(rows: list[dict]) -> dict[str, dict]:
    keys = [k for k in rows[0] if k not in ("start", "end")]
    out = {}
    for k in keys:
        v = np.array([r[k] for r in rows if k in r])
        out[k] = {"median": float(np.median(v)), "std": float(np.std(v)),
                  "min": float(v.min()), "max": float(v.max())}
    return out
