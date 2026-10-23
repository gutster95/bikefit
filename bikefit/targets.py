"""Target ranges and the rules that turn metrics into recommendations.

Ranges are common dynamic bike-fit guidelines for a road bike. They are
starting points, not hard limits. Texts come from i18n so every function
that produces advice takes the display language.
"""
from __future__ import annotations

import math

from .i18n import DEFAULT_LANG, t

# key: (low, high, unit); labels are i18n "metric.<key>"
ROAD = {
    "knee_extension": (30.0, 40.0, "°"),
    "knee_flexion_max": (105.0, 120.0, "°"),
    "hip_closed": (45.0, 75.0, "°"),
    "ankle_range": (15.0, 30.0, "°"),
    "torso_angle": (35.0, 50.0, "°"),
    "shoulder_angle": (80.0, 95.0, "°"),
    "elbow_flexion": (15.0, 30.0, "°"),
    "kops_mm": (-20.0, 20.0, "mm"),
}
# Time trial / triathlon on aero bars: flatter torso, more closed hip,
# elbows bent roughly 90 deg under the shoulders.
TT = {
    **ROAD,
    "hip_closed": (40.0, 70.0, "°"),
    "torso_angle": (10.0, 25.0, "°"),
    "shoulder_angle": (80.0, 100.0, "°"),
    "elbow_flexion": (70.0, 100.0, "°"),
}
# Knee-over-pedal is a road heuristic; TT positions sit far forward on purpose.
del TT["kops_mm"]
PROFILES = {"road": ROAD, "tt": TT}
MAX_STEP_MM = 10  # never move a contact point more than this in one round
MIN_STEP_MM = 3  # smaller changes are within the measurement uncertainty
MIN_STEP_DEG = 1.5

# Fitting order: what to change first when several values are off.
STEP = {"knee_extension": 1, "knee_flexion_max": 1, "ankle_range": 1, "kops_mm": 2,
        "hip_closed": 3, "torso_angle": 3, "shoulder_angle": 3, "elbow_flexion": 3}


def evaluate(summary: dict, targets=ROAD) -> list[dict]:
    rows = []
    for key, (lo, hi, unit) in targets.items():
        if key not in summary:
            continue
        v = summary[key]["median"]
        status = "ok" if lo <= v <= hi else ("low" if v < lo else "high")
        rows.append({"key": key, "unit": unit, "value": v, "std": summary[key]["std"],
                     "lo": lo, "hi": hi, "status": status})
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


def is_done(summary: dict, segments: dict, mm_per_px: float | None, targets=ROAD) -> bool:
    return recommend(summary, segments, mm_per_px, targets) == [t("rec.all_good")]


