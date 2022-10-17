#!/bin/bash
rm -r ../icons
rm ../README

# setup
sed -i '25,34d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/Change your folder color with just a click/Change your folder color in Nautilus/' ../setup.py

# po
sed -i 's/folder_i18n/folder-color/' ../po/POTFILES.in
sed -i 's/folder_path/nautilus-extension/' ../po/POTFILES.in
sed -i 's/folder_i18n/folder-color/' ../nautilus-extension/folder-color.py

# debian
rm ../debian/postinst

sed -i '2d' ../debian/install

sed -i 's/ python3-nautilus, nautilus, / python3-nautilus, nautilus, /' ../debian/control

sed -i '25,44d' ../debian/copyright

sed -i 's/folder-color/folder-color/' ../debian/changelog

# me
rm -r ../install_scripts
