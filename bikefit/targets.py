"""Target ranges and the rule set that turns metrics into recommendations.

Ranges are common dynamic bike-fit guidelines for a road bike. They are
starting points, not hard limits, and will move into a config file later.
"""
from __future__ import annotations

import math

ROAD = {
    "knee_extension": (30.0, 40.0, "Kniebeugung unten (max. Streckung)", "°"),
    "knee_flexion_max": (105.0, 120.0, "Kniebeugung oben", "°"),
    "hip_closed": (45.0, 75.0, "Hüftwinkel geschlossen (oben)", "°"),
    "ankle_range": (15.0, 30.0, "Bewegungsumfang Fußgelenk", "°"),
    "torso_angle": (35.0, 50.0, "Oberkörper zur Horizontalen", "°"),
    "shoulder_angle": (80.0, 95.0, "Schulterwinkel", "°"),
    "elbow_flexion": (15.0, 30.0, "Ellbogenbeugung", "°"),
    "kops_mm": (-20.0, 20.0, "Knie vor Pedalachse bei 3 Uhr", "mm"),
}
# Time trial / triathlon on aero bars: flatter torso, more closed hip,
# elbows bent roughly 90 deg under the shoulders.
TT = {
    **ROAD,
    "hip_closed": (40.0, 70.0, "Hüftwinkel geschlossen (oben)", "°"),
    "torso_angle": (10.0, 25.0, "Oberkörper zur Horizontalen", "°"),
    "shoulder_angle": (80.0, 100.0, "Schulterwinkel", "°"),
    "elbow_flexion": (70.0, 100.0, "Ellbogenbeugung", "°"),
}
# Knee-over-pedal is a road heuristic; TT positions sit far forward on purpose.
del TT["kops_mm"]
PROFILES = {"rennrad": ROAD, "zeitfahren": TT}
MAX_STEP_MM = 10  # never move a contact point more than this in one round
ALL_GOOD = "Alle gemessenen Werte liegen im Zielbereich. Keine Änderung nötig."
MIN_STEP_MM = 3  # smaller changes are within the measurement uncertainty


def evaluate(summary: dict, targets=ROAD) -> list[dict]:
    rows = []
    for key, (lo, hi, label, unit) in targets.items():
        if key not in summary:
            continue
        v = summary[key]["median"]
        status = "ok" if lo <= v <= hi else ("niedrig" if v < lo else "hoch")
        rows.append({"key": key, "label": label, "unit": unit, "value": v,
                     "std": summary[key]["std"], "lo": lo, "hi": hi, "status": status})
    return rows


def saddle_height_change_mm(knee_ext_deg: float, target_deg: float,
                            thigh_mm: float, shank_mm: float) -> float:
    """Change in hip-to-ankle distance needed to move the knee from the
    measured to the target flexion at full extension (law of cosines). The
    hip-ankle line at the bottom of the stroke runs close to the seat tube,
    so this is a good estimate for the saddle height change."""
    def dist(flex):
        inc = math.radians(180.0 - flex)
        return math.sqrt(thigh_mm**2 + shank_mm**2 - 2 * thigh_mm * shank_mm * math.cos(inc))
    return dist(target_deg) - dist(knee_ext_deg)


