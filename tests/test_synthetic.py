"""Checks the metric pipeline against a simulated rider with known geometry.

The pose model is skipped: joints are computed from crank kinematics, then
noised, so every expected value is known exactly.
"""
import numpy as np
import pytest

from bikefit import metrics, targets
from bikefit.analysis import analyze_track, localize, result_data
from bikefit.tracks import Track, lowpass

MM_PER_PX = 2.0
CRANK = 172.5
THIGH, SHANK, FOOT = 440.0, 430.0, 260.0


def simulate(hip_offset_mm=(-170.0, -770.0), fps=60.0, rpm=90.0, seconds=40.0,
             noise_px=2.0, facing=1, seed=0):
    rng = np.random.default_rng(seed)
    n = int(fps * seconds)
    theta = 2 * np.pi * rpm / 60 * np.arange(n) / fps
    s = 1 / MM_PER_PX
    bb = np.array([1000.0, 800.0])
    # crank angle 0 = pointing forward (3 o'clock), rotating down
    pedal = bb + CRANK * s * np.column_stack([facing * np.cos(theta), np.sin(theta)])
    # foot pitch: heel drops on the down stroke
    pitch = np.radians(10 + 8 * np.sin(theta + 0.5))
    u = np.column_stack([facing * np.cos(pitch), np.sin(pitch)])  # forward along foot
    up = np.column_stack([u[:, 1] * facing, -u[:, 0] * facing])   # normal, pointing up
    heel = pedal - 0.7 * FOOT * s * u
    toe = pedal + 0.3 * FOOT * s * u
    ankle = pedal - 110 * s * u + 90 * s * up
    hip = np.tile(bb + np.array([facing * hip_offset_mm[0], hip_offset_mm[1]]) * s, (n, 1))
    # two-link IK, knee forward of the hip-ankle line
    d = ankle - hip
    L = np.linalg.norm(d, axis=1)
    a = (THIGH * s) ** 2
    along = (a - (SHANK * s) ** 2 + L ** 2) / (2 * L)
    h = np.sqrt(np.clip(a - along ** 2, 0, None))
    e = d / L[:, None]
    perp = np.column_stack([e[:, 1], -e[:, 0]]) * facing
    knee = hip + e * along[:, None] + perp * h[:, None]
    if np.mean(knee[:, 0] - hip[:, 0]) * facing < 0:
        knee = hip + e * along[:, None] - perp * h[:, None]
    torso = np.radians(40)
    shoulder = hip + 580 * s * np.array([facing * np.cos(torso), -np.sin(torso)])
    elbow = shoulder + 290 * s * np.array([facing * np.cos(np.radians(-75)), -np.sin(np.radians(-75))])
    wrist = elbow + 260 * s * np.array([facing * np.cos(np.radians(-20)), -np.sin(np.radians(-20))])
    truth = {"knee_flexion": 180 - metrics.included_angle(hip, knee, ankle)}
    pts = {"shoulder": shoulder, "elbow": elbow,
           "wrist": wrist, "hip": hip, "knee": knee, "ankle": ankle,
           "heel": heel, "toe": toe}
    noisy = {k: lowpass(v + rng.normal(0, noise_px, v.shape), fps) if noise_px else v
             for k, v in pts.items()}
    noisy["pedal"] = noisy["heel"] + 0.7 * (noisy["toe"] - noisy["heel"])
    return Track(fps=fps, side="right", facing=facing, points=noisy), truth, pedal, knee


@pytest.mark.parametrize("facing", [1, -1])
def test_cycles_and_knee_angle(facing):
    track, truth, _, _ = simulate(facing=facing)
    res = analyze_track(track, CRANK)
    assert abs(len(res.cycles) - 60) <= 2  # 40 s at 90 rpm
    assert res.summary["cadence_rpm"]["median"] == pytest.approx(90, abs=2)
    true_ext = truth["knee_flexion"].min()
    assert res.summary["knee_extension"]["median"] == pytest.approx(true_ext, abs=1.5)
    assert res.crank.mm_per_px == pytest.approx(MM_PER_PX, rel=0.05)
    assert res.summary["torso_angle"]["median"] == pytest.approx(40, abs=1)


