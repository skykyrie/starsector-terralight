#!/bin/bash
# Compile-check the mod's loose Java scripts against the Starsector API source (unofficial mirror) + small stubs.
# Usage: tools/jcheck.sh [folder with data/**.java]   (default: build/TerraLight/data)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(dirname "$HERE")"
API="$ROOT/_scratch/starsector-api"
[ -d "$API" ] || git clone --depth 1 https://github.com/jaghaimo/starsector-api.git "$API" >/dev/null 2>&1
OUT="$ROOT/_scratch/jc"; rm -rf "$OUT"; mkdir -p "$OUT"
javac -nowarn -encoding latin1 -proc:none -implicit:none -sourcepath "$API/src:$HERE/java_stubs" -d "$OUT" \
  $(find "${1:-$ROOT/build/TerraLight/data}" -name "*.java") 2>&1 | grep -v JAVA_TOOL | grep -v "^Note:" || true
echo "javac done (no 'error:' lines above = OK)"
