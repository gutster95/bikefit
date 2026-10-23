# Bikefit Software – Konzept v0.1

Stand: 23.10.2026 · Status: Konzeptphase, noch kein Code

---

## 1. Ziel in einem Satz

Eine günstige Software, die dich auf dem Rad auf der Rolle per Kamera filmt, deine Gelenke automatisch erkennt, die wichtigen Winkel über viele Kurbelumdrehungen misst und daraus konkrete Empfehlungen ableitet, zum Beispiel „Sattel 6 mm höher, 5 mm nach vorn“.

---

## 2. Wie ein professionelles Bike-Fitting abläuft

Ein Fitter im Laden (Retül, Shimano Bike Fitting, Guru, Trek Precision Fit usw.) arbeitet grob in diesen Schritten. Die Software sollte denselben Ablauf abbilden, weil die Kamera nur einen Teil davon abdeckt.

1. **Anamnese:** Ziele (Rennen, Langstrecke, Triathlon, Komfort), Beschwerden (Knie vorne oder hinten, Taubheit in Händen oder Füßen, Nacken, unterer Rücken, Sitzbeschwerden), Verletzungen, Trainingsumfang.
2. **Körpercheck:** Beweglichkeit (Hamstrings, Hüftbeuger), Beinlängendifferenz, Fußstellung (Senk- oder Hohlfuß, Varus/Valgus), Sitzknochenabstand.
3. **Ist-Aufnahme:** Rad vermessen (Sattelhöhe, Sattelversatz, Reach und Drop zum Lenker, Kurbellänge, Cleat-Position).
4. **Dynamische Analyse:** Fahrer fährt 3 bis 5 Minuten bei moderater Last und 80 bis 95 U/min, Kamera oder Marker zeichnen auf. Gemessen wird über viele Umdrehungen, nicht an einem Standbild.
5. **Anpassungen in fester Reihenfolge**, weil jede Änderung die folgenden beeinflusst:
   1. Schuhplatten (Cleats): Vorne/hinten, Rotation, Q-Faktor
   2. Sattelhöhe
   3. Sattelversatz (vor/zurück) und Neigung
   4. Cockpit: Reach (Vorbaulänge), Lenkerhöhe (Spacer, Vorbauwinkel), Hebelposition
6. **Nachmessung** nach jeder Änderung, bis die Werte im Zielbereich sind.
7. **Bericht:** Vorher/Nachher-Werte und die Koordinaten der neuen Position, damit man sie auf ein anderes Rad übertragen kann.

**Wichtig für uns:** Schritt 5.1 (Cleats) und der Körpercheck lassen sich per Seitenkamera kaum lösen. Die Kamera ist stark bei Sattelhöhe, Sattelversatz und Oberkörperposition. Für Knie-Tracking und Cleats braucht es eine **Frontalansicht**.

---

## 3. Körperpunkte (Tracking-Punkte)

Profi-Systeme kleben Marker auf knöcherne Landmarken. Wir nutzen dieselben Punkte, erkannt durch ein Pose-Modell, optional unterstützt durch farbige Klebepunkte.

| Punkt | Landmarke | Wofür |
|---|---|---|
| Handgelenk | Processus styloideus ulnae | Ellbogen-, Reach-Bewertung |
| Ellbogen | Epicondylus lateralis | Ellbogenwinkel |
| Schulter | Acromion | Schulter-, Oberkörperwinkel |
| Hüfte | Trochanter major | Hüft-, Knie-, Oberkörperwinkel |
| Knie | Epicondylus lateralis femoris | Kniewinkel |
| Sprunggelenk | Malleolus lateralis | Knie-, Fußgelenkwinkel |
| Ferse | Calcaneus | Fußgelenkwinkel |
| Fußballen | 5. Mittelfußköpfchen | Fußwinkel, Cleat-Position |
| Frontal: Kniemitte | Patella | Knie-Tracking seitlich |
| Frontal: Hüfte beidseitig | Spina iliaca | Becken-Kippen und -Wippen |

