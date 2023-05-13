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

import os, gettext, gi
gi.require_version("Gtk", "3.0")
from gi.repository import Nautilus, Gtk, GObject, Gio, GLib
try:
    from urllib import unquote # python 3
except ImportError:
    from urllib.parse import unquote # python 2

# i18n
gettext.textdomain("folder_i18n")
_ = gettext.gettext

COLORS_ALL = {
    "black": _("Black"),
    "blue": _("Blue"),
    "brown": _("Brown"),
    "cyan": _("Cyan"),
    "green": _("Green"),
    "grey": _("Grey"),
    "magenta": _("Magenta"),
    "orange": _("Orange"),
    "pink": _("Pink"),
    "purple": _("Purple"),
    "red": _("Red"),
    "violet": _("Violet"),
    "white": _("White"),
    "yellow": _("Yellow")
}
EMBLEMS_ALL = {
    "emblem-important": _("Important"),
    "emblem-urgent": _("In Progress"),
    "emblem-favorite": _("Favorite"),
    "emblem-default": _("Finished"),
    "emblem-new": _("New")
}
USER_DIRS = {
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_DESKTOP): "-desktop",
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOCUMENTS): "-documents",
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD): "-downloads",
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_MUSIC): "-music",
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES): "-pictures",
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_PUBLIC_SHARE): "-public",
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_TEMPLATES): "-templates",
    GLib.get_user_special_dir(GLib.USER_DIRECTORY_VIDEOS): "-videos"
}
ICON_SIZE = 48

class FolderColor:
    """Folder Color Class"""
    def __init__(self):
        self.is_modified = False
        self.colors = []
        self.emblems = []

    def _get_skel_folder(self, folder, color):
        """Default directories"""
        if folder in USER_DIRS:
            # Check icon for default folder
            skel_color = color + USER_DIRS[folder]
            if "_" in color: # Legacy themes
                skel_color = skel_color.replace("-", "_")
            if self._get_icon_name(skel_color):
                return skel_color
        return color

    def _get_icon_name(self, icon_name):
        """Get icon name and filename"""
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.lookup_icon(icon_name, ICON_SIZE, 0)
        if icon is not None:
            return {"icon": os.path.splitext(os.path.basename(icon.get_filename()))[0], "filename": icon.get_filename()}
        else:
            return {"icon": "", "filename": ""}

    def set_colors_theme(self):
        """Available colors into system"""
        self.colors.clear()
        icon_options = ["folder-", "folder_color_", "folder_", "folder-", "folder_color_", "folder_"] # 3 iter for theme / 3 iter for hicolor
        for color in COLORS_ALL.keys():
            for i, option in enumerate(icon_options):
                icon_aux = self._get_icon_name(option+color)
                # Theme priority
                if i < 3 and icon_aux["icon"] and not "/hicolor/" in icon_aux["filename"]:
                    self.colors.append({"icon": icon_aux["icon"], "label": COLORS_ALL[color], "uri": icon_aux["filename"]})
                    break
                # hicolor by default
                if i >= 3 and icon_aux["icon"]:
                    self.colors.append({"icon": icon_aux["icon"], "label": COLORS_ALL[color], "uri": icon_aux["filename"]})
                    break

    def set_emblems_theme(self):
        """Available emblems into system"""
        self.emblems.clear()
        for emblem in EMBLEMS_ALL.keys():
            icon_aux = self._get_icon_name(emblem)
            if icon_aux["icon"]:
                self.emblems.append({"icon": icon_aux["icon"], "label": EMBLEMS_ALL[emblem], "uri": icon_aux["filename"]})

    def get_colors_theme(self):
        return self.colors

    def get_emblems_theme(self):
        return self.emblems

    def set_color(self, item, color):
        if self.is_modified:
            self._set_restore_folder(item)
        item_aux = Gio.File.new_for_path(item)
        # TODO info = item_aux.query_info("metadata::custom-icon-name", 0, None)
        # TODO info.set_attribute_string("metadata::custom-icon-name", # TODO self._get_skel_folder(item, color["icon"]))
        # TODO item_aux.set_attributes_from_info(info, 0, None)
        self._reload_icon(item)
    
    def set_emblem(self, item, emblem):
        emblem_aux = []
        emblem_aux.append(emblem["icon"])
        emblems = list(emblem_aux)
        emblems.append(None) # Needs
        item_aux = Gio.File.new_for_path(item)
        info = item_aux.query_info("metadata::emblems", 0, None)
        info.set_attribute_stringv("metadata::emblems", emblems)
        item_aux.set_attributes_from_info(info, 0, None)
        self._reload_icon(item)

    def set_restore(self, item):
        self._set_restore_folder(item)
        self._set_restore_emblem(item)
        self._reload_icon(item)
 
    def _set_restore_folder(self, item):
        item_aux = Gio.File.new_for_path(item)
        info = item_aux.query_info("metadata::custom-icon-name", 0, None)
        info.set_attribute("metadata::custom-icon", Gio.FileAttributeType.INVALID, 0)
        info.set_attribute("metadata::custom-icon-name", Gio.FileAttributeType.INVALID, 0)
        item_aux.set_attributes_from_info(info, 0, None)

    def _set_restore_emblem(self, item):
        item_aux = Gio.File.new_for_path(item)
        info = item_aux.query_info("metadata::emblems", 0, None)
        info.set_attribute("metadata::emblems", Gio.FileAttributeType.INVALID, 0)
        item_aux.set_attributes_from_info(info, 0, None)

    def _reload_icon(self, item):
        os.utime(item, None)

    def get_is_modified(self, items):
        """Restore is enabled?"""
        # For each dir, search custom icon or emblem
        for item in items:
            # Get metadata file/folder
            item_path = unquote(item.get_uri()[7:])
            item = Gio.File.new_for_path(item_path)
            info = item.query_info("metadata", 0, None)
            # If any metadata then restore menu
            if info.get_attribute_as_string("metadata::custom-icon-name") or \
               info.get_attribute_as_string("metadata::custom-icon") or \
               info.get_attribute_as_string("metadata::emblems"):
                self.is_modified = True
                return True
        self.is_modified = False
        return False

