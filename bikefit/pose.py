"""Markerless pose detection with MediaPipe Pose Landmarker.

Returns per-frame pixel coordinates for both body sides; the side facing the
camera is chosen later in tracks.py.
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

import numpy as np

MODEL_URLS = {
    "lite": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task",
    "full": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task",
    "heavy": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task",
}
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"

# MediaPipe landmark indices per side
LANDMARKS = {
    "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23, "knee": 25,
             "ankle": 27, "heel": 29, "toe": 31},
    "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24, "knee": 26,
              "ankle": 28, "heel": 30, "toe": 32},
}
JOINTS = list(LANDMARKS["left"].keys())


def model_path(variant: str) -> Path:
    path = MODEL_DIR / f"pose_landmarker_{variant}.task"
    if not path.exists():
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Lade Pose-Modell '{variant}' herunter (einmalig) ...")
        urllib.request.urlretrieve(MODEL_URLS[variant], path)
    return path


class PoseDetector:
    """Wraps PoseLandmarker in VIDEO mode."""

    def __init__(self, variant: str = "heavy"):
        import mediapipe as mp
        from mediapipe.tasks.python import BaseOptions
        from mediapipe.tasks.python import vision

        self._mp = mp
        options = vision.PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(model_path(variant))),
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        self._last_ts = -1

    def detect(self, frame_bgr: np.ndarray, timestamp_ms: int):
        """Returns {side: {joint: (x, y, z, visibility)}} in pixels, or None."""
        h, w = frame_bgr.shape[:2]
        rgb = frame_bgr[:, :, ::-1].copy()
        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb)
        timestamp_ms = max(int(timestamp_ms), self._last_ts + 1)
        self._last_ts = timestamp_ms
        result = self._landmarker.detect_for_video(image, timestamp_ms)
        if not result.pose_landmarks:
            return None
        lms = result.pose_landmarks[0]
        out = {}
        for side, idx in LANDMARKS.items():
            out[side] = {
                joint: (lms[i].x * w, lms[i].y * h, lms[i].z * w, lms[i].visibility)
                for joint, i in idx.items()
            }
        return out

    def close(self):
        self._landmarker.close()
