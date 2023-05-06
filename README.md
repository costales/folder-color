# Folder Color for Linux

A file browser extension for choosing the color/emblems of a folder/files in Linux (Nautilus/Nemo/Caja file browsers).

# INSTALL

With Nautilus:

```
# add-apt-repository ppa:costales/folder-color
# apt-get update
# sudo apt install python3-nautilus nautilus
# sudo apt-get install folder-color
# gtk-update-icon-cache /usr/share/icons/Yaru/
$ nautilus -q
```

With Nemo:

```
# add-apt-repository ppa:costales/folder-color
# apt-get update
# sudo apt install python-nemo nemo
# sudo apt-get install folder-color-nemo
# gtk-update-icon-cache /usr/share/icons/Yaru/
$ nemo -q
```

With Caja:

```
# add-apt-repository ppa:costales/folder-color
# apt-get update
# sudo apt install python3-caja caja
# sudo apt-get install folder-color-caja
# gtk-update-icon-cache /usr/share/icons/Yaru/
$ caja -q
```

# LICENSES

Folder Color, (Yaru-Colors)[https://github.com/Jannomag/Yaru-Colors] & (Yaru icons)[https://github.com/ubuntu/yaru] are licensed under the GPL v3.

See file LICENSE.txt for the complete terms.


# CREATE A NEW THEME
=========================

Are you an icon designer? Let's see how to create an icon theme compatible with Folder Color.

### 1. FOLDER COLORS

File name: `folder-<color>.svg` or `folder-<color>.png`.

`<color>` can be:

 * `blue` (Mandatory)
 * `black`
 * `brown`
 * `cyan`
 * `green`
 * `grey`
 * `magenta`
 * `orange`
 * `pink`
 * `purple`
 * `red`
 * `violet`
 * `white`
 * `yellow`

Folder color will work (you'll see the entry menu) if AT LEAST exists the icon: "folder-blue".

Final filename path:

```
/usr/share/icons/MyAwesomeTheme/48x48/places/folder-blue.svg
/usr/share/icons/MyAwesomeTheme/48x48/places/folder-green.svg
```

The entries menu will use this icon name from the default theme: `undo`.


## 2. DEFAULT FOLDERS (OPTIONAL)

These folders have emblems inside.

They could be:

 * `desktop`
 * `documents`
 * `downloads`
 * `music`
 * `pictures`
 * `public`
 * `templates`
 * `videos`

Icon nomenclature: folder-<color>-<emblem>

Final filename path:

```
/usr/share/icons/MyAwesomeTheme/48x48/places/folder-blue-desktop.svg
/usr/share/icons/MyAwesomeTheme/48x48/places/folder-blue-documents.svg
```


## 3. EMBLEMS (OPTIONAL)

Folder Color will use any of these standard emblems:

 * `emblem-important`
 * `emblem-urgent`
 * `emblem-favorite`
 * `emblem-default`
 * `emblem-new`

## 4. ALL RESOLUTIONS (OPTIONAL)

Reply the previous sections for all resolutions (not only 48px) in points 1, 2 and 3.


## 5. CHECK

Copy your icons into: `~/.icons/<your_theme>/`.

After install them, remember to refresh your theme:

```
$ gtk-update-icon-cache `~/.icons/<your_theme>`
```

Set your theme as default system theme.

Restart your file browser:

```
$ [nautilus|caja|nemo] -q
```

