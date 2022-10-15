#!/bin/bash
rm -r ../icons
rm -r ../po
rm ../README

# setup
sed -i '25,34d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/Change your folder color with just a click/Change your folder color in Nemo/' ../setup.py
sed -i 's/nautilus-python/nemo-python/' ../setup.py
sed -i 's/nautilus-extension/nemo-extension/' ../setup.py
sed -i 's/"folder-color"/"folder-color-nemo"/' ../setup.py

# extension
mv ../nautilus-extension/ ../nemo-extension
sed -i 's/nautilus/nemo/g' ../nemo-extension/folder-color.py
sed -i 's/Nautilus/Nemo/g' ../nemo-extension/folder-color.py

# debian
rm ../debian/postinst

sed -i '2d' ../debian/install
sed -i 's/nautilus/nemo/g' ../debian/install

sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-nemo/' ../debian/copyright
sed -i '25,44d' ../debian/copyright

sed -i 's/Source: folder-color/Source: folder-color-nemo/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-nemo/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python-nemo, nemo, folder-color-common, /' ../debian/control
sed -i '14,15d' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color for Nemo/' ../debian/control
sed -i 's/Change a folder color used in Nautilus/Change a folder color used in Nemo/' ../debian/control

sed -i 's/folder-color/folder-color-nemo/' ../debian/changelog

# me
rm -r ../install_scripts

