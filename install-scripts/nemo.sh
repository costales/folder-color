#!/bin/bash
rm ../README*
rm -rf ../nautilus-extension-gtk3
rm -rf ../.git
rm -r ../icons

# setup
sed -i '17,26d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/nautilus/nemo/g' ../setup.py
sed -i 's/"folder-color"/"folder-color-nemo"/' ../setup.py

# extension
mv ../nautilus-extension/ ../nemo-extension
sed -i 's/nautilus/nemo/g' ../nemo-extension/folder-color.py
sed -i 's/Nautilus/Nemo/g' ../nemo-extension/folder-color.py

# po
sed -i 's/folder_i18n/folder-color-nemo/' ../nemo-extension/folder-color.py
sed -i 's/folder_i18n/folder-color-nemo/' ../po/POTFILES.in
sed -i 's/folder_path/nemo-extension/' ../po/POTFILES.in

# debian
rm ../debian/postinst

sed -i '2d' ../debian/install
sed -i 's/nautilus/nemo/g' ../debian/install

sed -i '25,44d' ../debian/copyright
sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-nemo/' ../debian/copyright

sed -i 's/Source: folder-color/Source: folder-color-nemo/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-nemo/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python-nemo, nemo, /' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color for Nemo/' ../debian/control

sed -i 's/folder-color/folder-color-nemo/' ../debian/changelog

# me
rm -rf ../install_scripts
