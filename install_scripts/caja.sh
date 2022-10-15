#!/bin/bash
rm -r ../icons
rm -r ../po
rm ../README

# setup
sed -i '25,34d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/Change your folder color with just a click/Change your folder color in Caja/' ../setup.py
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
sed -i 's/red   = (color.red   \* 255)/red   = int(color.red   \/ 256)/g' ../caja-extension/folder-color.py
sed -i 's/green = (color.green \* 255)/green = int(color.green \/ 256)/g' ../caja-extension/folder-color.py
sed -i 's/blue  = (color.blue  \* 255)/blue  = int(color.blue  \/ 256)/g' ../caja-extension/folder-color.py


# debian
rm ../debian/postinst

sed -i '2d' ../debian/install
sed -i 's/nautilus/caja/g' ../debian/install

sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-caja/' ../debian/copyright
sed -i '25,44d' ../debian/copyright

sed -i 's/Source: folder-color/Source: folder-color-caja/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-caja/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python-caja, caja, folder-color-common, /' ../debian/control
sed -i '14,15d' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color for Caja/' ../debian/control
sed -i 's/Change a folder color used in Nautilus/Change a folder color used in Caja/' ../debian/control

sed -i 's/folder-color/folder-color-caja/' ../debian/changelog

# me
rm -r ../install_scripts

