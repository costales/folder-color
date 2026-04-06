#!/bin/bash

rm -rf ../.git
rm ../README.md

# Myself
rm -rf ../install-scripts

# Extension
sed -i "s/metadata::custom-icon-name/metadata::custom-icon/g" ../extension/GTK3.py
sed -i "s/metadata::custom-icon-name/metadata::custom-icon/g" ../extension/GTK4.py

# Build
find . -type f -name "*.txt" -print0 | xargs -0 sed -i 's/folder-color/folder-color-caja/g'
find . -type f -name "*.txt" -print0 | xargs -0 sed -i 's/nautilus/caja/g'
find . -type f -name "*.txt" -print0 | xargs -0 sed -i 's/Nautilus/Caja/g'

echo "Done. Go to parent directory and run dpkg-buildpackage"