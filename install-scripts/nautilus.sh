#!/bin/bash

if [ -z "$1" ]; then
    echo "Call as ./nautilus.sh GTK4 or ./nautilus.sh GTK3"
    exit 1
fi

# GTK
if [ "$1" == "GTK4" ]; then
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

# debian
if [ "$1" == "GTK3" ]; then
    sed -i 's/kinetic/focal/' ../debian/changelog
fi

# myself
rm -rf ../install-scripts

echo "Done"