def recommend(summary: dict, segments: dict, mm_per_px: float | None,
              targets=ROAD, bike=None) -> list[str]:
    """One change at a time, in fitting order: saddle height, setback, cockpit.
    bike (profile.Bike) turns relative changes into absolute settings."""
    tips = []
    ext = summary["knee_extension"]["median"]
    lo, hi = targets["knee_extension"][:2]
    if not lo <= ext <= hi:
        target = lo + 2 if ext < lo else hi - 2
        direction = "senken" if ext < lo else "anheben"
        text = f"Sattelhöhe {direction}: Knie unten {ext:.0f}° gebeugt, Ziel {lo:.0f}–{hi:.0f}°."
        if mm_per_px:
            delta = saddle_height_change_mm(ext, target, segments["thigh_px"] * mm_per_px,
                                            segments["shank_px"] * mm_per_px)
            step = max(-MAX_STEP_MM, min(MAX_STEP_MM, delta))
            text += f" Rechnerisch ca. {abs(delta):.0f} mm, in diesem Schritt {abs(step):.0f} mm"
            if bike and bike.sattelhoehe_mm:
                text += f" (Sattelhöhe {bike.sattelhoehe_mm:.0f} → {bike.sattelhoehe_mm + step:.0f} mm)"
            text += ", dann neu messen."
        else:
            text += " Für eine Angabe in mm Kurbellänge mit --kurbel angeben."
        if ext < lo and summary.get("ankle_range", {}).get("median", 0) > targets["ankle_range"][1]:
            text += " Das große Fußgelenk-Spiel bestätigt: Du gleichst eine zu hohe Sattelposition mit dem Fuß aus."
        tips.append(text)
        tips.append("Erst die Sattelhöhe anpassen und neu messen, danach Sattelversatz und Cockpit.")
        return tips

    if "kops_mm" in summary and "kops_mm" in targets:
        kops = summary["kops_mm"]["median"]
        klo, khi = targets["kops_mm"][:2]
        if kops > khi + MIN_STEP_MM:
            step = min(MAX_STEP_MM, kops - khi)
            tips.append(f"Sattel etwas nach hinten: Knie {kops:.0f} mm vor der Pedalachse bei 3 Uhr. "
                        f"Zuerst {step:.0f} mm{_setback(bike, step)}, Sattelhöhe danach prüfen.")
        elif kops < klo - MIN_STEP_MM:
            step = min(MAX_STEP_MM, klo - kops)
            tips.append(f"Sattel etwas nach vorn: Knie {-kops:.0f} mm hinter der Pedalachse bei 3 Uhr. "
                        f"Zuerst {step:.0f} mm{_setback(bike, -step)}, Sattelhöhe danach prüfen.")
        if tips:
            return tips

    torso = summary["torso_angle"]["median"]
    shoulder = summary["shoulder_angle"]["median"]
    elbow = summary["elbow_flexion"]["median"]
    arms_reliable = summary["elbow_flexion"]["std"] <= 8
    if not arms_reliable:
        tips.append("Keine Cockpit-Empfehlung: Armwinkel zu unruhig. Hände während der Aufnahme ruhig am Lenker lassen.")
    elif shoulder > targets["shoulder_angle"][1] or elbow < targets["elbow_flexion"][0]:
        tips.append(f"Cockpit eher zu lang: Schulterwinkel {shoulder:.0f}°, Ellbogen {elbow:.0f}° gebeugt. "
                    "Kürzerer Vorbau oder Lenker näher heranholen." + _stem(summary, segments, mm_per_px, targets, bike, -1))
    elif shoulder < targets["shoulder_angle"][0] or elbow > targets["elbow_flexion"][1]:
        tips.append(f"Cockpit eher zu kurz: Schulterwinkel {shoulder:.0f}°, Ellbogen {elbow:.0f}° gebeugt. "
                    "Längerer Vorbau möglich." + _stem(summary, segments, mm_per_px, targets, bike, 1))
    if torso < targets["torso_angle"][0] and summary["hip_closed"]["median"] < targets["hip_closed"][0]:
        tips.append(f"Oberkörper sehr flach ({torso:.0f}°) und Hüfte oben eng: Lenker etwas höher (Spacer).")
    elif torso > targets["torso_angle"][1]:
        tips.append(f"Oberkörper recht aufrecht ({torso:.0f}°): für mehr Aero kann der Lenker tiefer, wenn es bequem bleibt.")
    if not tips:
        tips.append(ALL_GOOD)
    return tips


def _setback(bike, change_mm: float) -> str:
    if bike and bike.sattelversatz_mm is not None:
        return f" (Versatz {bike.sattelversatz_mm:.0f} → {bike.sattelversatz_mm + change_mm:.0f} mm)"
    return ""