Zusätzlich am **Rad**: Tretlagermitte, Pedalachse, Sattelspitze/-mitte, Lenkermitte. Die Tretlagermitte ist der Referenzpunkt für alle Rad-Koordinaten (Stack/Reach-Logik).

---

## 4. Messwerte und Zielbereiche (dynamisch, Seitenansicht)

Werte als **Beugung** angegeben (0° = gestreckt), sofern nicht anders notiert. Die Bereiche sind gängige Richtwerte aus Fitting-Praxis und Literatur und sollen in der Software **konfigurierbar** sein, denn Fitting-Schulen weichen leicht voneinander ab. Dynamisch gemessene Kniewinkel liegen typischerweise etwa 5 bis 10° anders als statisch (Goniometer, Pedal unten im Stand), deshalb messen wir dynamisch und vergleichen nur mit dynamischen Zielwerten.

| Messwert | Definition | Richtwert Rennrad | Hauptstellschraube |
|---|---|---|---|
| Kniebeugung unten (BDC) | Minimale Beugung pro Umdrehung | ca. 30–40° | Sattelhöhe |
| Kniebeugung oben (TDC) | Maximale Beugung | ca. 105–115° | Sattelhöhe, Kurbellänge |
| Hüftwinkel geschlossen | Oberkörper zu Oberschenkel am oberen Totpunkt | Rennrad ≥ ca. 45°, Zeitfahren tiefer | Lenkerhöhe, Sattelversatz, Kurbellänge |
| Fußgelenk-Bewegung | Spanne des Winkels Knie–Knöchel–Fußballen | ca. 15–30° Spanne | Sattelhöhe (zu hoch = „Zehenspitzenfahren“), Cleats |
| Knie über Pedalachse (KOPS) | Horizontaler Abstand Knie zu Pedalachse bei Kurbel waagerecht vorn | grober Startwert, ca. 0 ± 2 cm | Sattelversatz |
| Oberkörperwinkel | Linie Hüfte–Schulter zur Horizontalen | Sportlich 35–45°, Endurance 45–55°, TT 10–25° | Lenkerhöhe, Reach |
| Schulterwinkel | Oberkörper zu Oberarm | ca. 80–90° | Reach |
| Ellbogenbeugung | | ca. 15–30° | Reach, Lenkerhöhe |
| Hüftwippen | Vertikale Bewegung der Hüfte pro Umdrehung | möglichst klein, Richtwert < 1–2 cm | Sattel zu hoch, Beinlängendifferenz |

**Frontalansicht:**

| Messwert | Bedeutung |
|---|---|
| Knie-Tracking | Seitliche Bahn des Knies über die Umdrehung. Eine Acht oder starkes Einknicken nach innen deutet auf Cleat-, Fußbett- oder Q-Faktor-Thema hin. |
| Links/rechts-Symmetrie | Unterschiede im Kniewinkel unten zwischen den Beinen, Hinweis auf Beinlängendifferenz oder Beckenschiefstand. |
| Becken-Kippen | Seitliches Absinken der Hüfte, Sattel zu hoch oder Asymmetrie. |

---

## 5. Wie Empfehlungen entstehen

Kein „Geheim-Algorithmus“, sondern drei Bausteine, die man nachvollziehen kann:

### 5.1 Regelwerk mit fester Reihenfolge

Für jede Messgröße gibt es Zielbereich, Abweichung und eine Stellschraube. Die Regeln werden in der Reihenfolge Sattelhöhe → Sattelversatz → Cockpit abgearbeitet. Es wird immer nur **eine Änderung zur Zeit** empfohlen, danach wird neu gemessen. So vermeidet man, dass sich Änderungen gegenseitig verfälschen.

Beispiele:
- Knie unten mit 25° Beugung zu gestreckt **und** großes Fußgelenk-Strecken **und** Hüftwippen → Sattel zu hoch.
- Knie unten 45° → Sattel zu tief.
- Knie deutlich vor der Pedalachse und Hüftwinkel sehr eng → Sattel zu weit vorn.
- Oberkörper flacher als das Profil erlaubt und Schulterwinkel > 95° → Reach zu lang.

