"""Offline analysis of a recorded video file."""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Callable

import cv2
import imageio_ffmpeg
import numpy as np

from .analysis import analyze_track, report_text, write_outputs
from .overlay import draw_crank, draw_skeleton, draw_text_panel
from .pose import PoseDetector
from .tracks import build_track

Progress = Callable[[float, str], None]  # (fraction 0..1, message)
MAX_OUTPUT_WIDTH = 1280


def console_progress(fraction: float, message: str):
    sys.stdout.write(f"\r{message} {fraction:5.0%}")
    sys.stdout.flush()


class H264Writer:
    """Writes browser-playable H.264 through the ffmpeg bundled with
    imageio-ffmpeg (OpenCV's own encoders differ per platform)."""

    def __init__(self, path: Path, fps: float, size: tuple[int, int]):
        self.size = size
        self._gen = imageio_ffmpeg.write_frames(
            str(path), size, fps=fps, codec="libx264", pix_fmt_in="bgr24",
            output_params=["-crf", "23", "-preset", "veryfast", "-movflags", "+faststart"],
            macro_block_size=2)
        self._gen.send(None)

    def write(self, frame: np.ndarray):
        if (frame.shape[1], frame.shape[0]) != self.size:
            frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_AREA)
        self._gen.send(np.ascontiguousarray(frame))

    def release(self):
        self._gen.close()


def detect_video(path: Path, model: str, max_seconds: float | None,
                 progress: Progress = console_progress):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Video nicht lesbar: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    limit = int(max_seconds * fps) if max_seconds else total
    detector = PoseDetector(model)
    raw = []
    while len(raw) < limit:
        ok, frame = cap.read()
        if not ok:
            break
        raw.append(detector.detect(frame, len(raw) * 1000.0 / fps))
        if len(raw) % 15 == 0:
            progress(len(raw) / max(1, min(limit, total)), "Erkenne Körperpunkte")
    detector.close()
    cap.release()
    return raw, fps


def render_video(src: Path, dst: Path, res, progress: Progress = console_progress):
    cap = cv2.VideoCapture(str(src))
    t = res.track
    writer = None
    cycle_of = np.full(len(t), -1)
    for ci, (a, b) in enumerate(res.cycles):
        cycle_of[a:b] = ci
    for _ in range(t.offset):  # read instead of seek: seeking is inexact in phone videos
        cap.grab()
    for i in range(len(t)):
        ok, frame = cap.read()
        if not ok:
            break
        if writer is None:
            h, w = frame.shape[:2]
            scale = min(1.0, MAX_OUTPUT_WIDTH / w)
            writer = H264Writer(dst, t.fps, (int(w * scale) // 2 * 2, int(h * scale) // 2 * 2))
        draw_crank(frame, res.crank.center, res.crank.radius_px)
        draw_skeleton(frame, {k: v[i] for k, v in t.points.items()},
                      thickness=max(2, frame.shape[0] // 400))
        lines = [(f"Knie {res.angles['knee_flexion'][i]:5.1f} deg gebeugt", None),
                 (f"Huefte {res.angles['hip_angle'][i]:5.1f} deg", None),
                 (f"Oberkoerper {res.angles['torso_angle'][i]:5.1f} deg", None)]
        if cycle_of[i] >= 0:
            row = res.rows[cycle_of[i]]
            lo, hi = res.targets["knee_extension"][:2]
            lines.append((f"Umdrehung {cycle_of[i] + 1}: Knie unten {row['knee_extension']:.1f} deg",
                          lo <= row["knee_extension"] <= hi))
        draw_text_panel(frame, lines)
        writer.write(frame)
        if i % 30 == 0:
            progress(i / len(t), "Erstelle Video mit Skelett")
    cap.release()
    if writer:
        writer.release()


def analyze_file(path: Path, out_dir: Path, crank_mm: float | None, side: str = "auto",
                 model: str = "heavy", max_seconds: float | None = None, render: bool = True,
                 profile: str | None = None, rider=None, progress: Progress = console_progress,
                 quiet: bool = False):
    raw, fps = detect_video(path, model, max_seconds,
                            lambda f, m: progress(0.85 * f if render else f, m))
    progress(0.85 if render else 0.95, "Berechne Winkel und Empfehlungen")
    track = build_track(raw, fps, side=side)
    res = analyze_track(track, crank_mm, profile, rider)
    write_outputs(res, out_dir)
    if render:
        render_video(path, out_dir / "analyse.mp4", res, lambda f, m: progress(0.85 + 0.15 * f, m))
    progress(1.0, "Fertig")
    if not quiet:
        print()
        print(report_text(res))
        print(f"\nErgebnisse gespeichert in: {out_dir}")
    return res
