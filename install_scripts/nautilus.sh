#!/bin/bash
rm ../README
rm r ../nautilus-extension-gtk3

# po
sed -i 's/folder_i18n/folder-color/' ../po/POTFILES.in
sed -i 's/folder_path/nautilus-extension/' ../po/POTFILES.in
sed -i 's/folder_i18n/folder-color/' ../nautilus-extension/folder-color.py

# me
rm -r ../install_scripts
