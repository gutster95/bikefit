"""User-facing texts in German and English.

The analysis stores message keys with parameters; text is rendered only
when shown, so a result can be read in either language.
"""
from __future__ import annotations

LANGS = ("de", "en")
DEFAULT_LANG = "en"

MESSAGES: dict[str, dict[str, str]] = {
    # metric labels
    "metric.knee_extension": {"de": "Kniebeugung unten (max. Streckung)", "en": "Knee flexion at bottom (max. extension)"},
    "metric.knee_flexion_max": {"de": "Kniebeugung oben", "en": "Knee flexion at top"},
    "metric.hip_closed": {"de": "Hüftwinkel geschlossen (oben)", "en": "Closed hip angle (top)"},
    "metric.ankle_range": {"de": "Bewegungsumfang Fußgelenk", "en": "Ankle range of motion"},
    "metric.torso_angle": {"de": "Oberkörper zur Horizontalen", "en": "Torso angle to horizontal"},
    "metric.shoulder_angle": {"de": "Schulterwinkel", "en": "Shoulder angle"},
    "metric.elbow_flexion": {"de": "Ellbogenbeugung", "en": "Elbow flexion"},
    "metric.kops_mm": {"de": "Knie vor Pedalachse bei 3 Uhr", "en": "Knee over pedal spindle at 3 o'clock"},
    "metric.hip_rock_mm": {"de": "Hüftbewegung vertikal", "en": "Vertical hip movement"},

    # recommendations (one change at a time)
    "rec.all_good": {"de": "Alle gemessenen Werte liegen im Zielbereich. Keine Änderung nötig.",
                     "en": "All measured values are within their target range. No change needed."},
    "rec.saddle_height": {"de": "Sattelhöhe {direction}: Knie unten {value:.0f}° gebeugt, Ziel {lo:.0f}–{hi:.0f}°.",
                          "en": "{direction} the saddle: knee bent {value:.0f}° at the bottom, target {lo:.0f}–{hi:.0f}°."},
    "rec.dir.lower": {"de": "senken", "en": "Lower"},
    "rec.dir.raise": {"de": "anheben", "en": "Raise"},
    "rec.saddle_height_mm": {"de": "Rechnerisch ca. {total:.0f} mm, in diesem Schritt {step:.0f} mm{absolute}, dann neu messen.",
                             "en": "Calculated about {total:.0f} mm, {step:.0f} mm in this step{absolute}, then measure again."},
    "rec.saddle_height_abs": {"de": " (Sattelhöhe {before:.0f} → {after:.0f} mm)", "en": " (saddle height {before:.0f} → {after:.0f} mm)"},
    "rec.need_crank": {"de": "Für eine Angabe in mm die Kurbellänge eintragen.", "en": "Enter the crank length to get millimetres."},
    "rec.ankle_compensates": {"de": "Das große Fußgelenk-Spiel bestätigt: Du gleichst eine zu hohe Sattelposition mit dem Fuß aus.",
                              "en": "The large ankle movement confirms it: your foot compensates for a saddle that is too high."},
    "rec.order": {"de": "Erst die Sattelhöhe anpassen und neu messen, danach Sattelversatz und Cockpit.",
                  "en": "Adjust the saddle height first and measure again, then setback and cockpit."},
    "rec.setback_back": {"de": "Sattel etwas nach hinten: Knie {kops:.0f} mm vor der Pedalachse bei 3 Uhr. Zuerst {step:.0f} mm{absolute}, Sattelhöhe danach prüfen.",
                         "en": "Move the saddle back a little: knee {kops:.0f} mm ahead of the pedal spindle at 3 o'clock. First {step:.0f} mm{absolute}, then check the saddle height."},
    "rec.setback_forward": {"de": "Sattel etwas nach vorn: Knie {kops:.0f} mm hinter der Pedalachse bei 3 Uhr. Zuerst {step:.0f} mm{absolute}, Sattelhöhe danach prüfen.",
                            "en": "Move the saddle forward a little: knee {kops:.0f} mm behind the pedal spindle at 3 o'clock. First {step:.0f} mm{absolute}, then check the saddle height."},
    "rec.setback_abs": {"de": " (Versatz {before:.0f} → {after:.0f} mm)", "en": " (setback {before:.0f} → {after:.0f} mm)"},
    "rec.arms_unsteady": {"de": "Keine Cockpit-Empfehlung: Armwinkel zu unruhig. Hände während der Aufnahme ruhig am Lenker lassen.",
                          "en": "No cockpit advice: arm angles too unsteady. Keep your hands still on the bar while filming."},
    "rec.cockpit_long": {"de": "Cockpit eher zu lang: Schulterwinkel {shoulder:.0f}°, Ellbogen {elbow:.0f}° gebeugt. Kürzerer Vorbau oder Lenker näher heranholen.",
                         "en": "Cockpit rather too long: shoulder angle {shoulder:.0f}°, elbows bent {elbow:.0f}°. Shorter stem or bring the bar closer."},
    "rec.cockpit_short": {"de": "Cockpit eher zu kurz: Schulterwinkel {shoulder:.0f}°, Ellbogen {elbow:.0f}° gebeugt. Längerer Vorbau möglich.",
                          "en": "Cockpit rather too short: shoulder angle {shoulder:.0f}°, elbows bent {elbow:.0f}°. A longer stem is possible."},
    "rec.stem_shoulder_fine": {"de": "Der Schulterwinkel passt aber schon, also eher kleine Korrektur: Bremshebel etwas nach oben/hinten drehen oder Arme bewusst leicht beugen.",
                               "en": "The shoulder angle is already fine, so make a small correction: rotate the brake hoods slightly up/back or bend your arms a little on purpose."},
    "rec.stem_mm": {"de": "Rechnerisch ca. {total:.0f} mm, also Vorbau {step:.0f} mm {direction}{absolute}.",
                    "en": "Calculated about {total:.0f} mm, so a stem {step:.0f} mm {direction}{absolute}."},
    "rec.stem_abs": {"de": " ({before:.0f} → {after:.0f} mm)", "en": " ({before:.0f} → {after:.0f} mm)"},
    "word.longer": {"de": "länger", "en": "longer"},
    "word.shorter": {"de": "kürzer", "en": "shorter"},
    "rec.torso_flat": {"de": "Oberkörper sehr flach ({torso:.0f}°) und Hüfte oben eng: Lenker etwas höher (Spacer).",
                       "en": "Torso very flat ({torso:.0f}°) and hip closed at the top: raise the bar a little (spacers)."},
    "rec.torso_upright": {"de": "Oberkörper recht aufrecht ({torso:.0f}°): für mehr Aero kann der Lenker tiefer, wenn es bequem bleibt.",
                          "en": "Torso fairly upright ({torso:.0f}°): for more aero the bar can go lower, as long as it stays comfortable."},

    # per-metric fixes
    "fix.noise": {"de": "Nur {outside:.0f}{unit} außerhalb, das liegt in der Messgenauigkeit. Nichts ändern, beim nächsten Video wieder anschauen.",
                  "en": "Only {outside:.0f}{unit} outside, which is within the measurement accuracy. Change nothing and check again in the next video."},
    "fix.on_edge": {"de": "Liegt praktisch auf der Grenze. Nichts ändern.", "en": "Practically on the limit. Change nothing."},
    "fix.saddle_lower": {"de": "Sattel tiefer stellen", "en": "Lower the saddle"},
    "fix.saddle_higher": {"de": "Sattel höher stellen", "en": "Raise the saddle"},
    "fix.saddle_mm": {"de": ": rechnerisch {total:.0f} mm, jetzt {step:.0f} mm", "en": ": calculated {total:.0f} mm, {step:.0f} mm now"},
    "fix.abs": {"de": " ({before:.0f} → {after:.0f} mm)", "en": " ({before:.0f} → {after:.0f} mm)"},
    "fix.leg_straight": {"de": "Das Bein ist unten fast gestreckt.", "en": "The leg is almost straight at the bottom."},
    "fix.leg_bent": {"de": "Das Bein bleibt unten zu stark gebeugt.", "en": "The leg stays too bent at the bottom."},
    "fix.knee_top_open": {"de": "Knie oben weit offen, meist Folge eines hohen Sattels. Erst die Sattelhöhe prüfen.",
                          "en": "Knee wide open at the top, usually from a high saddle. Check the saddle height first."},
    "fix.knee_top_closed": {"de": "Knie oben stark gebeugt: Sattel etwas höher oder kürzere Kurbel (2,5 bis 5 mm kürzer) entlastet das Knie.",
                            "en": "Knee strongly bent at the top: a slightly higher saddle or shorter cranks (2.5 to 5 mm shorter) relieve the knee."},
    "fix.ankle_low": {"de": "Fuß arbeitet wenig. Unkritisch, eventuell Sattel 2 bis 3 mm höher und bewusst rund treten.",
                      "en": "Little ankle movement. Not critical; maybe raise the saddle 2 to 3 mm and pedal in smooth circles."},
    "fix.ankle_high": {"de": "Fuß kippt stark ab, oft Ausgleich für einen zu hohen Sattel: Sattel 3 bis 5 mm tiefer oder Cleats 2 bis 3 mm weiter nach hinten.",
                       "en": "Foot drops a lot, often compensating for a saddle that is too high: lower the saddle 3 to 5 mm or move the cleats 2 to 3 mm back."},
    "fix.kops": {"de": "Sattel {step:.0f} mm nach {direction} schieben{absolute}. Das Knie steht {kops:.0f} mm {position} der Pedalachse. Danach Sattelhöhe prüfen, beim Verschieben ändert sie sich leicht.",
                 "en": "Slide the saddle {step:.0f} mm {direction}{absolute}. The knee is {kops:.0f} mm {position} the pedal spindle. Check the saddle height afterwards, it changes slightly."},
    "word.forward": {"de": "vorn", "en": "forward"},
    "word.back": {"de": "hinten", "en": "back"},
    "word.behind": {"de": "hinter", "en": "behind"},
    "word.ahead": {"de": "vor", "en": "ahead of"},
    "fix.hip_closed": {"de": "Hüfte oben zu eng: Lenker höher (10 mm Spacer unter den Vorbau) oder kürzerer Vorbau. Kürzere Kurbeln öffnen die Hüfte ebenfalls.",
                       "en": "Hip too closed at the top: raise the bar (10 mm spacer under the stem) or use a shorter stem. Shorter cranks also open the hip."},
    "fix.hip_open": {"de": "Hüfte bleibt offen: Lenker darf tiefer (10 mm Spacer über den Vorbau), wenn du sportlicher sitzen willst.",
                     "en": "Hip stays open: the bar can go lower (move a 10 mm spacer above the stem) if you want a sportier position."},
    "fix.tt_torso_flat": {"de": "Sehr flach: Auflegerpads 10 mm höher.", "en": "Very flat: raise the aero pads 10 mm."},
    "fix.tt_torso_upright": {"de": "Recht aufrecht: Auflegerpads 10 mm tiefer.", "en": "Fairly upright: lower the aero pads 10 mm."},
    "fix.torso_flat": {"de": "Oberkörper sehr flach ({torso:.0f}°): Lenker höher, 10 mm Spacer unter den Vorbau {absolute}oder Vorbau mit mehr Steigung.",
                       "en": "Torso very flat ({torso:.0f}°): raise the bar, 10 mm spacer under the stem {absolute}or a stem with more rise."},
    "fix.torso_upright": {"de": "Oberkörper aufrecht ({torso:.0f}°): für mehr Aero Lenker tiefer, 10 mm Spacer über den Vorbau {absolute}. Nur wenn es bequem bleibt.",
                          "en": "Torso upright ({torso:.0f}°): for more aero lower the bar, move a 10 mm spacer above the stem {absolute}. Only if it stays comfortable."},
    "fix.spacer_abs": {"de": "({before:.0f} → {after:.0f} mm) ", "en": "({before:.0f} → {after:.0f} mm) "},
    "fix.tt_pads_forward": {"de": "Pads weiter nach vorn.", "en": "Move the pads forward."},
    "fix.tt_pads_back": {"de": "Pads weiter nach hinten.", "en": "Move the pads back."},
    "fix.cockpit_short": {"de": "Cockpit zu kurz: Vorbau länger.", "en": "Cockpit too short: longer stem."},
    "fix.cockpit_long": {"de": "Cockpit zu lang: Vorbau kürzer.", "en": "Cockpit too long: shorter stem."},
    "fix.stem_mm": {"de": " Rechnerisch {total:.0f} mm, also {step:.0f} mm{absolute}.", "en": " Calculated {total:.0f} mm, so {step:.0f} mm{absolute}."},
    "fix.tt_arms_straight": {"de": "Arme zu gestreckt: Pads näher zum Körper.", "en": "Arms too straight: move the pads closer to the body."},
    "fix.tt_arms_bent": {"de": "Arme zu stark gebeugt: Pads weiter nach vorn.", "en": "Arms bent too much: move the pads forward."},
    "fix.arms_straight_hoods": {"de": "Arme fast gestreckt, der Schulterwinkel passt aber. Darum nicht den Vorbau tauschen: Bremsgriffe 5 bis 10 mm höher bzw. näher drehen und die Ellbogen bewusst locker beugen.",
                                "en": "Arms almost straight, but the shoulder angle fits. So don't swap the stem: rotate the brake hoods 5 to 10 mm higher or closer and keep your elbows loosely bent."},
    "fix.arms_straight_stem": {"de": "Arme fast gestreckt: Lenker näher heran (Vorbau 10 mm kürzer) oder etwas höher. Ellbogen locker beugen, das dämpft Stöße.",
                               "en": "Arms almost straight: bring the bar closer (stem 10 mm shorter) or slightly higher. Keep your elbows loosely bent, it absorbs bumps."},
    "fix.arms_bent": {"de": "Arme stark gebeugt: Cockpit eher zu kurz oder zu hoch, Vorbau 10 mm länger oder Lenker tiefer.",
                      "en": "Arms strongly bent: cockpit rather too short or too high, stem 10 mm longer or lower bar."},
    "fix.arms_unsteady": {"de": "Achtung, der Armwinkel schwankt stark, bitte Hände ruhig halten.",
                          "en": "Note: the arm angle varies a lot, please keep your hands still."},
    "fix.after_saddle": {"de": "Erst nach der Sattelhöhe ändern.", "en": "Change this only after the saddle height."},

    # measurement quality warnings
    "warn.coverage": {"de": "Person nur in {coverage:.0%} der Bilder erkannt (Licht, Kleidung, Bildausschnitt prüfen).",
                      "en": "Rider detected in only {coverage:.0%} of frames (check light, clothing and framing)."},
    "warn.crank_fit": {"de": "Pedalkreis unsauber erkannt, mm-Werte und KOPS sind unsicher.",
                       "en": "Pedal circle detected poorly; millimetre values and KOPS are uncertain."},
    "warn.knee_std": {"de": "Kniewinkel schwankt stark zwischen den Umdrehungen (Tracking-Rauschen oder unruhiges Treten).",
                      "en": "Knee angle varies a lot between revolutions (tracking noise or uneven pedalling)."},
    "warn.elbow_std": {"de": "Armwinkel schwanken stark (Hände bewegt oder Griffposition gewechselt). Arm-Werte mit Vorsicht lesen.",
                       "en": "Arm angles vary a lot (hands moved or grip changed). Read the arm values with care."},
    "warn.few_cycles": {"de": "Nur {cycles} Umdrehungen. Für belastbare Werte mindestens 30 Sekunden aufnehmen.",
                        "en": "Only {cycles} revolutions. Record at least 30 seconds for reliable values."},
    "warn.thigh": {"de": "Oberschenkellänge {thigh:.0f} mm wirkt unplausibel, Maßstab prüfen.",
                   "en": "Thigh length {thigh:.0f} mm looks implausible, check the scale."},
    "warn.camera_moved": {"de": "Das Bild bewegt sich (Kamera geschwenkt oder gezoomt?). Kamera muss fest stehen, sonst sind Pedalkreis, mm-Werte und Hüftbewegung falsch.",
                          "en": "The image moves (camera panned or zoomed?). The camera must stay fixed, otherwise pedal circle, millimetre values and hip movement are wrong."},

    # notes
    "note.leg_length": {"de": "Beinlänge im Video ({measured:.0f} mm) passt schlecht zur Körpergröße (erwartet ca. {expected:.0f} mm). Kurbellänge oder Kameraposition prüfen.",
                        "en": "Leg length in the video ({measured:.0f} mm) does not match your height well (expected about {expected:.0f} mm). Check the crank length or camera position."},
    "note.lemond": {"de": "Startwert Sattelhöhe nach LeMond-Formel: {lemond:.0f} mm{current}. Nur grober Richtwert, die Videomessung hat Vorrang.",
                    "en": "Starting saddle height by the LeMond formula: {lemond:.0f} mm{current}. Only a rough guide; the video measurement takes priority."},
    "note.lemond_current": {"de": " (aktuell {current:.0f} mm, Differenz {diff:+.0f} mm)", "en": " (currently {current:.0f} mm, difference {diff:+.0f} mm)"},
    "note.cleaned": {"de": "Automatisch korrigiert: {leg_swaps} Bilder mit vertauschten Beinen, {jumps} Sprünge, {bad_segments} unplausible Segmentlängen.",
                     "en": "Corrected automatically: {leg_swaps} frames with swapped legs, {jumps} jumps, {bad_segments} implausible segment lengths."},

    # progress and errors
    "progress.queued": {"de": "In der Warteschlange", "en": "Queued"},
    "progress.running": {"de": "Läuft", "en": "Running"},
    "progress.detecting": {"de": "Erkenne Körperpunkte", "en": "Detecting body points"},
    "progress.computing": {"de": "Berechne Winkel und Empfehlungen", "en": "Computing angles and advice"},
    "progress.rendering": {"de": "Erstelle Video mit Skelett", "en": "Rendering video with skeleton"},
    "progress.done": {"de": "Fertig", "en": "Done"},
    "error.video_unreadable": {"de": "Video nicht lesbar.", "en": "Video cannot be read."},
    "error.no_person": {"de": "Im Video wurde keine Person erkannt.", "en": "No person was detected in the video."},
    "error.too_short": {"de": "Aufnahme zu kurz, um Kurbelumdrehungen zu erkennen.", "en": "Recording too short to detect crank revolutions."},
    "error.few_cycles": {"de": "Nur {cycles} Kurbelumdrehungen erkannt. Bitte mindestens 30 Sekunden gleichmäßig treten und filmen.",
                         "en": "Only {cycles} crank revolutions detected. Please pedal steadily and film for at least 30 seconds."},
    "api.unknown_bike": {"de": "Unbekanntes Rad", "en": "Unknown bike"},
    "api.no_session": {"de": "Fitting nicht gefunden", "en": "Fitting not found"},
    "api.still_running": {"de": "Die Auswertung läuft noch. Bitte warten, bis sie fertig ist.",
                          "en": "The analysis is still running. Please wait until it has finished."},
    "error.unexpected": {"de": "Unerwarteter Fehler: {detail}", "en": "Unexpected error: {detail}"},

    # video overlay (ASCII only, OpenCV has no umlauts)
    "overlay.knee": {"de": "Knie {v:5.1f} deg gebeugt", "en": "Knee {v:5.1f} deg flexed"},
    "overlay.hip": {"de": "Huefte {v:5.1f} deg", "en": "Hip {v:5.1f} deg"},
    "overlay.torso": {"de": "Oberkoerper {v:5.1f} deg", "en": "Torso {v:5.1f} deg"},
    "overlay.cycle": {"de": "Umdrehung {n}: Knie unten {v:.1f} deg", "en": "Revolution {n}: knee at bottom {v:.1f} deg"},

    # text report (command line)
    "report.title": {"de": "BIKEFIT ANALYSE", "en": "BIKEFIT ANALYSIS"},
    "report.side": {"de": "Analysierte Körperseite: {side}   Blickrichtung im Bild: {facing}", "en": "Analysed side: {side}   Facing in image: {facing}"},
    "word.left": {"de": "links", "en": "left"},
    "word.right": {"de": "rechts", "en": "right"},
    "report.cycles": {"de": "Kurbelumdrehungen: {cycles}   Trittfrequenz: {cadence:.0f} U/min", "en": "Crank revolutions: {cycles}   Cadence: {cadence:.0f} rpm"},
    "report.window": {"de": "Ausgewertet: Sekunde {start:.1f} bis {end:.1f} des Videos", "en": "Analysed: second {start:.1f} to {end:.1f} of the video"},
    "report.scale": {"de": "Maßstab aus Kurbellänge: {scale:.2f} mm pro Pixel   Oberschenkel {thigh:.0f} mm, Unterschenkel {shank:.0f} mm",
                     "en": "Scale from crank length: {scale:.2f} mm per pixel   thigh {thigh:.0f} mm, shank {shank:.0f} mm"},
    "report.header": {"de": "Messwert", "en": "Metric"},
    "report.value": {"de": "Wert", "en": "Value"},
    "report.target": {"de": "Ziel", "en": "Target"},
    "report.info_only": {"de": "(nur Info)", "en": "(info only)"},
    "report.advice": {"de": "EMPFEHLUNG", "en": "ADVICE"},
    "report.notes": {"de": "INFO", "en": "INFO"},
    "report.warnings": {"de": "HINWEISE ZUR MESSQUALITÄT", "en": "MEASUREMENT QUALITY"},
    "report.footer": {"de": "Werte sind Mediane über alle Umdrehungen, ± ist die Streuung.\nDie Software ersetzt keine medizinische Beratung.",
                      "en": "Values are medians over all revolutions, ± is the spread.\nThis software does not replace medical advice."},
    "status.ok": {"de": "ok", "en": "ok"},
    "status.low": {"de": "zu niedrig", "en": "too low"},
    "status.high": {"de": "zu hoch", "en": "too high"},
}


def lang_or_default(lang: str | None) -> str:
    return lang if lang in LANGS else DEFAULT_LANG


def t(key: str, lang: str = DEFAULT_LANG, **params) -> str:
    texts = MESSAGES[key]
    return texts.get(lang, texts[DEFAULT_LANG]).format(**params)


def render(message: dict, lang: str) -> str:
    """message: {"key": ..., "params": {...}} or a legacy {"text": ...}."""
    if "text" in message:
        return message["text"]
    return t(message["key"], lang, **message.get("params", {}))


class AnalysisError(Exception):
    """An error the rider can act on, shown in their language."""

    def __init__(self, key: str, **params):
        super().__init__(t(key, DEFAULT_LANG, **params))
        self.key, self.params = key, params
