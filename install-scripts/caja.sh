#!/bin/bash

rm -rf ../.git
rm ../README.md

# Special
sed -i 's/python3-nautilus, nautilus, /python3-caja, caja, /' ../debian/control

# folder-color to folder-color-nemo
find . -type f -name "*.txt" | xargs sed -i 's/folder-color/folder-color-caja/g'

# nautilus to nemo
find . -type f -name "*.txt" | xargs sed -i 's/nautilus/caja/g'
find . -type f -name "*.txt" | xargs sed -i 's/Nautilus/Caja/g'
find . -type f -name "*.txt" | xargs sed -i 's/metadata::custom-icon-name/metadata::custom-icon/g'

# Delete myself
rm -rf ../install-scripts