### 5.2 Geometrische Berechnung des Betrags

Statt grober Daumenregeln („1 cm ≈ x Grad“) rechnen wir mit den gemessenen Segmentlängen. Oberschenkel (Hüfte–Knie) und Unterschenkel (Knie–Knöchel) sind bekannt, daraus ergibt sich über den Kosinussatz der Abstand Hüfte–Knöchel beim Ziel-Kniewinkel. Die Differenz zum Ist-Abstand, projiziert auf die Sitzrohrrichtung, ist die Sattelhöhenänderung in mm. Gleiches Prinzip für Versatz und Reach. Dafür brauchen wir einen **Maßstab in mm**, siehe Abschnitt 7.

### 5.3 Profile und Beschwerden

Die Zielbereiche verschieben sich je nach Profil (Komfort, Sport, Race, Triathlon, Gravel/MTB) und Beschwerden aus der Anamnese. Beispiel: Schmerzen vorne am Knie → eher Richtung oberes Ende der Sattelhöhe und Sattel nicht zu weit vorn. Schmerzen hinten am Knie → eher etwas tiefer.

**Haftung:** Die Software gibt Empfehlungen, keine medizinische Diagnose. Bei Schmerzen weist sie auf Physio oder Fachperson hin.

---

## 6. Bestehende Tools (Marktüberblick)

| Tool | Prinzip | Grobe Kosten | Bemerkung |
|---|---|---|---|
| Retül (Specialized) | 3D-Motion-Capture mit aktiven LED-Markern | System im fünfstelligen Bereich, Fitting im Laden ca. 200–350 € | Goldstandard im Handel |
| Shimano Bike Fitting (ehem. bikefitting.com) | 3D-Marker, Fit-Bike | Händlersystem, teuer | Starke Datenbank und Fitbike |
| Guru, Purely Custom, Trek Precision Fit | Verstellbares Fit-Bike plus Kamera oder Marker | Händlersystem | |
| Velogicfit | Tiefenkamera (Kinect) ohne Marker | Händler-Abo | Zeigt, dass Tiefenkameras funktionieren |
| MyVeloFit | KI-Pose-Erkennung aus Handyvideo, online | Für Endkunden einige 10 € pro Fit oder Abo | Nächster Konkurrent zu unserer Idee |
| Bike Fast Fit | Handy-App, Video plus manuell gesetzte Punkte | Wenige Euro | Günstig, aber viel Handarbeit |

Preise sind Richtwerte aus Händler- und Anbieterseiten und ändern sich. **Unsere Lücke:** lokal laufend (keine Cloud, keine Abo-Kosten), echtes Live-Feedback während des Fahrens, Frontal- plus Seitenansicht, und die Empfehlung in mm statt nur „zu hoch“.

---

## 7. Kamera, Entfernung und Tiefe

Das ist der knifflige Teil deiner Idee, deshalb ausführlicher.

### 7.1 Die gute Nachricht

Für die wichtigsten Werte, die Gelenkwinkel in der Seitenansicht, brauchen wir **keine echte Tiefe**. Winkel sind unabhängig vom Maßstab. Entscheidend ist, dass die Kamera **senkrecht zur Fahrebene** steht und auf **Höhe der Hüfte bis Tretlager**. Ein Laptop auf der anderen Seite des Raumes ist dafür sogar gut: Aus 3 bis 4 m Abstand ist die perspektivische Verzerrung kleiner als aus 1 m.

### 7.2 Wofür wir Entfernung oder Maßstab doch brauchen

- **Empfehlungen in mm** (Sattel 6 mm hoch) brauchen Pixel → mm.
- **Kamera-Ausrichtung prüfen:** Steht die Kamera schräg, werden Winkel verfälscht. Die Software soll das erkennen und warnen.
- **Bildausschnitt:** Der ganze Fahrer mit Rad muss ins Bild, aber so groß wie möglich.

