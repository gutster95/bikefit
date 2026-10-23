"""Draws skeleton, crank circle and angles onto video frames."""
from __future__ import annotations

import cv2
import numpy as np

BONES = [("shoulder", "elbow"), ("elbow", "wrist"), ("shoulder", "hip"),
         ("hip", "knee"), ("knee", "ankle"), ("ankle", "heel"),
         ("heel", "toe"), ("ankle", "toe")]
GREEN, RED, WHITE, YELLOW = (80, 200, 80), (60, 60, 230), (255, 255, 255), (0, 210, 255)


def _pt(p):
    return int(round(p[0])), int(round(p[1]))


def draw_skeleton(frame, pts: dict, thickness: int = 3):
    for a, b in BONES:
        if a in pts and b in pts and not np.isnan(pts[a]).any() and not np.isnan(pts[b]).any():
            cv2.line(frame, _pt(pts[a]), _pt(pts[b]), WHITE, thickness, cv2.LINE_AA)
    for name, p in pts.items():
        if not np.isnan(p).any():
            color = YELLOW if name == "pedal" else GREEN
            cv2.circle(frame, _pt(p), thickness + 3, color, -1, cv2.LINE_AA)


def draw_crank(frame, center, radius):
    cv2.circle(frame, _pt(center), int(radius), YELLOW, 1, cv2.LINE_AA)
    cv2.drawMarker(frame, _pt(center), YELLOW, cv2.MARKER_CROSS, 16, 2)


def draw_text_panel(frame, lines: list[tuple[str, bool | None]], origin=(20, 40)):
    """lines: (text, ok) where ok=True green, False red, None white."""
    scale = max(0.5, frame.shape[0] / 1400)
    step = int(34 * scale / 0.75)
    width = int(max((len(t) for t, _ in lines), default=0) * 15 * scale) + 20
    x, y = origin
    overlay = frame.copy()
    cv2.rectangle(overlay, (x - 10, y - step), (x + width, y + step * (len(lines) - 1) + 12), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    for i, (text, ok) in enumerate(lines):
        color = WHITE if ok is None else (GREEN if ok else RED)
        cv2.putText(frame, text, (x, y + i * step), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2, cv2.LINE_AA)
