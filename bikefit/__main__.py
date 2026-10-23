"""Command line entry point: python -m bikefit <command> ..."""
from __future__ import annotations

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="bikefit", description="Bikefit: measure joint angles on the bike.")
    parser.add_argument("--lang", choices=["en", "de"], default="en", help="Language of reports and messages")
    sub = parser.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="Analyse a recorded video")
    a.add_argument("video", type=Path)
    a.add_argument("--crank", type=float, help="Crank length in mm, e.g. 172.5 (for values in mm)")
    a.add_argument("--side", choices=["auto", "left", "right"], default="auto", help="Body side facing the camera")
    a.add_argument("--model", choices=["lite", "full", "heavy"], default="heavy")
    a.add_argument("--profile", choices=["road", "tt"],
                   help="Target ranges: road or tt (time trial/triathlon). Default: bike type from profile.json")
    a.add_argument("--max-seconds", type=float, help="Only analyse the start of the video")
    a.add_argument("--out", type=Path, help="Folder for results")
    a.add_argument("--no-video", action="store_true", help="Do not write the overlay video")

    sub.add_parser("profile", help="Enter or change the rider and bike profile")
    w = sub.add_parser("web", help="Start the browser interface")
    w.add_argument("--port", type=int, default=8765)
    w.add_argument("--no-browser", action="store_true", help="Do not open the browser automatically")

    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    from .migrate import migrate_project
    migrate_project(root)
    profile_path = root / "profile.json"
    from .profile import Profile
    rider = Profile.load(profile_path)

    if args.cmd == "analyze":
        from .video import analyze_file
        out = args.out or root / "results" / args.video.stem
        analyze_file(args.video, out, args.crank, args.side, args.model, args.max_seconds,
                     render=not args.no_video, profile=args.profile, rider=rider, lang=args.lang)
    elif args.cmd == "web":
        import threading
        import webbrowser

        import uvicorn

        from .web.app import create_app
        url = f"http://127.0.0.1:{args.port}"
        print(f"Bikefit is running at {url}  (stop with Ctrl+C)")
        if not args.no_browser:
            threading.Timer(1.5, webbrowser.open, (url,)).start()
        uvicorn.run(create_app(root / "data"), host="127.0.0.1", port=args.port, log_level="warning")
    elif args.cmd == "profile":
        from .profile import interactive
        interactive(profile_path)


if __name__ == "__main__":
    main()
