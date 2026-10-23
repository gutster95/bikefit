"""Rider and bike profile: stored once in profil.json, used by every analysis."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

# Anthropometric segment ratios relative to body height (Drillis & Contini,
# as tabulated by Winter): greater trochanter height and ankle height.
TROCHANTER_RATIO = 0.530
ANKLE_RATIO = 0.039
LEMOND_FACTOR = 0.883  # saddle height (BB center to saddle top) = inseam * 0.883

FLEXIBILITY = {
    "1": ("gering", "Fingerspitzen kommen im Stand mit gestreckten Beinen höchstens bis zum Schienbein"),
    "2": ("mittel", "Fingerspitzen erreichen die Knöchel oder Zehen"),
    "3": ("gut", "Handflächen oder Fingerknöchel erreichen den Boden"),
}
GOALS = {"1": "komfort", "2": "sport", "3": "rennen"}
COMPLAINTS = {"1": "knie_vorne", "2": "knie_hinten", "3": "ruecken", "4": "nacken",
              "5": "taube_haende", "6": "taube_fuesse", "7": "sitzbeschwerden"}


class _FromDict:
    @classmethod
    def from_dict(cls, data: dict):
        """Ignores unknown keys, so older or richer files still load."""
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in names})


@dataclass
class Rider(_FromDict):
    groesse_cm: float | None = None
    schrittlaenge_cm: float | None = None
    beweglichkeit: str = "mittel"
    ziel: str = "sport"
    beschwerden: list[str] = field(default_factory=list)


@dataclass
class Bike(_FromDict):
    typ: str = "rennrad"  # rennrad | zeitfahren
    marke: str = ""
    modell: str = ""
    rahmengroesse: str = ""
    stack_mm: float | None = None
    reach_mm: float | None = None
    sitzwinkel_grad: float | None = None
    kurbel_mm: float | None = None
    sattelhoehe_mm: float | None = None  # BB center to top of saddle, along seat tube
    sattelversatz_mm: float | None = None  # saddle tip behind BB, horizontal
    vorbau_mm: float | None = None
    vorbau_winkel_grad: float | None = None
    spacer_mm: float | None = None


@dataclass
class Profile:
    fahrer: Rider = field(default_factory=Rider)
    rad: Bike = field(default_factory=Bike)

    def save(self, path: Path):
        path.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Profile":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(fahrer=Rider.from_dict(data.get("fahrer", {})), rad=Bike.from_dict(data.get("rad", {})))


def _ask(prompt: str, current, cast=str):
    shown = "" if current in (None, "", []) else f" [{current}]"
    while True:
        answer = input(f"{prompt}{shown}: ").strip()
        if not answer:
            return current
        try:
            return cast(answer.replace(",", "."))
        except ValueError:
            print("  Bitte eine Zahl eingeben.")


def _choose(prompt: str, options: dict, current: str) -> str:
    print(prompt)
    for key, value in options.items():
        label = value[0] + " – " + value[1] if isinstance(value, tuple) else value
        print(f"  {key}) {label}")
    names = {k: (v[0] if isinstance(v, tuple) else v) for k, v in options.items()}
    answer = input(f"Auswahl [{current}]: ").strip()
    return names.get(answer, current)


def interactive(path: Path):
    """Asks for every field in German; Enter keeps the stored value."""
    p = Profile.load(path)
    f, r = p.fahrer, p.rad
    print("\nFAHRER (Enter übernimmt den Wert in Klammern)\n")
    f.groesse_cm = _ask("Körpergröße in cm", f.groesse_cm, float)
    f.schrittlaenge_cm = _ask("Schrittlänge in cm (barfuß, Buch zwischen die Beine, Oberkante bis Boden)",
                              f.schrittlaenge_cm, float)
    f.beweglichkeit = _choose("Beweglichkeit: Im Stand mit gestreckten Beinen nach vorn beugen.",
                              FLEXIBILITY, f.beweglichkeit)
    f.ziel = _choose("Ziel:", GOALS, f.ziel)
    print("Beschwerden (Nummern mit Komma trennen, leer = keine Änderung, 0 = keine):")
    for k, v in COMPLAINTS.items():
        print(f"  {k}) {v}")
    answer = input(f"Auswahl {f.beschwerden}: ").strip()
    if answer == "0":
        f.beschwerden = []
    elif answer:
        f.beschwerden = [COMPLAINTS[a.strip()] for a in answer.split(",") if a.strip() in COMPLAINTS]

    print("\nRAD (Geometrie steht auf der Herstellerseite; Ist-Maße mit dem Maßband)\n")
    r.typ = _choose("Radtyp:", {"1": "rennrad", "2": "zeitfahren"}, r.typ)
    r.modell = _ask("Modell", r.modell)
    r.rahmengroesse = _ask("Rahmengröße", r.rahmengroesse)
    r.stack_mm = _ask("Stack in mm", r.stack_mm, float)
    r.reach_mm = _ask("Reach in mm", r.reach_mm, float)
    r.sitzwinkel_grad = _ask("Sitzwinkel in Grad", r.sitzwinkel_grad, float)
    r.kurbel_mm = _ask("Kurbellänge in mm", r.kurbel_mm, float)
    r.sattelhoehe_mm = _ask("Sattelhöhe in mm (Mitte Tretlager bis Oberkante Sattel, entlang Sitzrohr)",
                            r.sattelhoehe_mm, float)
    r.sattelversatz_mm = _ask("Sattelversatz in mm (Sattelspitze hinter Tretlagermitte, waagerecht)",
                              r.sattelversatz_mm, float)
    r.vorbau_mm = _ask("Vorbaulänge in mm", r.vorbau_mm, float)
    r.vorbau_winkel_grad = _ask("Vorbauwinkel in Grad (z.B. -6)", r.vorbau_winkel_grad, float)
    r.spacer_mm = _ask("Spacer unter dem Vorbau in mm", r.spacer_mm, float)
    p.save(path)
    print(f"\nGespeichert: {path}")
    return p


def adjusted_targets(base: dict, rider: Rider) -> dict:
    """Shifts target ranges for flexibility, goal and complaints."""
    t = dict(base)

    def shift(key, d_lo, d_hi):
        lo, hi, label, unit = t[key]
        t[key] = (lo + d_lo, hi + d_hi, label, unit)

    torso_shift = {"gering": 5, "mittel": 0, "gut": -3}.get(rider.beweglichkeit, 0)
    torso_shift += {"komfort": 5, "sport": 0, "rennen": -3}.get(rider.ziel, 0)
    if torso_shift:
        shift("torso_angle", torso_shift, torso_shift)
    if "knie_vorne" in rider.beschwerden:
        shift("knee_extension", 0, -4)  # prefer the higher-saddle end
    if "knie_hinten" in rider.beschwerden:
        shift("knee_extension", 4, 0)  # prefer the lower-saddle end
    if {"ruecken", "nacken", "taube_haende"} & set(rider.beschwerden):
        shift("torso_angle", 3, 3)
    return t


def plausibility(profile: Profile, segments_mm: dict | None) -> list[str]:
    """Cross-checks the video scale against body height and the saddle
    height against the LeMond rule."""
    notes = []
    f, r = profile.fahrer, profile.rad
    if f.groesse_cm and segments_mm:
        expected = (TROCHANTER_RATIO - ANKLE_RATIO) * f.groesse_cm * 10
        measured = segments_mm["thigh"] + segments_mm["shank"]
        ratio = measured / expected
        if abs(ratio - 1) > 0.12:
            notes.append(f"Beinlänge im Video ({measured:.0f} mm) passt schlecht zur Körpergröße "
                         f"(erwartet ca. {expected:.0f} mm). Kurbellänge oder Kameraposition prüfen.")
    if f.schrittlaenge_cm:
        lemond = LEMOND_FACTOR * f.schrittlaenge_cm * 10
        text = f"Startwert Sattelhöhe nach LeMond-Formel: {lemond:.0f} mm"
        if r.sattelhoehe_mm:
            text += f" (aktuell {r.sattelhoehe_mm:.0f} mm, Differenz {r.sattelhoehe_mm - lemond:+.0f} mm)"
        notes.append(text + ". Nur grober Richtwert, die Videomessung hat Vorrang.")
    return notes
