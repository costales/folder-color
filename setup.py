#!/usr/bin/env python3

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os, sys, glob, DistUtilsExtra.auto

# Create data files
data = [ ('/usr/share/nautilus-python/extensions',   ['nautilus-extension/folder-color.py']),
         ('/usr/share/icons/hicolor/16x16/actions',  glob.glob('icons/hicolor/16x16/actions/*.svg')),
         ('/usr/share/icons/Yaru/16x16/places',      glob.glob('icons/Yaru/16x16/places/*.png')),
         ('/usr/share/icons/Yaru/16x16@2x/places',   glob.glob('icons/Yaru/16x16@2x/places/*.png')),
         ('/usr/share/icons/Yaru/22x22/places',      glob.glob('icons/Yaru/22x22/places/*.png')),
         ('/usr/share/icons/Yaru/22x22@2x/places',   glob.glob('icons/Yaru/22x22@2x/places/*.png')),
         ('/usr/share/icons/Yaru/24x24/places',      glob.glob('icons/Yaru/24x24/places/*.png')),
         ('/usr/share/icons/Yaru/24x24@2x/places',   glob.glob('icons/Yaru/24x24@2x/places/*.png')),
         ('/usr/share/icons/Yaru/32x32/places',      glob.glob('icons/Yaru/32x32/places/*.png')),
         ('/usr/share/icons/Yaru/32x32@2x/places',   glob.glob('icons/Yaru/32x32@2x/places/*.png')),
         ('/usr/share/icons/Yaru/48x48/places',      glob.glob('icons/Yaru/48x48/places/*.png')),
         ('/usr/share/icons/Yaru/48x48@2x/places',   glob.glob('icons/Yaru/48x48@2x/places/*.png')),
         ('/usr/share/icons/Yaru/256x256/places',    glob.glob('icons/Yaru/256x256/places/*.png')),
         ('/usr/share/icons/Yaru/256x256@2x/places', glob.glob('icons/Yaru/256x256@2x/places/*.png')) ]

# Setup stage
DistUtilsExtra.auto.setup(
    name         = "folder-color",
    version      = "0.4.1",
    description  = "Change your folder color with just a click",
    author       = "Marcos Alvarez Costales",
    author_email = "marcos.costales@gmail.com",
    url          = "https://github.com/costales/folder-color",
    license      = "GPL3",
    data_files   = data
)

