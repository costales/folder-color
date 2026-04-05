#!/bin/bash

rm -rf ../.git
rm ../README.md
rm -r ../icons

# setup
sed -i '17,29d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/nautilus/caja/g' ../setup.py
sed -i 's/"folder-color"/"folder-color-caja"/' ../setup.py

# po
sed -i 's/folder_i18n/folder-color-caja/' ../extension-GTK3/folder-color.py
sed -i 's/folder_i18n/folder-color-caja/' ../extension-GTK4/folder-color.py
sed -i 's/folder_i18n/folder-color-caja/' ../po/POTFILES.in
sed -i 's/folder_path/caja-extension/' ../po/POTFILES.in

# debian
sed -i 's/folder-color/folder-color-caja/' ../debian/changelog
sed -i 's/folder-color/folder-color-caja/' ../debian/copyright

sed -i 's/Source: folder-color/Source: folder-color-caja/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-caja/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python3-caja, caja, /' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color for Caja/' ../debian/control

sed -i 's/nautilus/caja/g' ../debian/prerm

# extension
sed -i 's/nautilus/caja/g' ../extension-GTK3/folder-color.py
sed -i 's/Nautilus/Caja/g' ../extension-GTK3/folder-color.py
sed -i "s/metadata::custom-icon-name/metadata::custom-icon/g" ../extension-GTK3/folder-color.py
sed -i 's/nautilus/caja/g' ../extension-GTK4/folder-color.py
sed -i 's/Nautilus/Caja/g' ../extension-GTK4/folder-color.py
sed -i "s/metadata::custom-icon-name/metadata::custom-icon/g" ../extension-GTK4/folder-color.py

# myself
rm -rf ../install-scripts

echo "Done"
