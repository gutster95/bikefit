#!/bin/bash
# Double-click to start Bikefit in the browser (Mac). The first start installs
# Python and all packages, later starts only check for updates.
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || echo "First start: setting up Bikefit (a few minutes) ..."
bash install.sh || { echo "Setup failed."; read -p "Press Enter to close"; exit 1; }
echo "Starting Bikefit, the browser opens in a moment ..."
.venv/bin/python -m bikefit web
