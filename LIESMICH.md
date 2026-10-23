# Bikefit – Video-Analyse

Misst deine Gelenkwinkel auf dem Rad aus einem Video, ganz ohne Marker. Bedient wird im Browser, gestartet per Doppelklick.

## Starten (Mac)

1. **Python installieren:** Auf https://www.python.org/downloads/ die aktuelle Version 3.12 oder 3.13 für macOS laden und installieren.
2. Im Finder im Ordner `bikefit` auf **`start.command`** doppelklicken.
   - Falls macOS warnt („nicht verifizierter Entwickler“): Rechtsklick → Öffnen → Öffnen.
   - Falls sich stattdessen ein Texteditor öffnet: Terminal öffnen und `bash ~/Documents/"Bikefit Software"/bikefit/start.command` eingeben.
3. Beim ersten Start wird alles installiert (einige Minuten, ca. 30 MB Erkennungsmodell). Danach öffnet sich der Browser mit Bikefit.
4. Beenden: Im Terminalfenster Ctrl+C drücken oder das Fenster schließen.

## Starten (Windows)

1. **Python installieren:** Auf https://www.python.org/downloads/ Version 3.12 oder 3.13 für Windows laden. Im Installer **„Add python.exe to PATH“** anhaken.
2. Im Ordner `bikefit` auf **`start.bat`** doppelklicken.
   - Falls Windows warnt („Der Computer wurde durch Windows geschützt“): Weitere Informationen → Trotzdem ausführen.
3. Beim ersten Start wird alles installiert, danach öffnet sich der Browser. Beenden: Konsolenfenster schließen.

Alle Daten (Profil, Garage, Videos, Auswertungen) liegen im Ordner `daten/`.

## Die Oberfläche

Der Ablauf ist wie ein Gespräch beim Fitter: **Gespräch** (Ziel, Beschwerden) → **Körper** (Größe, Schrittlänge, Beweglichkeit) → **Rad** (Garage mit Marke, Modell, Kurbellänge, aktuellen Einstellungen) → **Video** hochladen → **Auswertung**: links das Video mit Skelett, rechts der nächste Schritt und alle Messwerte. Danach verstellst du das Rad, trägst die neuen Maße ein und lädst ein neues Video hoch. Die Software vergleicht jede Runde mit der vorherigen, bis alles im Zielbereich ist. Alte Fittings löschst du auf der Startseite über das Papierkorb-Symbol (mit Sicherheitsabfrage).

## Für Fortgeschrittene: Terminal

### Profil anlegen

```
bash installieren.sh   # einmalig
bash bikefit.sh profil
```
Fragt Körpergröße, Schrittlänge, Beweglichkeit, Ziel, Beschwerden und die Daten deines Rads ab (Geometrie von der Herstellerseite, Ist-Maße mit dem Maßband). Damit passt die Software die Zielbereiche an dich an, prüft den Maßstab und gibt Empfehlungen als konkrete Einstellungen aus, z. B. „Sattelhöhe 755 → 749 mm“ oder „Vorbau 110 → 100 mm“. Mit Kurbellänge im Profil kannst du `--kurbel` weglassen.

### Video auswerten

**Aufnahme mit dem Pixel 9:**
- Kamera-App, Video in **1080p mit 60 fps** einstellen.
- Handy seitlich vom Rad, **2,5 bis 4 m** entfernt, auf **Höhe von Hüfte bis Tretlager**, gerade (nicht schräg) zum Rad. Die Kamera sollte genau quer zum Rad stehen.
- Die **ganze Person mit Rad** muss im Bild sein, Querformat.
- Eng anliegende Kleidung, helles gleichmäßiges Licht, möglichst ruhiger Hintergrund.
- 2 Minuten warm fahren, dann **mindestens 60 Sekunden** bei 85 bis 95 U/min und mittlerer Last filmen, Hände am Bremsgriff.
- Video auf den Mac kopieren (z. B. über Google Drive oder per USB-Kabel), am besten in den Ordner `videos`.

**Auswerten:**
```
bash bikefit.sh analyse videos/MEIN_VIDEO.mp4 --kurbel 172.5
```
Für Triathlon/Zeitfahrrad mit Aufleger zusätzlich `--profil zeitfahren` angeben.

`--kurbel` ist deine Kurbellänge in mm (steht auf der Innenseite der Kurbel). Damit rechnet die Software Pixel in mm um und kann sagen, um wie viele mm der Sattel sich ändern sollte.

Ergebnisse landen in `ergebnisse/MEIN_VIDEO/`:
- `bericht.txt` – Messwerte, Zielbereiche, Empfehlung
- `analyse.mp4` – dein Video mit Skelett und Winkeln
- `umdrehungen.csv`, `frames.csv` – alle Rohwerte (öffnet sich in Excel/Numbers)

## Wie es funktioniert

1. MediaPipe erkennt in jedem Bild 33 Körperpunkte; genutzt wird die Körperseite, die zur Kamera zeigt.
2. Die Bewegungen werden geglättet (Wackeln der Erkennung entfernen).
3. Aus dem Kniewinkel werden die einzelnen Kurbelumdrehungen erkannt.
4. Aus der Bahn des Fußes wird der Pedalkreis bestimmt. Mittelpunkt = Tretlager, Radius = Kurbellänge → Maßstab in mm.
5. Pro Umdrehung werden Knie, Hüfte, Fußgelenk, Oberkörper, Schulter, Ellbogen und Knie-über-Pedal gemessen, dann der Median über alle Umdrehungen gebildet.
6. Regeln in der Fitting-Reihenfolge (Sattelhöhe → Sattelversatz → Cockpit) ergeben **eine** Empfehlung. Danach ändern, neu messen.

## Automatische Korrekturen

Vor der Glättung repariert die Software typische Erkennungsfehler: vertauschte Beine (wenn sich die Beine in der Seitenansicht kreuzen), einzelne Sprünge von Knöchel oder Fuß und Bilder, in denen Ober- oder Unterschenkel plötzlich zu lang oder zu kurz wären. Wie viel korrigiert wurde, steht im Bericht unter INFO.

## Bekannte Grenzen

- Anfang und Ende des Videos (Aufsteigen, zur Kamera laufen) schneidet die Software automatisch ab. Ausgewertet wird die längste Strecke, in der du auf dem Rad sitzt.
- Die Hüftbewegung wird nur als Info gezeigt: Ohne Marker wandert der Hüftpunkt mit dem Oberschenkel mit, der Wert ist deshalb zu hoch.

- Ohne Marker ist der Hüftpunkt die unsicherste Stelle. Werte über viele Umdrehungen sind trotzdem stabil.
- Der Oberkörperwinkel setzt voraus, dass die Kamera waagerecht steht.
- Knie-über-Pedal ist ein grober Richtwert.
- Die Zielbereiche sind Richtwerte für ein Rennrad.
