import builtins

from bikefit import targets
from bikefit.analysis import analyze_track, localize, result_data
from bikefit.profile import Bike, Profile, Rider, adjusted_targets, interactive, plausibility
from tests.test_synthetic import CRANK, simulate


def test_targets_follow_rider():
    stiff = adjusted_targets(targets.ROAD, Rider(flexibility="low", goal="comfort"))
    assert stiff["torso_angle"][:2] == (45.0, 60.0)
    knee = adjusted_targets(targets.ROAD, Rider(complaints=["knee_front"]))
    assert knee["knee_extension"][:2] == (30.0, 36.0)


def test_profile_gives_absolute_settings():
    track, _, _, _ = simulate(hip_offset_mm=(-170.0, -800.0))
    p = Profile(bike=Bike(crank_mm=CRANK, saddle_height_mm=760))
    res = analyze_track(track, None, rider=p)  # crank length comes from the profile
    assert res.crank.mm_per_px is not None
    data = result_data(res)
    assert "760 →" in localize(data, "en")["recommendations"][0]
    assert "Sattel" in localize(data, "de")["recommendations"][0]


def test_scale_plausibility():
    p = Profile(rider=Rider(height_cm=180, inseam_cm=85))
    ok = plausibility(p, {"thigh": 450, "shank": 440}, "de")
    assert not any("passt schlecht" in n for n in ok)
    bad = plausibility(p, {"thigh": 300, "shank": 290}, "de")
    assert any("passt schlecht" in n for n in bad)
    assert any("does not match" in n for n in plausibility(p, {"thigh": 300, "shank": 290}, "en"))
    assert any("751 mm" in n for n in ok)  # 0.883 * 850


def test_interactive_roundtrip(tmp_path, monkeypatch):
    answers = iter(["182", "86", "1", "3", "1,3", "1", "Tarmac", "56", "565", "395", "73.5",
                    "172,5", "755", "60", "110", "-6", "20"])
    monkeypatch.setattr(builtins, "input", lambda _: next(answers))
    path = tmp_path / "profile.json"
    interactive(path)
    p = Profile.load(path)
    assert p.rider.flexibility == "low" and p.rider.goal == "race"
    assert p.rider.complaints == ["knee_front", "lower_back"]
    assert p.bike.crank_mm == 172.5 and p.bike.stem_angle_deg == -6


def test_corrections_for_every_off_target_value():
    summary = {k: {"median": v, "std": 2.0} for k, v in {
        "knee_extension": 34, "knee_flexion_max": 112, "hip_closed": 60, "ankle_range": 20,
        "torso_angle": 42, "shoulder_angle": 100, "elbow_flexion": 10, "kops_mm": -35}.items()}
    segs = {"thigh_px": 430, "shank_px": 420, "arm_px": 560}
    bike = Bike(saddle_setback_mm=60, stem_mm=110)
    rows = targets.evaluate(summary)
    targets.corrections(rows, summary, segs, 1.0, bike, lang="de")
    by = {r["key"]: r for r in rows}
    assert by["knee_extension"]["fix"] is None
    assert "nach vorn" in by["kops_mm"]["fix"] and "60 → 50 mm" in by["kops_mm"]["fix"]
    assert "kürzer" in by["shoulder_angle"]["fix"] and "110 →" in by["shoulder_angle"]["fix"]
    assert "gestreckt" in by["elbow_flexion"]["fix"]
    assert by["kops_mm"]["step"] == 2 and by["elbow_flexion"]["step"] == 3
    rows = targets.evaluate(summary)
    targets.corrections(rows, summary, segs, 1.0, bike, lang="en")
    assert "forward" in {r["key"]: r for r in rows}["kops_mm"]["fix"]
