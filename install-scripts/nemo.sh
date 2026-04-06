#!/bin/bash

rm -rf ../.git
rm ../README.md

# Build
find .. -type f -name "*.txt" -print0 | xargs -0 sed -i 's/folder-color/folder-color-nemo/g'
find .. -type f -name "*.txt" -print0 | xargs -0 sed -i 's/nautilus/nemo/g'
find .. -type f -name "*.txt" -print0 | xargs -0 sed -i 's/Nautilus/Nemo/g'

# Myself
rm -rf ../install-scripts

echo "Done. Go to parent directory and run dpkg-buildpackage"