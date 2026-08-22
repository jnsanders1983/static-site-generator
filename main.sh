#!/bin/bash

# 1. Execute compilation and transformation routines
python3 src/main.py

# 2. Jump inside distribution environment and spawn the development server network listener
cd public && python3 -m http.server 8888
