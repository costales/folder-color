# Folder Color 0.3.0 - https://github.com/costales/folder-color Copyright (C) 2012-2023 Marcos Alvarez Costales
#
# Folder Color is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
# Folder Color is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Folder Color; if not, see http://www.gnu.org/licenses for more information.

import os, gettext
from gi.repository import Nautilus, Gtk, GObject, Gio

# Python 2 or 3
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

# i18n
gettext.textdomain('folder_i18n')
_ = gettext.gettext


class FolderColor:
    """Folder Color Class"""
    def __init__(self):
        self.COLORS_ALL = {
            'black'  : _("Black"),
            'blue'   : _("Blue"),
            'brown'  : _("Brown"),
            'cyan'   : _("Cyan"),
            'green'  : _("Green"),
            'grey'   : _("Grey"),
            'magenta': _("Magenta"),
            'orange' : _("Orange"),
            'pink'   : _("Pink"),
            'purple' : _("Purple"),
            'red'    : _("Red"),
            'violet' : _("Violet"),
            'yellow' : _("Yellow")
        }
        self.EMBLEMS_ALL = {
            'emblem-important': _("Important"),
            'emblem-urgent'   : _("In Progress"),
            'emblem-favorite' : _("Favorite"),
            'emblem-default'  : _("Finished"),
            'emblem-new'      : _("New")
        }
        self.colors = {}
        self.emblems = {}

    def _get_icon_name(self, icon_name):
        """Get icon name and filename"""
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.lookup_icon(icon_name, 48, 0)
        if icon is None:
            return {'icon': '',
                    'filename': ''}
        else:
            return {'icon': os.path.splitext(os.path.basename(icon.get_filename()))[0],
                    'filename': icon.get_filename()}

    def set_colors_theme(self):
        """Available colors into system"""
        icon_options = ["folder-", "folder_color_", "folder_", "folder-", "folder_color_", "folder_"] # 3 for theme / 3 for hicolor
        for color in self.COLORS_ALL.keys():
            for i, option in enumerate(icon_options):
                icon_aux = self._get_icon_name(option+color)
                # Theme priority
                if i < 3 and icon_aux['icon'] and '/hicolor/' not in icon_aux['filename']:
                    self.colors[icon_aux['icon']] = self.COLORS_ALL[color]
                    continue
                # hicolor by default
                if i >= 3 and icon_aux['icon']:
                    self.colors[icon_aux['icon']] = self.COLORS_ALL[color]
                    continue

    def set_emblems_theme(self):
        """Available emblems into system"""
        for emblem in self.EMBLEMS_ALL.keys():
            icon = self._get_icon_name(emblem)
            if not icon['icon']:
                continue
            self.emblems[icon['icon']] = self.EMBLEMS_ALL[emblem]

    def get_colors_theme(self):
        return self.colors

    def get_emblems_theme(self):
        return self.emblems

class FolderColorMenu(GObject.GObject, Nautilus.MenuProvider):
    """File Browser Menu"""
    def __init__(self):
        GObject.Object.__init__(self)
        self.all_files = True
        self.all_dirs = True
        self.foldercolor = FolderColor()
        self.foldercolor.set_colors_theme()
        self.foldercolor.set_emblems_theme()
        print(self.foldercolor.get_colors_theme())
        print(self.foldercolor.get_emblems_theme())

    def get_file_items(self, window, items):
        """Click on directories or files"""
        if not self._check_show_menu(items):
            return

        print("show menu")
        return self._show_menu(items)

    def _check_show_menu(self, items):
        """Show the menu?"""
        self.all_files = True
        self.all_dirs = True

        if not len(items):
            return False
        
        for item in items:
            # GNOME can only handle files
            if item.get_uri_scheme() != 'file':
                return False

            if item.is_directory():
                self.all_files = False
            else:
                self.all_dirs = False

            if not self.all_files and not self.all_dirs:
                return False
        
        return True

    def _show_menu(self, items):
        """Menu for [directories|files]: [Color,Restore,Emblems|Emblems,Restore]"""
        # Directories
        colors = self.foldercolor.get_colors_theme()
        emblems = self.foldercolor.get_emblems_theme()
        if self.all_dirs:
            # Title
            top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Color"), icon='folder_color_picker')
            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)
            
            # Colors
            for color in colors.keys():
                name = ''.join(['ChangeFolderColorMenu::Colors"', color, '"'])
                item = Nautilus.MenuItem(name=name, label=_(colors[color]), icon=color)
                item.connect('activate', self._menu_activate_color, items, color)
                submenu.append_item(item)
            
            # Separator if there are emblems
            if len(self.foldercolor.get_emblems_theme()):
                item_sep = Nautilus.MenuItem(name='ChangeFolderColorMenu::Sep1', label=_("Emblem:"), sensitive=False)
                submenu.append_item(item_sep)
            
            # Emblems
            for emblem in emblems.keys():
                name = ''.join(['ChangeFolderColorMenu::Colors"', emblem, '"'])
                item = Nautilus.MenuItem(name=name, label=_(emblems[emblem]), icon=emblem)
                item.connect('activate', self._menu_activate_emblem, items, emblem)
                submenu.append_item(item)
        
            # Restore
            if self._check_menu_restore(items):
                item_sep = Nautilus.MenuItem(name='ChangeFolderEmblemMenu::Sep', label=_("Restore:"), sensitive=False)
                submenu.append_item(item_sep)
                item_restore = Nautilus.MenuItem(name='ChangeFolderColorMenu::Restore', label=_("Default"), icon='undo')
                item_restore.connect('activate', self._menu_activate_restore_all, items)
                submenu.append_item(item_restore)
            
        # Files
        else:
            # Title menu
            top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Emblem"), icon='folder_color_picker')
            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)

            # Emblems
            for emblem in emblems.keys():
                name = ''.join(['ChangeFolderColorMenu::Colors"', emblem, '"'])
                item = Nautilus.MenuItem(name=name, label=_(emblems[emblem]), icon=emblem)
                item.connect('activate', self._menu_activate_emblem, items, emblem)
                submenu.append_item(item)
        
            # Restore
            if self._check_menu_restore(items):
                item_sep = Nautilus.MenuItem(name='ChangeFolderEmblemMenu::Sep', label=_("Restore:"), sensitive=False)
                submenu.append_item(item_sep)
                item_restore = Nautilus.MenuItem(name='ChangeFolderColorMenu::Restore', label=_("Default"), icon='undo')
                item_restore.connect('activate', self._menu_activate_restore_emblem, items)
                submenu.append_item(item_restore)

        return top_menuitem,

    def _check_menu_restore(self, items):
        """Menu: Show restore?"""
        # For each dir, search custom icon or emblem
        for item in items:
            # Get metadata file/folder
            item_path = unquote(item.get_uri()[7:])
            item = Gio.File.new_for_path(item_path)
            info = item.query_info('metadata', 0, None)
            # If any metadata > restore menu
            if info.get_attribute_as_string('metadata::custom-icon-name') or info.get_attribute_as_string('metadata::custom-icon') or info.get_attribute_as_string('metadata::emblems'):
                return True
        return False

    def _menu_activate_color(self, menu, items, color):
        print(items)
        print(color)
    def _menu_activate_emblem(self, menu, items, emblem):
        print(items)
        print(emblem)
    def _menu_activate_restore_all(self, menu, items):
        print(items)
    def _menu_activate_restore_emblem(self, menu, items):
        print(items)
        