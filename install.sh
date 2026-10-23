#!/bin/bash
# Sets up or updates Bikefit: Python, packages and pose models.
# Python comes from uv (https://docs.astral.sh/uv/), which installs into the
# user's home folder without admin rights. Safe to run again at any time.
set -e
cd "$(dirname "$0")"
PYTHON_VERSION=3.13  # a version mediapipe ships wheels for

find_uv() {
  for c in "$(command -v uv)" "$HOME/.local/bin/uv" "$HOME/.cargo/bin/uv"; do
    [ -n "$c" ] && [ -x "$c" ] && { echo "$c"; return 0; }
  done
  return 0
}

UV=$(find_uv)
if [ -z "$UV" ] && command -v curl >/dev/null; then
  echo "Installing uv (downloads Python, no admin rights needed) ..."
  curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh >/dev/null || true
  UV=$(find_uv)
fi

if [ -n "$UV" ]; then
  if ! .venv/bin/python -c "import sys" 2>/dev/null; then
    echo "Setting up Python $PYTHON_VERSION ..."
    rm -rf .venv
    "$UV" venv --quiet --python "$PYTHON_VERSION" .venv
  fi
  echo "Checking packages ..."
  "$UV" pip install --quiet --python .venv/bin/python -r requirements.txt
elif [ -x .venv/bin/python ] || command -v python3 >/dev/null; then
  # no uv (e.g. offline): fall back to an existing environment or the system Python
  [ -x .venv/bin/python ] || python3 -m venv .venv
  echo "Checking packages ..."
  .venv/bin/python -m pip install --quiet -r requirements.txt
else
  echo "Could not install Python. Check the internet connection and try again."
  exit 1
fi

.venv/bin/python -c "from bikefit.pose import model_path; model_path('heavy'); model_path('full')"
mkdir -p videos