class FolderColorMenu(GObject.GObject, Nautilus.MenuProvider):
    """File Browser Menu"""
    def __init__(self):
        GObject.Object.__init__(self)
        self.all_files = True
        self.all_dirs = True
        self.foldercolor = FolderColor()
        self.theme = Gtk.Settings.get_default().get_property("gtk-icon-theme-name")
        self._load_theme()
        # Read available icons only at Nautilus startup

    def get_file_items(self, window, items):
        """Click on directories or files"""
        if self._check_show_menu(items):
            if self.theme != Gtk.Settings.get_default().get_property("gtk-icon-theme-name"):
                self.theme = Gtk.Settings.get_default().get_property("gtk-icon-theme-name")
                self._load_theme()
            return self._show_menu(items)

    def _load_theme(self):
        self.foldercolor.set_colors_theme()
        self.foldercolor.set_emblems_theme()

    def _check_show_menu(self, items):
        self.all_files = True
        self.all_dirs = True

        if not items:
            return False
        
        for item in items:
            # GNOME can only handle files
            if item.get_uri_scheme() != "file":
                return False

            if item.is_directory():
                self.all_files = False
            else:
                self.all_dirs = False

            if not self.all_files and not self.all_dirs:
                return True
        
        return True

    def _show_menu(self, items):
        """Menu for [directories|files]: [Color,Restore,Emblems|Emblems,Restore]"""
        # Directories
        colors = self.foldercolor.get_colors_theme()
        emblems = self.foldercolor.get_emblems_theme()
        is_modified = self.foldercolor.get_is_modified(items)

        # Main menu
        if self.all_dirs and colors:
            top_menuitem = Nautilus.MenuItem(name="FolderColorMenu::colors", label=_("Color"), icon="color-picker")
        elif emblems:
            top_menuitem = Nautilus.MenuItem(name="FolderColorMenu::colors", label=_("Emblem"), icon="color-picker")
        else:
            return
        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        # Colors
        if self.all_dirs:
            for color in colors:
                item = Nautilus.MenuItem(name="FolderColorMenu::color_" + color["icon"], label=color["label"], icon=color["icon"])
                item.connect("activate", self._menu_activate_color, items, color)
                submenu.append_item(item)
        # Emblems
        if emblems:
            if self.all_dirs and colors:
                item = Nautilus.MenuItem(name="FolderColorMenu::emblems", label="―――", sensitive=False)
                submenu.append_item(item)
            for emblem in emblems:
                item = Nautilus.MenuItem(name="FolderColorMenu::emblem_" + emblem["icon"], label=emblem["label"], icon=emblem["icon"])
                item.connect("activate", self._menu_activate_emblem, items, emblem)
                submenu.append_item(item)
        # Restore
        if is_modified:
            item = Nautilus.MenuItem(name="ChangeFolderEmblemMenu::separator", label="―――", sensitive=False)
            submenu.append_item(item)
            item = Nautilus.MenuItem(name="FolderColorMenu::restore", label=_("Default"), icon="undo")
            item.connect("activate", self._menu_activate_restore, items)
            submenu.append_item(item)

        return top_menuitem,

    def _menu_activate_color(self, menu, items, color):
        """Menu: Clicked color"""
        for item in items:
            if not item.is_gone():
                self.foldercolor.set_color(unquote(item.get_uri()[7:]), color)

    def _menu_activate_emblem(self, menu, items, emblem):
        """Menu: Clicked emblem"""
        for item in items:
            if not item.is_gone():
                self.foldercolor.set_emblem(unquote(item.get_uri()[7:]), emblem)

    def _menu_activate_restore(self, menu, items):
        """Menu: Clicked restore"""
        for item in items:
            if not item.is_gone():
                self.foldercolor.set_restore(unquote(item.get_uri()[7:]))
