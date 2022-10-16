#!/bin/bash
rm -r ../nautilus-extension
rm -r ../po
rm ../README

# setup
sed -i 's/data = .*/data = [/' ../setup.py
sed -i 's/"folder-color"/"folder-color-yaru"/' ../setup.py
sed -i 's/Change your folder color with just a click/Folder Color Library/' ../setup.py

# debian
sed -i '1d' ../debian/install
sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-yaru/' ../debian/copyright
sed -i 's/Source: folder-color/Source: folder-color-yaru/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-yaru/' ../debian/control
sed -i 's/python3-nautilus, nautilus, //' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color Library/' ../debian/control
sed -i 's/Change a folder color used in Nautilus/Icons and translations for Folder Color/' ../debian/control
sed -i 's/folder-color/folder-color-yaru/' ../debian/changelog

# me
rm -r ../install_scripts
