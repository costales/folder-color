#!/bin/bash

rm -rf ../.git
rm ../README.md

# Special
sed -i 's/python3-nautilus, nautilus, /python-nemo, nemo, /' ../debian/control

# folder-color to folder-color-nemo
find . -type f | xargs sed -i 's/folder-color/folder-color-nemo/g'

# nautilus to nemo
find . -type f | xargs sed -i 's/nautilus/nemo/g'
find . -type f | xargs sed -i 's/Nautilus/Nemo/g'

# Delete myself
rm -rf ../install-scripts