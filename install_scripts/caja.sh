#!/bin/bash
rm ../README*
rm -rf ../nautilus-extension-gtk3
rm -rf ../.git

# setup
sed -i 's/nautilus-python/caja-python/' ../setup.py
sed -i 's/nautilus-extension/caja-extension/' ../setup.py
sed -i 's/"folder-color"/"folder-color-caja"/' ../setup.py

# extension
mv ../nautilus-extension/ ../caja-extension
sed -i 's/nautilus/caja/g' ../caja-extension/folder-color.py
sed -i 's/Nautilus/Caja/g' ../caja-extension/folder-color.py
sed -i 's/is_uri=False/is_uri=True/' ../caja-extension/folder-color.py
sed -i "s/self.foldercolor.set_color(item_path, self._get_skel_folder(item_path, icon)\['name'\])/self.foldercolor.set_color(item_path, self._get_skel_folder(item_path, icon)\['filename'\], True)/" ../caja-extension/folder-color.py
sed -i 's/Gtk.ColorChooserDialog()/Gtk.ColorSelectionDialog()/g' ../caja-extension/folder-color.py
sed -i 's/dialog.set_use_alpha(False)//g' ../caja-extension/folder-color.py
sed -i 's/color = dialog.get_rgba()/color = dialog.get_color_selection().get_current_color()/g' ../caja-extension/folder-color.py

# po
sed -i 's/folder_i18n/folder-color-caja/' ../caja-extension/folder-color.py
sed -i 's/folder_i18n/folder-color-caja/' ../po/POTFILES.in
sed -i 's/folder_path/caja-extension/' ../po/POTFILES.in

# debian
sed -i 's/nautilus/caja/g' ../debian/install

sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-caja/' ../debian/copyright

sed -i 's/Source: folder-color/Source: folder-color-caja/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-caja/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python3-caja, caja, /' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color for Caja/' ../debian/control

sed -i 's/folder-color/folder-color-caja/' ../debian/changelog

# me
rm -rf ../install_scripts
