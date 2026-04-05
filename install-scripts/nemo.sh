#!/bin/bash

rm -rf ../.git
rm ../README.md

# setup
sed -i '17,29d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/nautilus/nemo/g' ../setup.py
sed -i 's/"folder-color"/"folder-color-nemo"/' ../setup.py

# po
sed -i 's/folder_i18n/folder-color-nemo/' ../extension-GTK3/folder-color.py
sed -i 's/folder_i18n/folder-color-nemo/' ../extension-GTK4/folder-color.py
sed -i 's/folder_i18n/folder-color-nemo/' ../po/POTFILES.in
sed -i 's/folder_path/nemo-extension/' ../po/POTFILES.in

# debian
sed -i 's/"folder-color"/"folder-color-nemo"/' ../debian/changelog
sed -i 's/"folder-color"/"folder-color-nemo"/' ../debian/control
sed -i 's/"folder-color"/"folder-color-nemo"/' ../debian/copyright
sed -i 's/nautilus/nemo/g' ../debian/prerm

# extension
sed -i 's/nautilus/nemo/g' ../nemo-extension/folder-color.py
sed -i 's/Nautilus/Nemo/g' ../nemo-extension/folder-color.py

# myself
rm -rf ../install-scripts

echo "Done"
