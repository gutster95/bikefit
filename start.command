#!/bin/bash
# Doppelklick startet Bikefit im Browser (Mac). Beim ersten Mal wird alles installiert.
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  echo "Erster Start: Bikefit wird eingerichtet (einige Minuten) ..."
  bash installieren.sh || { echo "Installation fehlgeschlagen."; read -p "Enter zum Schließen"; exit 1; }
fi
echo "Prüfe Pakete ..."
.venv/bin/pip install -q -r requirements.txt
echo "Starte Bikefit, der Browser öffnet sich gleich ..."
.venv/bin/python -m bikefit web
