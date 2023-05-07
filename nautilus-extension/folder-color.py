# Folder Color 0.3.0 - https://github.com/costales/folder-color
# Copyright (C) 2012-2023 Marcos Alvarez Costales
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os, gettext
gi.require_version("Gtk", "4.0")
from gi.repository import Nautilus, Gtk, GObject, Gio, GLib
# Python 2/3
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
            'white'  : _("White"),
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

    def _get_skel_folder(self, folder, color):
        """Default directories"""
        skel_color = color

        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_DESKTOP):
            skel_color += '-desktop'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOCUMENTS):
            skel_color += '-documents'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD):
            skel_color += '-downloads'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_MUSIC):
            skel_color += '-music'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES):
            skel_color += '-pictures'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_PUBLIC_SHARE):
            skel_color += '-public'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_TEMPLATES):
            skel_color += '-templates'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_VIDEOS):
            skel_color += '-videos'

        # Not a default dir
        if skel_color == color:
            return color

        # Search
        skel_folder_color = self._get_icon_name(skel_color)
        if skel_folder_color['icon']:
            print(folder + " " + skel_folder_color['icon'])
            return skel_folder_color['icon']
        else:
            return color

    def _get_icon_name(self, icon_name):
        """Get icon name and filename"""
        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        icon = icon_theme.lookup_icon(icon_name, None, 48, 1, Gtk.TextDirection.LTR, Gtk.IconLookupFlags.FORCE_REGULAR)
        if icon_theme.has_icon(icon_name):
            return {'name'    : icon.get_icon_name(),
                    'filename': icon.get_file().get_uri()}
        else:
            return {'name': '',
                    'filename': ''}

    def set_colors_theme(self):
        """Available colors into system"""
        icon_options = ["folder-", "folder_color_", "folder_", "folder-", "folder_color_", "folder_"] # 3 iter for theme / 3 iter for hicolor
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

    def set_color(self, item, color):
        """Set color to a file/directory"""
        print(item + " " + color + " " + self._get_skel_folder(item, color))
        self._set_restore_folder(item) # Needs
        item_aux = Gio.File.new_for_path(item)
        info = item_aux.query_info('metadata::custom-icon-name', 0, None)
        info.set_attribute_string("metadata::custom-icon-name", self._get_skel_folder(item, color))
        item_aux.set_attributes_from_info(info, 0, None)
        self._reload_icon(item)
    
    def set_emblem(self, item, emblem):
        """Set emblem"""
        self._set_restore_emblem(item) # Needs
        emblem_aux = []
        emblem_aux.append(emblem)
        emblems = list(emblem_aux)
        emblems.append(None) # Needs
        item_aux = Gio.File.new_for_path(item)
        info = item_aux.query_info('metadata::emblems', 0, None)
        info.set_attribute_stringv('metadata::emblems', emblems)
        item_aux.set_attributes_from_info(info, 0, None)
        self._reload_icon(item)

    def set_restore(self, item):
        """Restore color/emblem to default"""
        self._set_restore_folder(item)
        self._set_restore_emblem(item)
        self._reload_icon(item)
 
    def _set_restore_folder(self, item):
        item_aux = Gio.File.new_for_path(item)
        info = item_aux.query_info('metadata::custom-icon-name', 0, None)
        info.set_attribute('metadata::custom-icon', Gio.FileAttributeType.INVALID, 0)
        info.set_attribute('metadata::custom-icon-name', Gio.FileAttributeType.INVALID, 0)
        item_aux.set_attributes_from_info(info, 0, None)

    def _set_restore_emblem(self, item):
        item_aux = Gio.File.new_for_path(item)
        info = item_aux.query_info('metadata::emblems', 0, None)
        info.set_attribute('metadata::emblems', Gio.FileAttributeType.INVALID, 0)
        item_aux.set_attributes_from_info(info, 0, None)

    def _reload_icon(self, item):
        """Reload the current file/directory icon"""
        os.utime(item, None)

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

    def get_file_items(self, items):
        """Click on directories or files"""
        if self._check_show_menu(items):
            return self._show_menu(items)

    def _check_show_menu(self, items):
        """Show the menu?"""
        self.all_files = True
        self.all_dirs = True

        if len(items) == 0:
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

        if len(colors) == 0 and len(emblems) == 0:
            return

        if self.all_dirs:
            # Title
            top_menuitem = Nautilus.MenuItem(name='FolderColorMenu::colors', label=_("Color"), icon='folder_color_picker')
            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)
            
            # Colors
            for color in colors.keys():
                item = Nautilus.MenuItem(name="FolderColorMenu::color_" + color, label=_(colors[color]), icon=color)
                item.connect('activate', self._menu_activate_color, items, color)
                submenu.append_item(item)
            
            # Separator if there are emblems
            if len(emblems) > 0:
                item = Nautilus.MenuItem(name='FolderColorMenu::emblems', label=_("Emblem:"), sensitive=False)
                submenu.append_item(item)
            
            # Emblems
            for emblem in emblems.keys():
                item = Nautilus.MenuItem(name="FolderColorMenu::emblem_" + emblem, label=_(emblems[emblem]), icon=emblem)
                item.connect('activate', self._menu_activate_emblem, items, emblem)
                submenu.append_item(item)
        
            # Restore
            if self._check_menu_restore(items):
                item = Nautilus.MenuItem(name='ChangeFolderEmblemMenu::separator', label=_("Restore:"), sensitive=False)
                submenu.append_item(item)
                item = Nautilus.MenuItem(name='FolderColorMenu::restore', label=_("Default"), icon='undo')
                item.connect('activate', self._menu_activate_restore, items)
                submenu.append_item(item)
        # Files
        else:
            # Title menu
            if len(emblems) > 0:
                top_menuitem = Nautilus.MenuItem(name='FolderColorMenu::emblems', label=_("Emblem"), icon='folder_color_picker')
                submenu = Nautilus.Menu()
                top_menuitem.set_submenu(submenu)

            # Emblems
            for emblem in emblems.keys():
                item = Nautilus.MenuItem(name="FolderColorMenu::emblem_" + emblem, label=_(emblems[emblem]), icon=emblem)
                item.connect('activate', self._menu_activate_emblem, items, emblem)
                submenu.append_item(item)
        
            # Restore
            if self._check_menu_restore(items):
                item_sep = Nautilus.MenuItem(name='ChangeFolderEmblemMenu::separator', label=_("Restore:"), sensitive=False)
                submenu.append_item(item_sep)
                item_restore = Nautilus.MenuItem(name='FolderColorMenu::restore', label=_("Default"), icon='undo')
                item_restore.connect('activate', self._menu_activate_restore, items)
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
            if info.get_attribute_as_string('metadata::custom-icon-name') or \
               info.get_attribute_as_string('metadata::custom-icon') or \
               info.get_attribute_as_string('metadata::emblems'):
                return True
        return False

    def _menu_activate_color(self, menu, items, color):
        """Menu: Clicked color"""
        for item in items:
            if item.is_gone():
                continue
            self.foldercolor.set_color(unquote(item.get_uri()[7:]), color)

    def _menu_activate_emblem(self, menu, items, emblem):
        """Menu: Clicked emblem"""
        for item in items:
            if item.is_gone():
                continue
            self.foldercolor.set_emblem(unquote(item.get_uri()[7:]), emblem)

    def _menu_activate_restore(self, menu, items):
        """Menu: Clicked restore"""
        for item in items:
            if item.is_gone():
                continue
            self.foldercolor.set_restore(unquote(item.get_uri()[7:]))