def recommend(summary: dict, segments: dict, mm_per_px: float | None,
              targets=ROAD, bike=None, lang: str = DEFAULT_LANG) -> list[str]:
    """One change at a time, in fitting order: saddle height, setback, cockpit.
    bike (profile.Bike) turns relative changes into absolute settings."""
    tips = []
    ext = summary["knee_extension"]["median"]
    lo, hi = targets["knee_extension"][:2]
    if not lo <= ext <= hi:
        target = lo + 2 if ext < lo else hi - 2
        direction = t("rec.dir.lower" if ext < lo else "rec.dir.raise", lang)
        text = t("rec.saddle_height", lang, direction=direction, value=ext, lo=lo, hi=hi)
        if mm_per_px:
            delta = saddle_height_change_mm(ext, target, segments["thigh_px"] * mm_per_px,
                                            segments["shank_px"] * mm_per_px)
            step = max(-MAX_STEP_MM, min(MAX_STEP_MM, delta))
            absolute = (t("rec.saddle_height_abs", lang, before=bike.saddle_height_mm,
                          after=bike.saddle_height_mm + step) if bike and bike.saddle_height_mm else "")
            text += " " + t("rec.saddle_height_mm", lang, total=abs(delta), step=abs(step), absolute=absolute)
        else:
            text += " " + t("rec.need_crank", lang)
        if ext < lo and summary.get("ankle_range", {}).get("median", 0) > targets["ankle_range"][1]:
            text += " " + t("rec.ankle_compensates", lang)
        return [text, t("rec.order", lang)]

    if "kops_mm" in summary and "kops_mm" in targets:
        kops = summary["kops_mm"]["median"]
        klo, khi = targets["kops_mm"][:2]
        if kops > khi + MIN_STEP_MM:
            step = min(MAX_STEP_MM, kops - khi)
            return [t("rec.setback_back", lang, kops=kops, step=step, absolute=_setback(bike, step, lang))]
        if kops < klo - MIN_STEP_MM:
            step = min(MAX_STEP_MM, klo - kops)
            return [t("rec.setback_forward", lang, kops=-kops, step=step, absolute=_setback(bike, -step, lang))]

    torso = summary["torso_angle"]["median"]
    shoulder = summary["shoulder_angle"]["median"]
    elbow = summary["elbow_flexion"]["median"]
    if summary["elbow_flexion"]["std"] > 8:
        tips.append(t("rec.arms_unsteady", lang))
    elif shoulder > targets["shoulder_angle"][1] or elbow < targets["elbow_flexion"][0]:
        tips.append(t("rec.cockpit_long", lang, shoulder=shoulder, elbow=elbow)
                    + _stem(summary, segments, mm_per_px, targets, bike, -1, lang))
    elif shoulder < targets["shoulder_angle"][0] or elbow > targets["elbow_flexion"][1]:
        tips.append(t("rec.cockpit_short", lang, shoulder=shoulder, elbow=elbow)
                    + _stem(summary, segments, mm_per_px, targets, bike, 1, lang))
    if torso < targets["torso_angle"][0] and summary["hip_closed"]["median"] < targets["hip_closed"][0]:
        tips.append(t("rec.torso_flat", lang, torso=torso))
    elif torso > targets["torso_angle"][1]:
        tips.append(t("rec.torso_upright", lang, torso=torso))
    return tips or [t("rec.all_good", lang)]


def _setback(bike, change_mm: float, lang: str) -> str:
    """Moving the saddle back (positive change) increases the setback."""
    if bike and bike.saddle_setback_mm is not None:
        return t("rec.setback_abs", lang, before=bike.saddle_setback_mm,
                 after=bike.saddle_setback_mm + change_mm)
    return ""


def _stem(summary, segments, mm_per_px, targets, bike, direction: int, lang: str) -> str:
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
        return " " + t("rec.stem_shoulder_fine", lang)
    absolute = (t("rec.stem_abs", lang, before=bike.stem_mm, after=bike.stem_mm + step)
                if bike and bike.stem_mm else "")
    return " " + t("rec.stem_mm", lang, total=abs(change), step=abs(step),
                   direction=t("word.longer" if step > 0 else "word.shorter", lang), absolute=absolute)


