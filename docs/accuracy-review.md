# Wie gut ist unser Tracking? Eine nüchterne Bewertung

Stand: 23.10.2026 · Grundlage: Testclip „Radlabor, Road to Roth Folge 24“ (6 s, 1080p, 30 fps) plus Studien zu Profi- und Markerless-Systemen

---

## Kurzfassung

- **Für die Sattelhöhe reicht es, wenn sie deutlich daneben liegt.** Bei groben Fehlern ab etwa 10 mm erkennt die Software sicher, in welche Richtung du ändern musst.
- **Für die Feinabstimmung auf 2 bis 3 mm reicht es noch nicht.** Ein Profisystem wie Retül misst etwa 3- bis 5-mal genauer.
- **Vorher/Nachher-Vergleiche sind deutlich genauer als die absoluten Werte.** Die systematischen Fehler sind bei beiden Messungen ähnlich und heben sich größtenteils auf.
- **Das sichtbare „Driften“ kommt hauptsächlich vom Fuß und Knöchel**, kaum von Hüfte und Oberkörper. Dagegen lässt sich gezielt etwas tun (siehe Abschnitt 5).

---

## 1. Was Profi-Systeme schaffen

| System | Prinzip | Genauigkeit laut Studien |
|---|---|---|
| Vicon (Labor) | Viele Infrarotkameras + reflektierende Marker | Goldstandard, unter 1° |
| Retül Vantage | Aktive LED-Marker auf Knochenpunkten, 3D | Gegen Vicon: Standardfehler ca. 0,4–0,6° bei Kniestreckung/-beugung, 1,2–1,9° bei der Hüfte, ca. 1° am Fußgelenk ([Sensors 2021](https://www.mdpi.com/1424-8220/21/13/4473)). Wiederholbarkeit an verschiedenen Tagen: unter 3°, Knie-vor-Fuß ca. 4 mm ([JSC](https://jsc-journal.com/index.php/JSC/article/download/759/729)) |
| 2D-Markerless (OpenPose) | Ein Video, KI erkennt Gelenke | Knie auf der sichtbaren Seite: im Mittel 1,5° daneben, Streuung ±4°. Hüfte ±5–6°, Fußgelenk ±5°, verdeckte Seite doppelt so schlecht ([PLOS ONE 2023](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0293917)) |
| MediaPipe (unser Modell) | Ein Video, KI | Bei Kniebeugen, Sprüngen und Gehen im Mittel 7,7° Fehler an Hüfte/Knie, im Vergleich gehörte es trotzdem zu den besten Modellen ([SJSP](https://sjsp.aearedo.es/index.php/sjsp/article/download/pose-estimation-models-validated-lower-body-kinematics/219/3811)). Für Radfahren in Seitenansicht gibt es keine direkte Studie, die Bedingungen sind dort aber günstiger (wenig Bewegung, klare Seitenansicht) |

**Einordnung:** Ein Profisystem misst das Knie auf etwa 1° genau. Ohne Marker landet man typischerweise bei 3 bis 5°, vor allem weil die KI den Gelenkmittelpunkt nicht exakt dort setzt, wo ein Fitter seinen Marker klebt.

---

## 2. Was wir im Testclip gemessen haben

Gemessen wurde, wie stark die Punkte von Bild zu Bild zittern und wie stark sich Körpersegmente scheinbar in der Länge ändern. Ein Oberschenkel ist starr, jede Längenänderung ist also Messfehler.

| Punkt | Zittern von Bild zu Bild (RMS) | Bewertung |
|---|---|---|
| Schulter, Hüfte, Ellbogen | 1–2 mm | sehr ruhig |
| Knie | ca. 6 mm, einzelne Ausreißer bis 41 mm | ok |
| Knöchel, Ferse, Zehen | 18–24 mm, Ausreißer bis 236 mm | **Schwachstelle** |

| Segment | Scheinbare Längenschwankung (geglättet) |
|---|---|
| Oberschenkel (Hüfte–Knie) | ±7 mm bei 481 mm (1,4 %) |
| Rumpf (Hüfte–Schulter) | ±8 mm |
| Unterschenkel (Knie–Knöchel) | **±19 mm** bei 450 mm (4 %) |
| Fuß | ±12 mm |

**Winkel-Rauschen pro Bild** (vor Glättung und Mittelung): Knie 2,5°, Fußgelenk 2,2°, Ellbogen 3,4°, Hüfte 0,7°, Oberkörper 0,1°.
**Wiederholbarkeit zwischen Umdrehungen:** Knie unten ±1,7° über 4 Umdrehungen.

**Woher das Driften kommt:**
1. **Bein-Verwechslung:** In 2 Bildern (Bild 138–139) hat die KI kurz den Knöchel des hinteren Beins genommen, ein Sprung von über 30 cm. Das ist ein bekanntes Problem bei Seitenansichten, wenn sich die Beine überkreuzen.
2. **Fuß im Schatten der Kurbel:** Am unteren Totpunkt verdecken Kurbel, Kettenblatt und Schuh den Knöchel. Die KI rät dann mehr.
3. **Unruhige Kamera:** Im Clip bewegt sich das Bild leicht (es ist ein geschnittenes YouTube-Video). Die Hüfte scheint dadurch 5 bis 7 cm zu wandern, was beim echten Fahren unrealistisch ist.
4. **Kurzer Clip, 30 fps, Fahrerin redet und winkt:** All das gibt es bei einer echten Messaufnahme nicht.

---

## 3. Was heißt das in Millimetern am Sattel?

Mit deinen Proportionen gilt grob: **1° Kniewinkel ≈ 2,5 mm Sattelhöhe.**

| Fehlerquelle | Größe | Am Sattel |
|---|---|---|
| Zufälliges Rauschen, gemittelt über 60 Umdrehungen | unter 0,5° | ca. 1 mm, vernachlässigbar |
| Systematischer Versatz der KI-Gelenkpunkte (Literatur) | ca. 2–5° | **ca. 5–12 mm** |
| Kamera nicht genau senkrecht zum Rad (10° verdreht) | ca. 1–2° | ca. 3–5 mm |

**Fazit:** Das Rauschen ist kein Problem, weil wir über viele Umdrehungen mitteln. Das eigentliche Problem ist der **systematische Versatz**: Die KI setzt den Kniepunkt zum Beispiel immer etwas zu weit vorn. Der Zielbereich für das Knie ist 10° breit (30–40°), also etwa 25 mm am Sattel. Liegst du klar daneben, findet die Software das sicher. Liegst du am Rand, kann sie sich in die falsche Richtung irren.

**Vorher/Nachher ist genauer:** Wenn du den Sattel um 5 mm verstellst und neu misst, bleibt der systematische Versatz ungefähr gleich. Die Änderung selbst misst die Software dann auf etwa 1° genau.

---

## 4. Körpergröße, Rahmen, Kurbel: was schon drin ist, was fehlt

**Schon berücksichtigt:**
- **Deine Körperproportionen:** Ober- und Unterschenkellänge werden aus dem Video gemessen. Die mm-Empfehlung für den Sattel ist damit auf deinen Körper gerechnet, nicht auf einen Durchschnittsmenschen.
- **Kurbellänge:** Sie dient als Maßstab. Sie beeinflusst außerdem direkt den Kniewinkel oben und den Hüftwinkel.

**Fehlt noch, ist aber für ein gutes Fitting wichtig:**

| Daten | Wofür |
|---|---|
| Körpergröße, Schrittlänge (Innenbeinlänge) | Plausibilitätscheck des Maßstabs, Startwert Sattelhöhe (Schrittlänge × ca. 0,883 ab Tretlager) |
| Beweglichkeit (Hamstrings, Hüfte), z. B. Sit-and-Reach-Test | Wie flach der Oberkörper sein darf. Wer unbeweglich ist, braucht einen höheren Lenker |
| Rahmen: Stack, Reach, Sitzwinkel, Rahmengröße | Empfehlungen in Bauteilen übersetzen („2 Spacer weniger“, „Vorbau 10 mm kürzer“). Auch für die Frage, ob der Rahmen überhaupt passt |
| Aktuelle Ist-Maße am Rad: Sattelhöhe ab Tretlager, Sattelversatz, Sattel-Lenker-Abstand und -Überhöhung, Vorbau, Spacer | Ausgangspunkt dokumentieren, Position auf ein anderes Rad übertragen |
| Schuh, Cleat-Position, Pedalsystem | Beeinflusst Fußgelenk und effektive Beinlänge |
| Beschwerden, Ziel (Rennen, Langstrecke) | Wahl des Bereichs innerhalb der Zielwerte |

Vorschlag: Ein **Fahrer- und Radprofil**, das einmal ausgefüllt wird und in alle Berechnungen eingeht.

---

## 5. Was wir tun können, um näher an Profi-Systeme zu kommen

Nach Aufwand und Nutzen sortiert:

1. **Bessere Aufnahme (kostet nichts, bringt viel):** 60 fps vom Pixel, Stativ oder fester Platz, Kamera genau quer und auf Höhe des Tretlagers, kurze eng anliegende Hose, helle Socken und Schuhe. Dazu ein heller, gleichmäßiger Hintergrund und 60 Sekunden statt 6.
2. **Bein-Verwechslung automatisch korrigieren:** Ein Gelenk darf nicht 30 cm in einem Bild springen. Solche Bilder werden erkannt und ersetzt, und vertauschte Beine werden zurückgetauscht.
3. **Segmentlängen als Plausibilitätsprüfung:** Ober- und Unterschenkel sind starr. Bilder, in denen sich die Länge um mehr als ein paar Prozent ändert, werden verworfen oder korrigiert.
4. **Besseres Modell für die Beine testen:** RTMPose oder ViTPose. Sie sind in Studien an Knie und Knöchel meist genauer als MediaPipe und lassen sich ebenfalls lokal betreiben.
5. **Optionale Klebepunkte (ca. 0 €, z. B. farbige Sticker an Hüfte, Knie, Knöchel, Ferse, Fußballen):** Damit misst die Software genau dort, wo auch ein Fitter misst, und der systematische Versatz verschwindet weitgehend. Realistisches Ziel: Knie ca. 1–2° genau, also in Richtung Retül. Ohne Punkte bleibt der Standardmodus, mit Punkten gibt es einen „Präzisionsmodus“.
6. **Kalibrierung mit Winkelmesser:** Einmal im Stand das Knie mit einer Winkelmesser-App messen und mit der Software vergleichen. Daraus ergibt sich ein persönlicher Korrekturwert.
7. **Wattmesser (deine SRAM-Kurbel) einbinden:** Immer bei gleicher Leistung messen, damit Vergleiche fair sind.

**Meine Einschätzung:** Mit den Punkten 1 bis 4 reicht die Software für einen soliden Grund-Fit. Grobe Fehler bei Sattelhöhe, Sattelversatz und Oberkörperhaltung findet sie zuverlässig, Vorher/Nachher-Vergleiche sind aussagekräftig. Mit Punkt 5 (Klebepunkte) kommt sie bei der Sattelhöhe in die Nähe eines Ladensystems. Was sie nicht ersetzt: den Blick von vorn auf Knie und Füße, Cleat-Einstellung und Beweglichkeitstests. Das wäre der Frontalkamera-Schritt.
