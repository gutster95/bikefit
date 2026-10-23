# Bikefit – video bike fitting

Measures your joint angles on the bike from a video, without markers. Runs locally in the browser and starts with a double-click. The interface is available in English and German (switch in the top right).

German guide: [README.de.md](README.de.md)

## Start (Mac)

1. In Finder, open the `bikefit` folder and double-click **`start.command`**.
   - If macOS warns about an unidentified developer: right-click → Open → Open.
   - If a text editor opens instead: open Terminal and run `bash ~/Documents/"Bikefit Software"/bikefit/start.command`.
2. The first start installs everything by itself: Python (via [uv](https://docs.astral.sh/uv/), into your home folder, no admin rights needed), all packages and the pose model (about 40 MB). This takes a few minutes. Then the browser opens with Bikefit.
3. Later starts only check for updated packages.
4. To stop: press Ctrl+C in the Terminal window or close it.

## Start (Windows)

1. In the `bikefit` folder, double-click **`start.bat`**.
   - If Windows warns ("Windows protected your PC"): More info → Run anyway.
2. The first start installs Python, packages and models the same way, then the browser opens. To stop: close the console window.

All data (rider, garage, videos, results) lives in the `data/` folder. Data from the first, German-named version (`daten/`, `ergebnisse/`, `profil.json`) is moved automatically on start.

## The interface

The flow is like a conversation with a fitter: **Interview** (goal, complaints) → **Body** (height, inseam, flexibility) → **Bike** (garage with brand, model, crank length, current settings, or a model from the catalogue) → upload a **Video** → **Results**: the video with the detected skeleton, the next step and all measurements. Every value outside its target range shows what to change on the bike. Adjust the bike, enter the new settings and upload a new video. Each round is compared with the previous one until everything is in range. Old fittings can be deleted on the start page (with confirmation).

## Command line

```
bash install.sh                  # set up or update
bash bikefit.sh profile          # rider and bike profile (profile.json)
bash bikefit.sh analyze videos/MY_VIDEO.mp4 --crank 172.5
bash bikefit.sh --lang de analyze videos/MY_VIDEO.mp4
```

Options for `analyze`: `--crank` crank length in mm (scales pixels to millimetres; defaults to the profile), `--profile tt` for time trial / triathlon target ranges, `--side left|right`, `--max-seconds`, `--out`, `--no-video`.

Results go to `results/MY_VIDEO/`:
- `report.txt` – measurements, target ranges, recommendation
- `analysis.mp4` – your video with skeleton and angles
- `result.json` – language-neutral result (numbers and message keys)
- `cycles.csv`, `frames.csv` – all raw values

## Recording tips

- Video in 1080p at 60 fps, phone to the side of the bike, 2.5 to 4 m away, between hip and bottom bracket height, square to the bike.
- The whole person and bike in the frame, landscape. Tight clothes, bright even light.
- Warm up for 2 minutes, then film at least 60 seconds at 85 to 95 rpm, hands on the hoods.

## How it works

1. MediaPipe finds 33 body points in every frame; the side facing the camera is used.
2. Typical detection errors are repaired (swapped legs, single jumps, implausible segment lengths), then the tracks are smoothed.
3. Crank revolutions are detected from the knee angle.
4. The foot path gives the pedal circle: centre = bottom bracket, radius = crank length → scale in mm.
5. Knee, hip, ankle, torso, shoulder, elbow and knee-over-pedal are measured per revolution; the median over all revolutions is used.
6. Rules in fitting order (saddle height → setback → cockpit) give **one** recommendation at a time. Change it, film again.

There is no AI model besides pose detection: all advice is rule-based (`bikefit/targets.py`), texts are in `bikefit/i18n.py`.

## Known limits

- Getting on and off at the start and end of the video is cut automatically.
- Without markers the hip point is the least certain; values over many revolutions are still stable. Hip rocking is shown for information only.
- The torso angle assumes a level camera. Knee-over-pedal is a rough guide.

## Development

```
.venv/bin/python -m pytest
```
