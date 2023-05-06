Folder Color © 2012-2023 Marcos Alvarez Costales
================================================

WHAT IS IT?
===========
A file browser extension for choosing the color of a folder.




HOW DO I INSTALL & RUN IT?
==========================
From a PPA:
    # add-apt-repository ppa:costales/folder-color
    # apt-get update && sudo apt-get install folder-color
From the code (take a look to the dependencies):
    $ bzr branch lp:folder-color && cd folder-color && sudo python3 setup.py install --prefix=/usr

Then, restart Nautilus
    $ nautilus -q
You'll need also to refresh the system icons:
    # gtk-update-icon-cache /usr/share/icons/Humanity/

    


DEPENDENCIES
============
For Nautilus:
    python3-nautilus, nautilus
For Nemo:
    python-nemo, nemo
For Caja:
    python3-caja, caja


    

HOW TO CREATE A NEW THEME
=========================

HOW TO CREATE A NEW THEME
=========================
Folder color will work (you'll see the entry menu) if AT LEAST exists the icon: "blue-color".
You can use any compatible icon format (like SVG or PNG).



1. FOLDER COLORS (MANDATORY)
Icon nomenclature: folder-<color>.
<color>: brown, blue, green, grey, orange, pink, red, purple, yellow, cyan, black, violet, magenta

The unique mandatory color is blue in size 48px. The other are optionals.

For example: Blue folder color would be: /usr/share/icons/<MyAwesomeTheme>/48x48/<places>/folder-blue.svg

OTHER ICONS:
The entries menu will use these icons from the default theme: undo



2. DEFAULT FOLDERS (OPTIONAL)
These folders have icons inside. They are: Desktop, Documents, Downloads, Music, Pictures, Public, Templates, Videos.

Icon nomenclature: folder-<color>-<emblem>
<color>: brown, blue, green, grey, orange, pink, red, purple, yellow, cyan, black, violet, magenta
<emblem>: desktop, documents, downloads, music, pictures, public, templates, videos

For example, the blue 'Pictures' folder would be: /usr/share/icons/<MyAwesomeTheme>/48x48/<places>/folder-blue-pictures.svg



3. EMBLEMS (OPTIONAL)
Folder Color will use any of these standard emblems from the current theme:
 - emblem-favorite
 - emblem-important
 - emblem-new
 - emblem-urgent



4. ALL RESOLUTIONS (OPTIONAL)
Reply the previous sections for all resolutions (not only 48px) in points 1, 2 and 3.








HOW TO CHECK YOUR NEW THEME?
Copy your icons into:
    ~/.icons/<your_theme>/
After install them, remember to refresh your theme:
    # gtk-update-icon-cache ~/.icons/<your_theme>
Set your theme as default system theme.
And restart your file browser:
    $ [nautilus|caja|nemo] -q




MY PERSONAL RECOMMENDATION
Make all the icons is a really big work.
I'd recommend you to create just the icons of point 1. If you are full of beans, create the others.




DOUBTS?
Do you have any doubt or problem? Contact me here: https://costales.github.io/
I'll try to help you :)





LICENSES
====================
Folder Color code is licensed under the GPL v3.
http://www.gnu.org/licenses
See file LICENSE.txt for the complete license.
