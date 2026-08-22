#!/bin/bash
set -e

# Capture the argument passed to main.sh, defaulting to "/" if empty
BASEPATH=${1:-"/"}

echo "--- Initiating Production Site Compilation ---"
python3 src/main.py "$BASEPATH"

echo "--- Booting Development Web Server ---"
cd public && python3 -m http.server 8888
