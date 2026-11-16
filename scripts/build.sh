#!/usr/bin/env bash
# Regenerates every SVG in ../assets. Edit text/colours in the .py files, then run: bash scripts/build.sh
set -e
cd "$(dirname "$0")"
A=../assets
python3 hero.py $A/hero.svg
python3 about.py $A/about.svg
python3 pipeline.py $A/pipeline.svg
python3 orbit.py $A/orbit.svg
python3 cards.py $A
echo "assets regenerated"
