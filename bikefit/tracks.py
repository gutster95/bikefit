"""Turns raw per-frame detections into clean, smoothed joint trajectories."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.signal import butter, filtfilt

from . import cleaning
from .i18n import AnalysisError
from .pose import JOINTS

MIN_VISIBILITY = 0.3
# The pedal spindle sits under the ball of the foot, roughly 70 % of the way
# from heel to toe tip.
FOOT_PEDAL_RATIO = 0.7


@dataclass
class Track:
    """Trajectories of one body side, pixel coordinates, shape (N, 2) each."""
    fps: float
    side: str
    facing: int  # +1 = rider faces right in the image, -1 = faces left
    points: dict[str, np.ndarray] = field(default_factory=dict)
    coverage: float = 1.0  # share of frames with a usable detection
    corrections: dict = field(default_factory=dict)  # repaired samples per kind
    offset: int = 0  # index of the first used frame in the video

    def __len__(self):
        return len(next(iter(self.points.values())))


def choose_side(raw: list) -> str:
    """The side closer to the camera has the smaller MediaPipe depth (z)."""
    z = {"left": [], "right": []}
    for det in raw:
        if det is None:
            continue
        for side in z:
            z[side].append(np.mean([det[side][j][2] for j in ("hip", "knee", "ankle")]))
    if not z["left"]:
        raise AnalysisError("error.no_person")
    return "left" if np.median(z["left"]) < np.median(z["right"]) else "right"


def raw_arrays(raw: list, side: str) -> dict[str, np.ndarray]:
    """(N, 2) arrays with NaN where the joint was missing or barely visible."""
    n = len(raw)
    out = {j: np.full((n, 2), np.nan) for j in JOINTS}
    for i, det in enumerate(raw):
        if det is None:
            continue
        for j in JOINTS:
            x, y, _, vis = det[side][j]
            if vis >= MIN_VISIBILITY:
                out[j][i] = (x, y)
    return out


def fill_gaps(a: np.ndarray) -> np.ndarray:
    a = a.copy()
    idx = np.arange(len(a))
    for c in range(a.shape[1]):
        ok = ~np.isnan(a[:, c])
        if ok.sum() >= 2:
            a[:, c] = np.interp(idx, idx[ok], a[ok, c])
    return a


def lowpass(a: np.ndarray, fps: float, cutoff_hz: float = 10.0) -> np.ndarray:
    """Zero-phase Butterworth filter. 10 Hz keeps the pedalling harmonics
    (90 rpm = 1.5 Hz) and removes frame-to-frame jitter."""
    cutoff = min(cutoff_hz, 0.4 * fps)
    b, a_ = butter(2, cutoff / (fps / 2))
    if len(a) <= 3 * max(len(a_), len(b)):
        return a
    return filtfilt(b, a_, a, axis=0)


def riding_segment(raw: list, side: str, fps: float) -> tuple[int, int]:
    """Longest stretch where the rider sits on the bike: the hip stays near
    its usual position. Cuts getting on/off and walking to the camera."""
    a = raw_arrays(raw, side)
    hip = a["hip"]
    thigh = np.nanmedian(np.linalg.norm(hip - a["knee"], axis=1))
    center = np.nanmedian(hip, axis=0)
    for _ in range(2):  # re-center on the seated frames
        dist = np.linalg.norm(hip - center, axis=1)
        seated = dist < 0.35 * thigh
        if seated.sum() == 0:
            return 0, len(raw)
        center = np.median(hip[seated], axis=0)
    # bridge short dropouts, then take the longest run
    gap = int(0.5 * fps)
    runs, start, last = [], None, None
    for i in np.flatnonzero(seated):
        if start is None:
            start = i
        elif i - last > gap:
            runs.append((start, last + 1))
            start = i
        last = i
    runs.append((start, last + 1))
    a0, b0 = max(runs, key=lambda r: r[1] - r[0])
    margin = int(1.0 * fps)  # skip the first and last second of the stretch
    if b0 - a0 > 4 * margin:
        a0, b0 = a0 + margin, b0 - margin
    return int(a0), int(b0)


def build_track(raw: list, fps: float, side: str = "auto", smooth: bool = True,
                clean: bool = True, trim: bool = True) -> Track:
    if side == "auto":
        side = choose_side(raw)
    offset = 0
    if trim:
        offset, end = riding_segment(raw, side, fps)
        raw = raw[offset:end]
    arrays = raw_arrays(raw, side)
    coverage = float(np.mean(~np.isnan(arrays["knee"][:, 0])))
    corrections = {}
    if clean:
        far = raw_arrays(raw, "right" if side == "left" else "left")
        corrections["leg_swaps"] = cleaning.fix_leg_swaps(arrays, far)
        thigh = float(np.nanmedian(np.linalg.norm(arrays["hip"] - arrays["knee"], axis=1)))
        corrections["jumps"] = cleaning.reject_jumps(arrays, fps, thigh)
        corrections["bad_segments"] = cleaning.reject_bad_segments(arrays, fps)
    points = {}
    for j, a in arrays.items():
        a = fill_gaps(a)
        points[j] = lowpass(a, fps) if smooth and not np.isnan(a).any() else a
    points["pedal"] = points["heel"] + FOOT_PEDAL_RATIO * (points["toe"] - points["heel"])
    facing = 1 if np.nanmedian(points["wrist"][:, 0] - points["hip"][:, 0]) > 0 else -1
    return Track(fps=fps, side=side, facing=facing, points=points, coverage=coverage,
                 corrections=corrections, offset=offset)