### 7.3 Optionen

| Option | Hardware | Genauigkeit | Kosten | Bewertung |
|---|---|---|---|---|
| A. 2D + Kalibriermarker | Eine Kamera plus ausgedruckter ArUco/ChArUco-Marker am Rad oder an der Wand auf Höhe der Fahrebene | Winkel gut, mm ausreichend | ca. 0 € | **Empfehlung für Phase 1** |
| B. 2D + bekannte Radmaße | Laufraddurchmesser oder Kurbellänge als Maßstab, automatisch erkannt | Etwas schlechter als A | 0 € | Fallback ohne Marker |
| C. 2 Kameras (Seite + Front) | Laptop-Webcam plus Handy als zweite Kamera | Zusätzlich Knie-Tracking und Symmetrie | 0 € wenn Handy vorhanden | **Phase 2** |
| D. Tiefenkamera | Intel RealSense D455, Orbbec Femto oder OAK-D | Echte 3D-Punkte, Abstand direkt messbar | ca. 300–500 € | Optional, Phase 3 |
| E. iPhone mit LiDAR | iPhone Pro als Kamera | 3D bis ca. 5 m | vorhanden oder nicht | Interessant, aber nur Apple |
| F. 3D aus einer Kamera „schätzen“ | KI-Modell, das 3D aus 2D rät | Unzuverlässig für Fitting-Genauigkeit | 0 € | Nur Zusatzinfo |

### 7.4 Kamera-Qualität

Bei 90 U/min dreht die Kurbel 1,5-mal pro Sekunde. Mit **30 fps** gibt das etwa 20 Bilder pro Umdrehung, das reicht knapp, aber Bewegungsunschärfe am Fuß stört. **60 fps oder mehr** ist deutlich besser. Viele Laptop-Webcams liefern nur 30 fps bei schlechtem Licht, ein Handy als Kamera (per App oder Video-Upload) ist oft besser. Gutes, gleichmäßiges Licht und eng anliegende Kleidung verbessern die Erkennung massiv.

### 7.5 Einrichtungs-Assistent

Damit „Laptop drüben, Rad hier“ klappt, braucht die Software einen geführten Aufbau:
1. Live-Bild mit Overlay: „Ganzer Körper im Bild? Rad parallel?“
2. Marker erkennen → Abstand, Neigung der Kamera und Maßstab berechnen.
3. Ampel: grün, wenn Kamera innerhalb weniger Grad senkrecht steht, sonst Hinweis „Laptop etwas nach links drehen“.
4. Testaufnahme 10 Sekunden → Erkennungsqualität pro Gelenk anzeigen.

---

## 8. Feature-Set

### MVP (Phase 1) – „Seitenansicht, Sattel richtig einstellen“
- Kamera-Eingang: Webcam live **oder** Video-Datei vom Handy
- Einrichtungs-Assistent mit Kalibriermarker
- Pose-Erkennung der Körperpunkte aus Abschnitt 3 (eine Körperseite)
- Glättung der Punkte und automatische Erkennung jeder Kurbelumdrehung
- Messwerte aus Abschnitt 4 pro Umdrehung, Mittelwert und Streuung über 30+ Umdrehungen
- Live-Overlay: Skelett und Winkel im Video, Ampelfarben
- Regelwerk für Sattelhöhe und Sattelversatz, Empfehlung in mm
- Kurze Anamnese (Profil, Beschwerden)
- Sitzungsverlauf: Vorher/Nachher-Vergleich nach jeder Änderung
- PDF-Bericht

### Phase 2 – „Komplettes Fitting“
- Frontalansicht mit zweiter Kamera: Knie-Tracking, Symmetrie, Becken
- Cockpit-Empfehlungen: Reach, Lenkerhöhe, Spacer, Vorbaulänge
- Beide Körperseiten (Rad drehen oder zweite Seitenkamera)
- Rad-Koordinaten erfassen (Sattelhöhe ab Tretlager, Versatz, Lenker-Stack/Reach) und speichern
- Optional farbige Klebepunkte für höhere Genauigkeit

