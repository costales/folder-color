#!/bin/bash
rm ../README
rm -rf ../nautilus-extension-gtk3
rm -rf ../.git

# po
sed -i 's/folder_i18n/folder-color/' ../po/POTFILES.in
sed -i 's/folder_path/nautilus-extension/' ../po/POTFILES.in
sed -i 's/folder_i18n/folder-color/' ../nautilus-extension/folder-color.py

# me
rm -rf ../install_scripts
