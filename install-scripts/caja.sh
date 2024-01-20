#!/bin/bash

if [ -z "$1" ]; then
    echo "Call as ./caja.sh GTK4 or ./caja.sh GTK3"
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

mv ../nautilus-extension/ ../caja-extension
rm -rf ../.git
rm ../README.md
rm -r ../icons

# setup
sed -i '17,27d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/nautilus/caja/g' ../setup.py
sed -i 's/"folder-color"/"folder-color-caja"/' ../setup.py

# po
sed -i 's/folder_i18n/folder-color-caja/' ../caja-extension/folder-color.py
sed -i 's/folder_i18n/folder-color-caja/' ../po/POTFILES.in
sed -i 's/folder_path/caja-extension/' ../po/POTFILES.in

# debian
rm ../debian/postinst

sed -i '2d' ../debian/install
sed -i 's/nautilus/caja/g' ../debian/install

sed -i '25,44d' ../debian/copyright
sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-caja/' ../debian/copyright

sed -i 's/Source: folder-color/Source: folder-color-caja/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-caja/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python3-caja, caja, /' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color for Caja/' ../debian/control

sed -i 's/folder-color/folder-color-caja/' ../debian/changelog
if [ "$1" == "GTK3" ]; then
    sed -i 's/kinetic/focal/' ../debian/changelog
fi

# extension
sed -i 's/nautilus/caja/g' ../caja-extension/folder-color.py
sed -i 's/Nautilus/Caja/g' ../caja-extension/folder-color.py
sed -i "s/metadata::custom-icon-name/metadata::custom-icon/g" ../caja-extension/folder-color.py

sed -i 's/org.gnome.nautilus.icon-view/org.mate.caja.icon-view/g' ../caja-extension/folder-color.py
sed -i 's/default-zoom-level/default-zoom-level/g' ../caja-extension/folder-color.py
sed -i '57,72d' ../caja-extension/folder-color.py

# myself
rm -rf ../install-scripts

echo "Done"
