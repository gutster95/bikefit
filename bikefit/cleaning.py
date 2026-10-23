"""Repairs typical markerless tracking errors before smoothing.

Side views confuse the near and far leg when they cross, and the foot is
often hidden behind crank and chainring. Both show up as short jumps that a
real limb cannot make.
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import median_filter

LEG = ("knee", "ankle", "heel", "toe")
# Allowed sudden deviation of a rigid segment from its local median length.
SEGMENT_TOLERANCE = 0.08


def fix_leg_swaps(near: dict, far: dict) -> int:
    """Swaps near/far leg joints in frames where the swapped assignment
    continues the previous frame's near leg better. Edits arrays in place,
    returns the number of swapped frames."""
    swapped = 0
    prev = None
    for i in range(len(near["knee"])):
        cur = np.array([near[j][i] for j in LEG])
        alt = np.array([far[j][i] for j in LEG])
        if prev is not None and not np.isnan(cur).any() and not np.isnan(alt).any():
            keep = np.linalg.norm(cur - prev, axis=1).sum()
            swap = np.linalg.norm(alt - prev, axis=1).sum()
            if swap < 0.5 * keep:
                for j in LEG:
                    near[j][i], far[j][i] = far[j][i].copy(), near[j][i].copy()
                cur = alt
                swapped += 1
        if not np.isnan(cur).any():
            prev = cur
    return swapped


def reject_jumps(points: dict, fps: float, scale_px: float) -> int:
    """Marks samples far off a running median as missing. scale_px is a body
    length (thigh) that sets the tolerance independent of image size."""
    win = max(3, int(round(0.15 * fps)) | 1)
    limit = 0.2 * scale_px
    rejected = 0
    for a in points.values():
        ok = ~np.isnan(a[:, 0])
        if ok.sum() < win:
            continue
        ref = a.copy()
        for c in range(2):
            ref[ok, c] = median_filter(a[ok, c], size=win, mode="nearest")
        bad = ok & (np.linalg.norm(a - ref, axis=1) > limit)
        a[bad] = np.nan
        rejected += int(bad.sum())
    return rejected


def reject_bad_segments(points: dict, fps: float) -> int:
    """Thigh and shank are rigid, so their length may only change slowly
    (perspective and skin movement shift it by a few percent over a pedal
    stroke). A sudden change against the local median is a tracking error:
    the responsible joint is removed."""
    win = max(3, int(round(0.3 * fps)) | 1)

    def sudden_change(a, b):
        length = np.linalg.norm(points[a] - points[b], axis=1)
        ok = ~np.isnan(length)
        local = np.full_like(length, np.nan)
        local[ok] = median_filter(length[ok], size=win, mode="nearest")
        with np.errstate(invalid="ignore"):
            return np.abs(length / local - 1) > SEGMENT_TOLERANCE

    t_bad, s_bad = sudden_change("hip", "knee"), sudden_change("knee", "ankle")
    knee_bad = t_bad  # hip is the most stable point, so a bad thigh means a bad knee
    ankle_bad = s_bad & ~t_bad
    points["knee"][knee_bad] = np.nan
    for j in ("ankle", "heel", "toe"):
        points[j][ankle_bad] = np.nan
    return int(knee_bad.sum() + ankle_bad.sum())
