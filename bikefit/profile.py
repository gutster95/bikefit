"""Rider and bike profile: stored once in profile.json, used by every analysis."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

from .i18n import DEFAULT_LANG, t

# Anthropometric segment ratios relative to body height (Drillis & Contini,
# as tabulated by Winter): greater trochanter height and ankle height.
TROCHANTER_RATIO = 0.530
ANKLE_RATIO = 0.039
LEMOND_FACTOR = 0.883  # saddle height (BB center to saddle top) = inseam * 0.883

FLEXIBILITY = {
    "1": ("low", "fingertips reach the shins at most, standing with straight legs"),
    "2": ("medium", "fingertips reach the ankles or toes"),
    "3": ("high", "palms or knuckles reach the floor"),
}
GOALS = {"1": "comfort", "2": "sport", "3": "race"}
COMPLAINTS = {"1": "knee_front", "2": "knee_back", "3": "lower_back", "4": "neck",
              "5": "numb_hands", "6": "numb_feet", "7": "saddle_pain"}
BIKE_TYPES = ("road", "tt")


class _FromDict:
    @classmethod
    def from_dict(cls, data: dict):
        """Ignores unknown keys, so older or richer files still load."""
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in names})


@dataclass
class Rider(_FromDict):
    height_cm: float | None = None
    inseam_cm: float | None = None
    flexibility: str = "medium"
    goal: str = "sport"
    complaints: list[str] = field(default_factory=list)


@dataclass
class Bike(_FromDict):
    type: str = "road"  # road | tt (time trial / triathlon)
    brand: str = ""
    model: str = ""
    frame_size: str = ""
    stack_mm: float | None = None
    reach_mm: float | None = None
    seat_angle_deg: float | None = None
    crank_mm: float | None = None
    saddle_height_mm: float | None = None  # BB center to top of saddle, along seat tube
    saddle_setback_mm: float | None = None  # saddle tip behind BB, horizontal
    stem_mm: float | None = None
    stem_angle_deg: float | None = None
    spacer_mm: float | None = None


@dataclass
class Profile:
    rider: Rider = field(default_factory=Rider)
    bike: Bike = field(default_factory=Bike)

    def save(self, path: Path):
        path.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Profile":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(rider=Rider.from_dict(data.get("rider", {})), bike=Bike.from_dict(data.get("bike", {})))


def _ask(prompt: str, current, cast=str):
    shown = "" if current in (None, "", []) else f" [{current}]"
    while True:
        answer = input(f"{prompt}{shown}: ").strip()
        if not answer:
            return current
        try:
            return cast(answer.replace(",", "."))
        except ValueError:
            print("  Please enter a number.")


def _choose(prompt: str, options: dict, current: str) -> str:
    print(prompt)
    for key, value in options.items():
        label = value[0] + " – " + value[1] if isinstance(value, tuple) else value
        print(f"  {key}) {label}")
    names = {k: (v[0] if isinstance(v, tuple) else v) for k, v in options.items()}
    answer = input(f"Choice [{current}]: ").strip()
    return names.get(answer, current)


def interactive(path: Path):
    """Asks for every field; Enter keeps the stored value."""
    p = Profile.load(path)
    r, b = p.rider, p.bike
    print("\nRIDER (Enter keeps the value in brackets)\n")
    r.height_cm = _ask("Height in cm", r.height_cm, float)
    r.inseam_cm = _ask("Inseam in cm (barefoot, book between the legs, top edge to floor)", r.inseam_cm, float)
    r.flexibility = _choose("Flexibility: bend forward standing with straight legs.", FLEXIBILITY, r.flexibility)
    r.goal = _choose("Goal:", GOALS, r.goal)
    print("Complaints (numbers separated by commas, empty = no change, 0 = none):")
    for k, v in COMPLAINTS.items():
        print(f"  {k}) {v}")
    answer = input(f"Choice {r.complaints}: ").strip()
    if answer == "0":
        r.complaints = []
    elif answer:
        r.complaints = [COMPLAINTS[a.strip()] for a in answer.split(",") if a.strip() in COMPLAINTS]

    print("\nBIKE (geometry from the manufacturer's website; current settings with a tape measure)\n")
    b.type = _choose("Bike type:", {"1": "road", "2": "tt"}, b.type)
    b.model = _ask("Model", b.model)
    b.frame_size = _ask("Frame size", b.frame_size)
    b.stack_mm = _ask("Stack in mm", b.stack_mm, float)
    b.reach_mm = _ask("Reach in mm", b.reach_mm, float)
    b.seat_angle_deg = _ask("Seat tube angle in degrees", b.seat_angle_deg, float)
    b.crank_mm = _ask("Crank length in mm", b.crank_mm, float)
    b.saddle_height_mm = _ask("Saddle height in mm (BB center to top of saddle, along the seat tube)",
                              b.saddle_height_mm, float)
    b.saddle_setback_mm = _ask("Saddle setback in mm (saddle tip behind BB center, horizontal)",
                               b.saddle_setback_mm, float)
    b.stem_mm = _ask("Stem length in mm", b.stem_mm, float)
    b.stem_angle_deg = _ask("Stem angle in degrees (e.g. -6)", b.stem_angle_deg, float)
    b.spacer_mm = _ask("Spacers under the stem in mm", b.spacer_mm, float)
    p.save(path)
    print(f"\nSaved: {path}")
    return p


def adjusted_targets(base: dict, rider: Rider) -> dict:
    """Shifts target ranges for flexibility, goal and complaints."""
    out = dict(base)

    def shift(key, d_lo, d_hi):
        lo, hi, unit = out[key]
        out[key] = (lo + d_lo, hi + d_hi, unit)

    torso_shift = {"low": 5, "medium": 0, "high": -3}.get(rider.flexibility, 0)
    torso_shift += {"comfort": 5, "sport": 0, "race": -3}.get(rider.goal, 0)
    if torso_shift:
        shift("torso_angle", torso_shift, torso_shift)
    if "knee_front" in rider.complaints:
        shift("knee_extension", 0, -4)  # prefer the higher-saddle end
    if "knee_back" in rider.complaints:
        shift("knee_extension", 4, 0)  # prefer the lower-saddle end
    if {"lower_back", "neck", "numb_hands"} & set(rider.complaints):
        shift("torso_angle", 3, 3)
    return out


def plausibility(profile: Profile, segments_mm: dict | None, lang: str = DEFAULT_LANG) -> list[str]:
    """Cross-checks the video scale against body height and the saddle
    height against the LeMond rule."""
    notes = []
    r, b = profile.rider, profile.bike
    if r.height_cm and segments_mm:
        expected = (TROCHANTER_RATIO - ANKLE_RATIO) * r.height_cm * 10
        measured = segments_mm["thigh"] + segments_mm["shank"]
        if abs(measured / expected - 1) > 0.12:
            notes.append(t("note.leg_length", lang, measured=measured, expected=expected))
    if r.inseam_cm:
        lemond = LEMOND_FACTOR * r.inseam_cm * 10
        current = (t("note.lemond_current", lang, current=b.saddle_height_mm, diff=b.saddle_height_mm - lemond)
                   if b.saddle_height_mm else "")
        notes.append(t("note.lemond", lang, lemond=lemond, current=current))
    return notes
