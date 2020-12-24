#!/bin/bash
rm -r ../nautilus-extension
rm ../README

# setup
sed -i 's/data = .*/data = [/' ../setup.py
sed -i 's/"folder-color"/"folder-color-common"/' ../setup.py
sed -i 's/Change your folder color with just a click/Folder Color Library/' ../setup.py

# po
sed -i 's/folder-color/folder-color-common/' ../po/POTFILES.in
sed -i '4d' ../po/POTFILES.in

# debian
sed -i '1d' ../debian/install
sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-common/' ../debian/copyright
sed -i 's/Source: folder-color/Source: folder-color-common/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-common/' ../debian/control
sed -i 's/python3-nautilus, nautilus, //' ../debian/control
sed -i 's/Breaks: .*/Breaks: folder-color (<< 0.0.50), folder-color-nemo (<< 0.0.50), folder-color-caja (<< 0.0.50)/' ../debian/control
sed -i 's/Replaces: .*/Replaces: folder-color (<< 0.0.50), folder-color-nemo (<< 0.0.50), folder-color-caja (<< 0.0.50)/' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color Library/' ../debian/control
sed -i 's/Change a folder color used in Nautilus/Icons and translations for Folder Color/' ../debian/control
sed -i 's/folder-color/folder-color-common/' ../debian/changelog

# me
rm -r ../install_scripts
