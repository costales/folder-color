#!/bin/bash
rm ../README

# po
sed -i 's/folder_i18n/folder-color/' ../po/POTFILES.in
sed -i 's/folder_path/nautilus-extension/' ../po/POTFILES.in
sed -i 's/folder_i18n/folder-color/' ../nautilus-extension/folder-color.py

# me
cd ..
rm -r install_scripts
