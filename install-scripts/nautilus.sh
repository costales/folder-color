#!/bin/bash

echo "Call as ./nautilus.sh GTK4 or ./nautilus.sh GTK3"

# GTK
if [ $1="GTK4" ]; then
    echo "It's GTK4"
    rm -rf ../nautilus-extension-gtk3
else
    echo "It's GTK3"
    rm -rf ../nautilus-extension
    mv ../nautilus-extension-gtk3 ../nautilus-extension
fi

rm -rf ../.git
rm ../README.md

# po
sed -i 's/folder_i18n/folder-color/' ../po/POTFILES.in
sed -i 's/folder_path/nautilus-extension/' ../po/POTFILES.in
sed -i 's/folder_i18n/folder-color/' ../nautilus-extension/folder-color.py

# myself
rm -rf ../install-scripts
