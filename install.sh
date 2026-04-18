#!/usr/bin/env bash
# Build AgentOps.app and install it to /Applications.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PY_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')
if [[ "$PY_MAJOR" -lt 3 || ( "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 12 ) ]]; then
  echo "Python 3.12+ required (found $PY_MAJOR.$PY_MINOR)" >&2
  exit 1
fi

if [[ ! -d .venv ]]; then
  echo "==> Creating virtual env"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Installing dependencies"
pip install --upgrade pip >/dev/null
pip install -e ".[build]" >/dev/null

echo "==> Generating app icon"
bash scripts/make-icns.sh

echo "==> Building AgentOps.app with PyInstaller"
rm -rf build dist/AgentOps dist/AgentOps.app
pyinstaller --noconfirm agentops.spec

APP="$ROOT/dist/AgentOps.app"
if [[ ! -d "$APP" ]]; then
  echo "Build failed: $APP not found" >&2
  exit 1
fi

echo "==> Installing to /Applications"
rm -rf /Applications/AgentOps.app
cp -R "$APP" /Applications/

echo ""
echo "Done. Launch AgentOps from /Applications."
echo "On first launch: right-click -> Open (not code-signed yet)."