def corrections(rows: list[dict], summary: dict, segments: dict, mm_per_px: float | None,
                bike=None, tt: bool = False, lang: str = DEFAULT_LANG) -> list[dict]:
    """Adds a short bike change ("fix") and its place in the fitting order
    ("step") to every row outside its target range. Uses the row's own
    range, so it also works on stored results."""
    def mm(key):
        return segments[key] * mm_per_px if mm_per_px and key in segments else None

    thigh, shank, arm = mm("thigh_px"), mm("shank_px"), mm("arm_px")
    saddle_off = any(r["key"] == "knee_extension" and r["status"] != "ok" for r in rows)
    for r in rows:
        r["fix"], r["step"] = None, None
        if r["status"] == "ok":
            continue
        low = r["status"] == "low"
        v, lo, hi, k = r["value"], r["lo"], r["hi"], r["key"]
        outside = (lo - v) if low else (v - hi)
        if outside < (MIN_STEP_MM if r["unit"] == "mm" else MIN_STEP_DEG):
            unit = " mm" if r["unit"] == "mm" else "°"
            r["fix"] = (t("fix.noise", lang, outside=outside, unit=unit) if outside >= 0.5
                        else t("fix.on_edge", lang))
            continue
        if k == "knee_extension":
            text = t("fix.saddle_lower" if low else "fix.saddle_higher", lang)
            if thigh and shank:
                delta = saddle_height_change_mm(v, lo + 2 if low else hi - 2, thigh, shank)
                step = max(-MAX_STEP_MM, min(MAX_STEP_MM, delta))
                text += t("fix.saddle_mm", lang, total=abs(delta), step=abs(step))
                if bike and bike.saddle_height_mm:
                    text += t("fix.abs", lang, before=bike.saddle_height_mm, after=bike.saddle_height_mm + step)
            text += ". " + t("fix.leg_straight" if low else "fix.leg_bent", lang)
        elif k == "knee_flexion_max":
            text = t("fix.knee_top_open" if low else "fix.knee_top_closed", lang)
        elif k == "ankle_range":
            text = t("fix.ankle_low" if low else "fix.ankle_high", lang)
        elif k == "kops_mm":
            step = min(MAX_STEP_MM, outside)
            text = t("fix.kops", lang, step=step, direction=t("word.forward" if low else "word.back", lang),
                     absolute=_setback(bike, -step if low else step, lang), kops=abs(v),
                     position=t("word.behind" if v < 0 else "word.ahead", lang))
        elif k == "hip_closed":
            text = t("fix.hip_closed" if low else "fix.hip_open", lang)
        elif k == "torso_angle":
            if tt:
                text = t("fix.tt_torso_flat" if low else "fix.tt_torso_upright", lang)
            else:
                text = t("fix.torso_flat" if low else "fix.torso_upright", lang, torso=v,
                         absolute=_spacer(bike, 10 if low else -10, lang))
        elif k == "shoulder_angle":
            if tt:
                text = t("fix.tt_pads_forward" if low else "fix.tt_pads_back", lang)
            else:
                text = t("fix.cockpit_short" if low else "fix.cockpit_long", lang) + _stem_mm(v, lo, hi, arm, bike, lang)
        elif k == "elbow_flexion":
            if tt:
                text = t("fix.tt_arms_straight" if low else "fix.tt_arms_bent", lang)
            elif low:
                shoulder = summary.get("shoulder_angle", {}).get("median")
                shoulder_hi = next((x["hi"] for x in rows if x["key"] == "shoulder_angle"), 95)
                fits = shoulder is not None and shoulder <= shoulder_hi
                text = t("fix.arms_straight_hoods" if fits else "fix.arms_straight_stem", lang)
            else:
                text = t("fix.arms_bent", lang)
            if summary.get(k, {}).get("std", 0) > 8:
                text += " " + t("fix.arms_unsteady", lang)
        else:
            continue
        r["step"] = STEP[k]
        if saddle_off and STEP[k] > 1:
            text += " " + t("fix.after_saddle", lang)
        r["fix"] = text
    return rows


def _spacer(bike, change_mm: float, lang: str) -> str:
    if bike and bike.spacer_mm is not None:
        return t("fix.spacer_abs", lang, before=bike.spacer_mm, after=max(0, bike.spacer_mm + change_mm))
    return ""


def _stem_mm(shoulder, lo, hi, arm_mm, bike, lang: str) -> str:
    if not arm_mm:
        return ""
    change = math.radians(min(max(shoulder, lo + 2), hi - 2) - shoulder) * arm_mm
    step = round(change / 10) * 10 or (10 if change > 0 else -10)
    absolute = t("fix.abs", lang, before=bike.stem_mm, after=bike.stem_mm + step) if bike and bike.stem_mm else ""
    return t("fix.stem_mm", lang, total=abs(change), step=abs(step), absolute=absolute)
