#!/bin/bash
# Richtet die Python-Umgebung ein (einmalig).
set -e
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo "Python 3 fehlt. Bitte von https://www.python.org/downloads/ installieren."
  exit 1
fi
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python -c "from bikefit.pose import model_path; model_path('heavy'); model_path('full')"
mkdir -p videos
echo
echo "Fertig. Beispiel: bash bikefit.sh analyse videos/MEIN_VIDEO.mp4 --kurbel 172.5"
