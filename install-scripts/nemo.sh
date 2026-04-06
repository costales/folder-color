#!/bin/bash

rm -rf ../.git
rm ../README.md

# Myself
rm -rf ../install-scripts

# Build
find . -type f -name "*.txt" -print0 | xargs -0 sed -i 's/folder-color/folder-color-nemo/g'
find . -type f -name "*.txt" -print0 | xargs -0 sed -i 's/nautilus/nemo/g'
find . -type f -name "*.txt" -print0 | xargs -0 sed -i 's/Nautilus/Nemo/g'

echo "Done"

cd ..