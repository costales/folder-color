#!/usr/bin/env python3

# Folder Color 0.3.0 - https://github.com/costales/folder-color
# Copyright (C) 2012-2022 Marcos Alvarez Costales - https://costales.github.io/
#
# folder-color is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# Folder Color is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Folder Color; if not, see http://www.gnu.org/licenses 
# for more information.


import os, sys, glob, DistUtilsExtra.auto

# Create data files
data = [ ('/usr/share/nautilus-python/extensions',   ['nautilus-extension/folder-color.py']),
         ('/usr/share/icons/Yaru/16x16/places',      glob.glob('icons/Yaru/16x16/places/*.svg')),
         ('/usr/share/icons/Yaru/16x16@2x/places',   glob.glob('icons/Yaru/16x16@2x/places/*.svg')),
         ('/usr/share/icons/Yaru/24x24/places',      glob.glob('icons/Yaru/24x24/places/*.svg')),
         ('/usr/share/icons/Yaru/24x24@2x/places',   glob.glob('icons/Yaru/24x24@2x/places/*.svg')),
         ('/usr/share/icons/Yaru/32x32/places',      glob.glob('icons/Yaru/32x32/places/*.svg')),
         ('/usr/share/icons/Yaru/32x32@2x/places',   glob.glob('icons/Yaru/32x32@2x/places/*.svg')),
         ('/usr/share/icons/Yaru/48x48/places',      glob.glob('icons/Yaru/48x48/places/*.svg')),
         ('/usr/share/icons/Yaru/48x48@2x/places',   glob.glob('icons/Yaru/48x48@2x/places/*.svg')),
         ('/usr/share/icons/Yaru/256x256/places',    glob.glob('icons/Yaru/256x256/places/*.svg')),
         ('/usr/share/icons/Yaru/256x256@2x/places', glob.glob('icons/Yaru/256x256@2x/places/*.svg')) ]

# Setup stage
DistUtilsExtra.auto.setup(
    name         = "folder-color",
    version      = "0.3.0",
    description  = "Change your folder color with just a click",
    author       = "Marcos Alvarez Costales",
    author_email = "marcos.costales@gmail.com",
    url          = "https://github.com/costales/folder-color",
    license      = "GPL3",
    data_files   = data
)

