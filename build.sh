#!/bin/bash
set -e

echo "--- Initiating Production Build Suite ---"

# Compiles your project using your custom repository root subdirectory context
python3 src/main.py "/static-site-generator/"

echo "--- Production Build Completed Successfully ---"
