#!/bin/bash
# Doppelklick startet Bikefit im Browser. Beim ersten Mal wird alles installiert.
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  bash installieren.sh || { echo "Installation fehlgeschlagen."; read -p "Enter zum Schließen"; exit 1; }
fi
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python -m bikefit web