### Phase 3 – „Pro / Laden-tauglich“
- Tiefenkamera-Unterstützung
- Mehrere Fahrer und Räder verwalten
- Positionsübertragung auf neues Rad (Rahmengröße-Empfehlung aus Stack/Reach)
- Cleat-Assistent (Fußballen über Pedalachse)

---

## 9. Architektur

```
 Kamera / Video
      │
      ▼
 [1] Capture        Webcam, Handy-Stream oder Datei, Zeitstempel pro Frame
      │
      ▼
 [2] Kalibrierung   Marker → Kamerapose, Maßstab px→mm, Ausrichtungs-Check
      │
      ▼
 [3] Pose           Keypoints pro Frame + Konfidenz
      │               (z.B. RTMPose / MediaPipe, lokal via ONNX)
      ▼
 [4] Filter         Ausreißer weg, Glättung (One-Euro / Butterworth)
      │
      ▼
 [5] Zyklen         Kurbelumdrehungen erkennen (Fußbahn um Tretlager)
      │
      ▼
 [6] Kennzahlen     Winkel & Abstände pro Umdrehung → Statistik
      │
      ▼
 [7] Regelwerk      Profil + Zielbereiche + Geometrie → Empfehlung in mm
      │
      ▼
 [8] UI & Bericht   Live-Overlay, Dashboard, Vorher/Nachher, PDF
      │
 [9] Speicher       Sitzungen, Fahrer, Räder (lokal, SQLite)
```

### Technologie-Vorschlag
- **Sprache:** Python für den Analyse-Kern. OpenCV für Kamera und Marker, ONNX Runtime für das Pose-Modell, NumPy/SciPy für Signalverarbeitung. Alles läuft lokal, auch ohne Internet.
- **Pose-Modell:** Zwei Kandidaten testen wir gegeneinander: **MediaPipe Pose** (sehr einfach, schnell, läuft auf jeder CPU) und **RTMPose** (in Vergleichsstudien meist genauer an den Beinen). Studien zeigen, dass KI-Pose-Modelle Kniewinkel beim Radfahren auf wenige Grad genau treffen, aber am Fuß und an der Hüfte schwächer sind. Deshalb messen wir über viele Umdrehungen und bieten optional Klebepunkte an.
- **Oberfläche:** Lokale Web-Oberfläche im Browser (Python-Server plus einfaches Frontend). Vorteil: Läuft auf Mac und Windows, und das Handy kann sich per WLAN als zweite Kamera einklinken. Alternative wäre eine Desktop-App.
- **Regelwerk als Konfigurationsdatei** (YAML/JSON), damit Zielbereiche anpassbar sind, ohne Code zu ändern.

### Validierung
Bevor wir der Software trauen: Gelenkwinkel einmal mit Goniometer oder Klebepunkten von Hand nachmessen und mit der Software vergleichen. Ziel: Abweichung unter ca. 3° beim Knie.

---

## 10. Risiken

| Risiko | Gegenmaßnahme |
|---|---|
| Pose-Modell ungenau an Hüfte (Trochanter schwer zu sehen) | Mittelung, Klebepunkt-Option, Modellvergleich |
| Schlechtes Licht, weite Kleidung | Einrichtungs-Assistent prüft Erkennungsqualität |
| Kamera schräg → falsche Winkel | Marker-basierter Ausrichtungs-Check |
| Laptop-Webcam nur 30 fps | Handy als Kamera empfehlen |
| Empfehlungen ohne Kontext (Beschwerden, Beweglichkeit) | Anamnese im Ablauf, konservative Änderungsschritte (max. 5–10 mm pro Runde) |

---

## 11. Offene Fragen

Siehe Nachricht im Projekt. Die Antworten werden hier eingearbeitet.
