#!/bin/bash

rm -rf ../.git
rm ../README.md

# po
sed -i 's/folder_i18n/folder-color/' ../po/POTFILES.in
sed -i 's/folder_path/extension-GTK4/' ../po/POTFILES.in
sed -i 's/folder_i18n/folder-color/' ../extension-GTK3/folder-color.py
sed -i 's/folder_i18n/folder-color/' ../extension-GTK4/folder-color.py

# myself
rm -rf ../install-scripts

echo "Done"
