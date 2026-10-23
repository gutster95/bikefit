#!/bin/bash
# Runs Bikefit with the installed environment, e.g. bash bikefit.sh analyze video.mp4
cd "$(dirname "$0")"
exec .venv/bin/python -m bikefit "$@"
