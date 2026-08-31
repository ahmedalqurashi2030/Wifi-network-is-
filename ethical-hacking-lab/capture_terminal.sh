#!/usr/bin/env bash
set -euo pipefail

INPUT_FILE="$1"
OUTPUT_FILE="$2"
TITLE="${3:-Ethical Hacking Lab}"

mkdir -p "$(dirname "$OUTPUT_FILE")"

# Render the real command/output text inside an actual xterm window under Xvfb,
# then capture the terminal window. This preserves genuine execution evidence.
xvfb-run -a bash -lc '
  set -e
  export DISPLAY=${DISPLAY}
  xterm -geometry 145x42 -fa "DejaVu Sans Mono" -fs 10 -title '"'"'"$TITLE"'"'"' -hold \
    -e bash -lc '"'"'clear; cat "'"'"'"$INPUT_FILE"'"'"'"; sleep 20'"'"' &
  XPID=$!
  sleep 2
  scrot '"'"'"$OUTPUT_FILE"'"'"'
  kill "$XPID" 2>/dev/null || true
' 
