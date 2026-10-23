# Bikefit – Video-Bikefitting

Misst deine Gelenkwinkel auf dem Rad aus einem Video, ganz ohne Marker. Läuft lokal im Browser und startet per Doppelklick. Die Oberfläche gibt es auf Deutsch und Englisch (Umschalter oben rechts).

## Starten (Mac)

1. Im Finder im Ordner `bikefit` auf **`start.command`** doppelklicken.
   - Falls macOS warnt („nicht verifizierter Entwickler“): Rechtsklick → Öffnen → Öffnen.
   - Falls sich stattdessen ein Texteditor öffnet: Terminal öffnen und `bash ~/Documents/"Bikefit Software"/bikefit/start.command` eingeben.
2. Beim ersten Start installiert sich alles selbst: Python (über [uv](https://docs.astral.sh/uv/), in deinen Benutzerordner, ohne Admin-Rechte), alle Pakete und das Erkennungsmodell (ca. 40 MB). Das dauert einige Minuten, danach öffnet sich der Browser mit Bikefit.
3. Bei späteren Starts werden nur noch die Pakete geprüft.
4. Beenden: Im Terminalfenster Ctrl+C drücken oder das Fenster schließen.

## Starten (Windows)

1. Im Ordner `bikefit` auf **`start.bat`** doppelklicken.
   - Falls Windows warnt („Der Computer wurde durch Windows geschützt“): Weitere Informationen → Trotzdem ausführen.
2. Beim ersten Start werden Python, Pakete und Modelle genauso installiert, danach öffnet sich der Browser. Beenden: Konsolenfenster schließen.

Alle Daten (Profil, Garage, Videos, Auswertungen) liegen im Ordner `data/`. Daten aus der ersten Version (`daten/`, `ergebnisse/`, `profil.json`) werden beim Start automatisch übernommen.

## Die Oberfläche

Der Ablauf ist wie ein Gespräch beim Fitter: **Gespräch** (Ziel, Beschwerden) → **Körper** (Größe, Schrittlänge, Beweglichkeit) → **Rad** (Garage mit Marke, Modell, Kurbellänge, aktuellen Einstellungen oder ein Modell aus dem Katalog) → **Video** hochladen → **Auswertung**: das Video mit Skelett, der nächste Schritt und alle Messwerte. Bei jedem Wert außerhalb des Zielbereichs steht, was du am Rad änderst. Danach verstellst du das Rad, trägst die neuen Maße ein und lädst ein neues Video hoch, bis alles im Zielbereich ist. Alte Fittings löschst du auf der Startseite über das Papierkorb-Symbol (mit Sicherheitsabfrage).

## Aufnahme mit dem Handy

- Video in 1080p mit 60 fps, Handy seitlich vom Rad, 2,5 bis 4 m entfernt, auf Höhe von Hüfte bis Tretlager, genau quer zum Rad.
- Ganze Person mit Rad im Bild, Querformat. Eng anliegende Kleidung, helles gleichmäßiges Licht.
- 2 Minuten warm fahren, dann mindestens 60 Sekunden bei 85 bis 95 U/min filmen, Hände am Bremsgriff.

## Terminal

```
bash install.sh                  # einrichten oder aktualisieren
bash bikefit.sh profile          # Fahrer- und Radprofil
bash bikefit.sh --lang de analyze videos/MEIN_VIDEO.mp4 --crank 172.5
```

Ergebnisse landen in `results/MEIN_VIDEO/` (`report.txt`, `analysis.mp4`, CSV-Dateien). Mehr Details, wie es funktioniert und welche Grenzen es gibt, stehen in der englischen [README.md](README.md).
