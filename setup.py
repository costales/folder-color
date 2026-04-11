#!/usr/bin/env python3

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os, glob, DistUtilsExtra.auto

def get_data_files(src_root, dst_root):
    data_files = []
    for root, dirs, files in os.walk(src_root):
        if files:
            src_files = [os.path.join(root, f) for f in files]
            rel_path = os.path.relpath(root, src_root)
            dst_path = os.path.join(dst_root, rel_path)
            data_files.append((dst_path, src_files))
    return data_files

data = []

# Copy icons/ into /usr/share/icons/
data += get_data_files('icons', '/usr/share/icons')

# Copy extension into /usr/share/nautilus-python/extensions
data.append((
    '/usr/share/nautilus-python/extensions',
    ['extension/folder-color.py']
))

DistUtilsExtra.auto.setup(
    name="folder-color",
    version="0.4.2",
    description="Change your folder color with just a click",
    author="Marcos Alvarez Costales",
    author_email="marcos.costales@gmail.com",
    url="https://github.com/costales/folder-color",
    license="GPL3",
    data_files=data
)