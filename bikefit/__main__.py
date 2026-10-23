"""Command line entry point: python -m bikefit <befehl> ..."""
from __future__ import annotations

import argparse
from pathlib import Path

SIDES = {"auto": "auto", "links": "left", "rechts": "right"}


def main():
    parser = argparse.ArgumentParser(prog="bikefit", description="Bikefit: Gelenkwinkel auf dem Rad messen.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyse", help="Ein aufgenommenes Video auswerten")
    a.add_argument("video", type=Path)
    a.add_argument("--kurbel", type=float, help="Kurbellänge in mm, z.B. 172.5 (für Angaben in mm)")
    a.add_argument("--seite", choices=SIDES, default="auto", help="Körperseite zur Kamera")
    a.add_argument("--modell", choices=["lite", "full", "heavy"], default="heavy")
    a.add_argument("--profil", choices=["rennrad", "zeitfahren"],
                   help="Zielbereiche: rennrad oder zeitfahren (Triathlon/Aufleger). Standard: Radtyp aus profil.json")
    a.add_argument("--max-sekunden", type=float, help="Nur den Anfang des Videos auswerten")
    a.add_argument("--ausgabe", type=Path, help="Ordner für Ergebnisse")
    a.add_argument("--ohne-video", action="store_true", help="Kein Overlay-Video schreiben")

    sub.add_parser("profil", help="Fahrer- und Radprofil eingeben oder ändern")
    w = sub.add_parser("web", help="Oberfläche im Browser starten")
    w.add_argument("--port", type=int, default=8765)
    w.add_argument("--kein-browser", action="store_true", help="Browser nicht automatisch öffnen")

    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    profile_path = root / "profil.json"
    from .profile import Profile
    rider = Profile.load(profile_path)

    if args.cmd == "analyse":
        from .video import analyze_file
        out = args.ausgabe or root / "ergebnisse" / args.video.stem
        analyze_file(args.video, out, args.kurbel, SIDES[args.seite], args.modell,
                     args.max_sekunden, render=not args.ohne_video, profile=args.profil,
                     rider=rider)
    elif args.cmd == "web":
        import threading
        import webbrowser

        import uvicorn

        from .web.app import create_app
        url = f"http://127.0.0.1:{args.port}"
        print(f"Bikefit läuft auf {url}  (beenden mit Ctrl+C)")
        if not args.kein_browser:
            threading.Timer(1.5, webbrowser.open, (url,)).start()
        uvicorn.run(create_app(root / "daten"), host="127.0.0.1", port=args.port, log_level="warning")
    elif args.cmd == "profil":
        from .profile import interactive
        interactive(profile_path)


if __name__ == "__main__":
    main()
