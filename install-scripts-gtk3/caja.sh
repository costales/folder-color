#!/bin/bash

# GTK4
rm -rf ../nautilus-extension
rm -rf ../install-scripts

mv ../nautilus-extension-gtk3 ../nautilus-extension

rm -rf ../.git
rm ../README.md
rm -r ../icons

# setup
sed -i '17,26d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/nautilus/caja/' ../setup.py
sed -i 's/"folder-color"/"folder-color-caja"/' ../setup.py

# extension
mv ../nautilus-extension/ ../caja-extension
sed -i 's/nautilus/caja/g' ../caja-extension/folder-color.py
sed -i 's/Nautilus/Caja/g' ../caja-extension/folder-color.py
sed -i "s/metadata::custom-icon-name/metadata::custom-icon/g" ../caja-extension/folder-color.py
sed -i "s/self._get_skel_folder(item, color)/'file:\/\/'+self._get_icon_name(color)['filename']/g" ../caja-extension/folder-color.py

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

# myself
rm -rf ../install-scripts-gtk3