def _stem(summary, segments, mm_per_px, targets, bike, direction: int) -> str:
    """Hands move on an arc around the shoulder, so the reach change for a
    target shoulder angle is roughly arm length times the angle change.
    direction: -1 shorter, +1 longer, as decided by the rule."""
    if not mm_per_px or "arm_px" not in segments:
        return ""
    lo, hi = targets["shoulder_angle"][:2]
    shoulder = summary["shoulder_angle"]["median"]
    change = math.radians(min(max(shoulder, lo + 2), hi - 2) - shoulder) * segments["arm_px"] * mm_per_px
    step = round(change / 10) * 10  # stems come in 10 mm steps
    if step * direction <= 0:
        return (" Der Schulterwinkel passt aber schon, also eher kleine Korrektur:"
                " Bremshebel etwas nach oben/hinten drehen oder Arme bewusst leicht beugen.")
    text = f" Rechnerisch ca. {abs(change):.0f} mm, also Vorbau {abs(step):.0f} mm {'länger' if step > 0 else 'kürzer'}"
    if bike and bike.vorbau_mm:
        text += f" ({bike.vorbau_mm:.0f} → {bike.vorbau_mm + step:.0f} mm)"
    return text + "."


# Fitting order: what to change first when several values are off.
STEP = {"knee_extension": 1, "knee_flexion_max": 1, "ankle_range": 1, "kops_mm": 2,
        "hip_closed": 3, "torso_angle": 3, "shoulder_angle": 3, "elbow_flexion": 3}


