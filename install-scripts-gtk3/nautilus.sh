#!/bin/bash

# GTK4
rm -rf ../nautilus-extension
rm -rf ../install-scripts

mv ../nautilus-extension-gtk3 ../nautilus-extension

rm -rf ../.git
rm ../README.md

# po
sed -i 's/folder_i18n/folder-color/' ../po/POTFILES.in
sed -i 's/folder_path/nautilus-extension/' ../po/POTFILES.in
sed -i 's/folder_i18n/folder-color/' ../nautilus-extension/folder-color.py

# myself
rm -rf ../install-scripts-gtk3
