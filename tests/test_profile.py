import builtins

from bikefit import targets
from bikefit.analysis import analyze_track
from bikefit.profile import Bike, Profile, Rider, adjusted_targets, interactive, plausibility
from tests.test_synthetic import CRANK, simulate


def test_targets_follow_rider():
    stiff = adjusted_targets(targets.ROAD, Rider(beweglichkeit="gering", ziel="komfort"))
    assert stiff["torso_angle"][:2] == (45.0, 60.0)
    knee = adjusted_targets(targets.ROAD, Rider(beschwerden=["knie_vorne"]))
    assert knee["knee_extension"][:2] == (30.0, 36.0)


def test_profile_gives_absolute_settings():
    track, _, _, _ = simulate(hip_offset_mm=(-170.0, -800.0))
    p = Profile(rad=Bike(kurbel_mm=CRANK, sattelhoehe_mm=760))
    res = analyze_track(track, None, rider=p)  # crank length comes from the profile
    assert res.crank.mm_per_px is not None
    assert "760 →" in res.tips[0]


def test_scale_plausibility():
    p = Profile(fahrer=Rider(groesse_cm=180, schrittlaenge_cm=85))
    ok = plausibility(p, {"thigh": 450, "shank": 440})
    assert not any("passt schlecht" in n for n in ok)
    bad = plausibility(p, {"thigh": 300, "shank": 290})
    assert any("passt schlecht" in n for n in bad)
    assert any("751 mm" in n for n in ok)  # 0.883 * 850


def test_interactive_roundtrip(tmp_path, monkeypatch):
    answers = iter(["182", "86", "1", "3", "1,3", "1", "Tarmac", "56", "565", "395", "73.5",
                    "172,5", "755", "60", "110", "-6", "20"])
    monkeypatch.setattr(builtins, "input", lambda _: next(answers))
    path = tmp_path / "profil.json"
    interactive(path)
    p = Profile.load(path)
    assert p.fahrer.beweglichkeit == "gering" and p.fahrer.ziel == "rennen"
    assert p.fahrer.beschwerden == ["knie_vorne", "ruecken"]
    assert p.rad.kurbel_mm == 172.5 and p.rad.vorbau_winkel_grad == -6


def test_corrections_for_every_off_target_value():
    from bikefit import targets
    from bikefit.profile import Bike
    summary = {k: {"median": v, "std": 2.0} for k, v in {
        "knee_extension": 34, "knee_flexion_max": 112, "hip_closed": 60, "ankle_range": 20,
        "torso_angle": 42, "shoulder_angle": 100, "elbow_flexion": 10, "kops_mm": -35}.items()}
    rows = targets.evaluate(summary)
    segs = {"thigh_px": 430, "shank_px": 420, "arm_px": 560}
    targets.corrections(rows, summary, segs, 1.0, Bike(sattelversatz_mm=60, vorbau_mm=110))
    by = {r["key"]: r for r in rows}
    assert by["knee_extension"]["korrektur"] is None
    assert "nach vorn" in by["kops_mm"]["korrektur"] and "60 → 50 mm" in by["kops_mm"]["korrektur"]
    assert "kürzer" in by["shoulder_angle"]["korrektur"] and "110 →" in by["shoulder_angle"]["korrektur"]
    assert "gestreckt" in by["elbow_flexion"]["korrektur"]
    assert by["kops_mm"]["schritt"] == 2 and by["elbow_flexion"]["schritt"] == 3