def corrections(rows: list[dict], summary: dict, segments: dict, mm_per_px: float | None,
                bike=None, tt: bool = False) -> list[dict]:
    """Adds a short bike change ("korrektur") and its place in the fitting
    order ("schritt") to every row outside its target range. Uses the row's
    own range, so it also works on stored results."""
    def mm(key):
        return segments[key] * mm_per_px if mm_per_px and key in segments else None

    thigh, shank, arm = mm("thigh_px"), mm("shank_px"), mm("arm_px")
    saddle_off = any(r["key"] == "knee_extension" and r["status"] != "ok" for r in rows)
    for r in rows:
        r["korrektur"], r["schritt"] = None, None
        if r["status"] == "ok":
            continue
        low = r["status"] == "niedrig"
        v, lo, hi = r["value"], r["lo"], r["hi"]
        k = r["key"]
        outside = (lo - v) if low else (v - hi)
        if outside < (MIN_STEP_MM if r["unit"] == "mm" else 1.5):
            unit = " mm" if r["unit"] == "mm" else "°"
            r["korrektur"] = (f"Nur {outside:.0f}{unit} außerhalb, das liegt in der Messgenauigkeit. "
                              "Nichts ändern, beim nächsten Video wieder anschauen.") if outside >= 0.5 else (
                              "Liegt praktisch auf der Grenze. Nichts ändern.")
            continue
        if k == "knee_extension":
            text = f"Sattel {'tiefer' if low else 'höher'} stellen"
            if thigh and shank:
                delta = saddle_height_change_mm(v, lo + 2 if low else hi - 2, thigh, shank)
                step = max(-MAX_STEP_MM, min(MAX_STEP_MM, delta))
                text += f": rechnerisch {abs(delta):.0f} mm, jetzt {abs(step):.0f} mm"
                if bike and bike.sattelhoehe_mm:
                    text += f" ({bike.sattelhoehe_mm:.0f} → {bike.sattelhoehe_mm + step:.0f} mm)"
            text += "." + (" Das Bein ist unten fast gestreckt." if low else " Das Bein bleibt unten zu stark gebeugt.")
        elif k == "knee_flexion_max":
            text = ("Knie oben weit offen, meist Folge eines hohen Sattels. Erst die Sattelhöhe prüfen."
                    if low else "Knie oben stark gebeugt: Sattel etwas höher oder kürzere Kurbel "
                    "(2,5 bis 5 mm kürzer) entlastet das Knie.")
        elif k == "ankle_range":
            text = ("Fuß arbeitet wenig. Unkritisch, eventuell Sattel 2 bis 3 mm höher und bewusst rund treten."
                    if low else "Fuß kippt stark ab, oft Ausgleich für einen zu hohen Sattel: Sattel 3 bis 5 mm tiefer "
                    "oder Cleats 2 bis 3 mm weiter nach hinten.")
        elif k == "kops_mm":
            step = min(MAX_STEP_MM, (lo - v) if low else (v - hi))
            change = step if low else -step
            text = (f"Sattel {step:.0f} mm nach {'vorn' if low else 'hinten'} schieben"
                    f"{_setback(bike, -change)}. Das Knie steht {abs(v):.0f} mm "
                    f"{'hinter' if v < 0 else 'vor'} der Pedalachse. Danach Sattelhöhe prüfen, "
                    "beim Verschieben ändert sie sich leicht.")
        elif k == "hip_closed":
            text = ("Hüfte oben zu eng: Lenker höher (10 mm Spacer unter den Vorbau) oder kürzerer Vorbau. "
                    "Kürzere Kurbeln öffnen die Hüfte ebenfalls." if low else
                    "Hüfte bleibt offen: Lenker darf tiefer (10 mm Spacer über den Vorbau), wenn du sportlicher sitzen willst.")
        elif k == "torso_angle":
            if tt:
                text = ("Sehr flach: Auflegerpads 10 mm höher." if low else "Recht aufrecht: Auflegerpads 10 mm tiefer.")
            else:
                text = (f"Oberkörper sehr flach ({v:.0f}°): Lenker höher, 10 mm Spacer unter den Vorbau "
                        f"{_spacer(bike, 10)}oder Vorbau mit mehr Steigung." if low else
                        f"Oberkörper aufrecht ({v:.0f}°): für mehr Aero Lenker tiefer, 10 mm Spacer über den Vorbau "
                        f"{_spacer(bike, -10)}. Nur wenn es bequem bleibt.")
        elif k == "shoulder_angle":
            text = (("Pads weiter nach vorn." if low else "Pads weiter nach hinten.") if tt else
                    f"Cockpit {'zu kurz' if low else 'zu lang'}: Vorbau {'länger' if low else 'kürzer'}."
                    + _stem_mm(v, lo, hi, arm, bike))
        elif k == "elbow_flexion":
            if tt:
                text = ("Arme zu gestreckt: Pads näher zum Körper." if low else "Arme zu stark gebeugt: Pads weiter nach vorn.")
            else:
                shoulder = summary.get("shoulder_angle", {}).get("median")
                shoulder_ok = shoulder is not None and shoulder <= next(
                    (x["hi"] for x in rows if x["key"] == "shoulder_angle"), 95)
                text = (("Arme fast gestreckt, der Schulterwinkel passt aber. Darum nicht den Vorbau tauschen: "
                         "Bremsgriffe 5 bis 10 mm höher bzw. näher drehen und die Ellbogen bewusst locker beugen."
                         if shoulder_ok else
                         "Arme fast gestreckt: Lenker näher heran (Vorbau 10 mm kürzer) oder etwas höher. "
                         "Ellbogen locker beugen, das dämpft Stöße.") if low else
                        "Arme stark gebeugt: Cockpit eher zu kurz oder zu hoch, Vorbau 10 mm länger oder Lenker tiefer.")
            if summary.get(k, {}).get("std", 0) > 8:
                text += " Achtung, der Armwinkel schwankt stark, bitte Hände ruhig halten."
        else:
            continue
        r["schritt"] = STEP[k]
        if saddle_off and STEP[k] > 1:
            text += " Erst nach der Sattelhöhe ändern."
        r["korrektur"] = text
    return rows


def _spacer(bike, change_mm: float) -> str:
    if bike and bike.spacer_mm is not None:
        return f"({bike.spacer_mm:.0f} → {max(0, bike.spacer_mm + change_mm):.0f} mm) "
    return ""


def _stem_mm(shoulder, lo, hi, arm_mm, bike) -> str:
    if not arm_mm:
        return ""
    change = math.radians(min(max(shoulder, lo + 2), hi - 2) - shoulder) * arm_mm
    step = round(change / 10) * 10 or (10 if change > 0 else -10)
    text = f" Rechnerisch {abs(change):.0f} mm, also {abs(step):.0f} mm"
    if bike and bike.vorbau_mm:
        text += f" ({bike.vorbau_mm:.0f} → {bike.vorbau_mm + step:.0f} mm)"
    return text + "."
