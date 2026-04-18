#!/usr/bin/env bash
# Convert icon.svg -> dist/AppIcon.icns using macOS built-ins (qlmanage + sips + iconutil).
# No external deps needed.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SVG="$ROOT/icon.svg"
OUT_DIR="$ROOT/dist"
ICONSET="$OUT_DIR/AppIcon.iconset"
ICNS="$OUT_DIR/AppIcon.icns"

if [[ ! -f "$SVG" ]]; then
  echo "icon.svg not found at $SVG" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"
rm -rf "$ICONSET"
mkdir -p "$ICONSET"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

BASE_PNG="$TMP_DIR/base.png"
qlmanage -t -s 1024 -o "$TMP_DIR" "$SVG" >/dev/null
mv "$TMP_DIR"/*.png "$BASE_PNG"

# Standard macOS iconset sizes
declare -a SIZES=(16 32 64 128 256 512 1024)
for SIZE in "${SIZES[@]}"; do
  NAME="icon_${SIZE}x${SIZE}.png"
  sips -z "$SIZE" "$SIZE" "$BASE_PNG" --out "$ICONSET/$NAME" >/dev/null
  if [[ "$SIZE" != "1024" ]]; then
    DOUBLE=$((SIZE * 2))
    NAME2X="icon_${SIZE}x${SIZE}@2x.png"
    sips -z "$DOUBLE" "$DOUBLE" "$BASE_PNG" --out "$ICONSET/$NAME2X" >/dev/null
  fi
done

iconutil -c icns "$ICONSET" -o "$ICNS"
echo "Wrote $ICNS"
