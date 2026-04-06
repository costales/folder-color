#!/bin/bash

rm -rf ../.git
rm ../README.md

# Extension
sed -i "s/metadata::custom-icon-name/metadata::custom-icon/g" ../extension/folder-color.py

# Build
find .. -type f -print0 | xargs -0 sed -i 's/folder-color/folder-color-caja/g'
find .. -type f -print0 | xargs -0 sed -i 's/nautilus/caja/g'
find .. -type f -print0 | xargs -0 sed -i 's/Nautilus/Caja/g'

# Myself
rm -rf ../install-scripts

echo "Done. Go to parent directory"