#!/bin/bash
# Startet Bikefit mit der eingerichteten Umgebung, z.B. bash bikefit.sh analyse video.mp4
cd "$(dirname "$0")"
exec .venv/bin/python -m bikefit "$@"
