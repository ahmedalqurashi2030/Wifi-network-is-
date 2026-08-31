#!/usr/bin/env bash
set -euo pipefail

INPUT_FILE="$1"
OUTPUT_FILE="$2"
TITLE="${3:-Ethical Hacking Lab}"

mkdir -p "$(dirname "$OUTPUT_FILE")"
INPUT_FILE="$(realpath "$INPUT_FILE")"
OUTPUT_FILE="$(realpath -m "$OUTPUT_FILE")"
export INPUT_FILE OUTPUT_FILE TITLE

xvfb-run -a bash -lc '
  set -euo pipefail
  xterm -geometry 145x42 -fa "DejaVu Sans Mono" -fs 10 -title "$TITLE" \
    -e bash -lc "clear; cat \"$INPUT_FILE\"; sleep 8" &
  XPID=$!
  sleep 2
  scrot "$OUTPUT_FILE"
  kill "$XPID" 2>/dev/null || true
  wait "$XPID" 2>/dev/null || true
'

test -s "$OUTPUT_FILE"