def test_kops_matches_geometry():
    track, _, pedal, knee = simulate()
    res = analyze_track(track, CRANK)
    # true KOPS: crank exactly forward is theta = 0 (every cycle start of the sim)
    true_kops = (knee[0, 0] - pedal[0, 0]) * MM_PER_PX
    assert res.summary["kops_mm"]["median"] == pytest.approx(true_kops, abs=12)


def test_saddle_recommendation_closes_the_gap():
    """Saddle too high -> recommendation says lower; applying the computed
    change to the simulated rider lands inside the target range."""
    track, truth, _, _ = simulate(hip_offset_mm=(-170.0, -800.0))
    res = analyze_track(track, CRANK)
    ext = res.summary["knee_extension"]["median"]
    assert ext < 30
    assert "Lower" in localize(result_data(res), "en")["recommendations"][0]
    target = 30 + 2
    delta = targets.saddle_height_change_mm(ext, target, res.segments["thigh_px"] * MM_PER_PX,
                                            res.segments["shank_px"] * MM_PER_PX)
    assert delta < 0
    # move the hip along the seat tube (73 deg) by delta
    st = np.radians(73)
    new_offset = (-170.0 + delta * np.cos(st), -800.0 - delta * np.sin(st))
    _, truth2, _, _ = simulate(hip_offset_mm=new_offset)
    assert 30 <= truth2["knee_flexion"].min() <= 36


def _raw_from_track(track, far_offset=(40.0, 0.0)):
    """Fake MediaPipe output: near side from the track, far leg shifted half a
    crank turn so the legs cross like on a real bike."""
    n = len(track)
    half = int(round(track.fps * 60 / 90 / 2))
    raw = []
    for i in range(n):
        near = {j: (*track.points[j][i], 0.0, 0.99) for j in
                ("shoulder", "elbow", "wrist", "hip", "knee", "ankle", "heel", "toe")}
        k = (i + half) % n
        far = {j: (track.points[j][k][0] + far_offset[0], track.points[j][k][1] + far_offset[1], 0.1, 0.9)
               for j in near}
        raw.append({"right": near, "left": far})
    return raw


def test_cleaning_repairs_swaps_and_jumps():
    from bikefit.tracks import build_track
    track, truth, _, _ = simulate(noise_px=0.0)
    raw = _raw_from_track(track)
    rng = np.random.default_rng(1)
    swap_frames = rng.choice(np.arange(10, len(raw) - 10), 40, replace=False)
    for i in swap_frames:
        for j in ("knee", "ankle", "heel", "toe"):
            raw[i]["right"][j], raw[i]["left"][j] = raw[i]["left"][j], raw[i]["right"][j]
    jump_frames = rng.choice(np.arange(10, len(raw) - 10), 20, replace=False)
    for i in jump_frames:
        x, y, z, v = raw[i]["right"]["ankle"]
        raw[i]["right"]["ankle"] = (x + 150, y - 120, z, v)

    dirty = analyze_track(build_track(raw, track.fps, side="right", clean=False), CRANK)
    clean_track = build_track(raw, track.fps, side="right")
    clean = analyze_track(clean_track, CRANK)
    true_ext = truth["knee_flexion"].min()
    assert clean_track.corrections["leg_swaps"] >= 35
    assert abs(clean.summary["knee_extension"]["median"] - true_ext) < 1.0
    # the median hides single bad frames; the worst cycle shows them
    worst = lambda res: max(abs(r["knee_extension"] - true_ext) for r in res.rows)
    assert worst(clean) < 1.0
    assert worst(clean) < worst(dirty)
