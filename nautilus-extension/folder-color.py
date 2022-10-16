# Folder Color 0.1.4 - https://github.com/costales/folder-color
# Copyright (C) 2012-2022 Marcos Alvarez Costales - https://costales.github.io/
#
# Folder Color is free software; you can redistribute it and/or modify
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

import os, gettext
from gi.repository import Nautilus, Gtk, GObject, Gio, GLib

# Python 2 or 3
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

# i18n
gettext.textdomain('folder-color-common')
_ = gettext.gettext


class FolderColor:
    """Folder Color Class"""
    def __init__(self):
        # Folder colors
        self.COLORS = [
            'black',
            'blue',
            'brown',
            'cyan',
            'green',
            'grey',
            'magenta',
            'orange',
            'pink',
            'purple',
            'red',
            'violet',
            'yellow'
        ]
        self.I18N_COLORS = {
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
        # Emblems
        self.EMBLEMS = [
            'emblem-important',
            'emblem-urgent',
            'emblem-favorite',
            'emblem-default',
            'emblem-new'
        ]
        self.I18N_EMBLEMS = {
            'emblem-important': _("Important"),
            'emblem-urgent'   : _("In Progress"),
            'emblem-favorite' : _("Favorite"),
            'emblem-default'  : _("Finished"),
            'emblem-new'      : _("New")
        }
        # Custom folder color
        self.PATH_CUSTOM_COLOR = os.path.join(os.getenv('HOME'), '.local', 'share', 'folder-color', 'icons')
        self.GRADIENT_RANGE = 15
        self.VALUE_LIGHT  = 'value_light'
        self.VALUE_MIDDLE = 'value_middle'
        self.VALUE_DARK   = 'value_dark'
    
    def get_icon(self, icon_name):
        """Get icon name and filename (used for check if exists an icon)"""
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.lookup_icon(icon_name, 48, 0)
        if icon != None:
            return {'name'    : os.path.splitext(os.path.basename(icon.get_filename()))[0],
                    'filename': icon.get_filename()}
        else:
            return {'name': '',
                    'filename': ''}
    
    def set_color(self, item_path, color, is_uri=False):
        """Set color to a file/directory"""
         # Restore
        self.restore_color(item_path)
        # Set
        item = Gio.File.new_for_path(item_path)
        if not is_uri:
            info = item.query_info('metadata::custom-icon-name', 0, None)
            info.set_attribute_string("metadata::custom-icon-name", color)
        else:
            info = item.query_info('metadata::custom-icon', 0, None)
            info.set_attribute_string('metadata::custom-icon', 'file://'+color)
        item.set_attributes_from_info(info, 0, None)
        # Refresh
        self._refresh(item_path)
    
    def set_emblem(self, item_path, emblem_name=''):
        """Set emblem"""
        # Restore
        self.restore_emblem(item_path)
        # Set
        if emblem_name:
            emblem = []
            emblem.append(emblem_name)
            emblems = list(emblem)
            emblems.append(None) # Needs
            item = Gio.File.new_for_path(item_path)
            info = item.query_info('metadata::emblems', 0, None)
            info.set_attribute_stringv('metadata::emblems', emblems)
            item.set_attributes_from_info(info, 0, None)
        # Refresh
        self._refresh(item_path)
    
    def restore_emblem(self, item_path):
        """Restore emblem to default"""
        item = Gio.File.new_for_path(item_path)
        info = item.query_info('metadata::emblems', 0, None)
        info.set_attribute('metadata::emblems', Gio.FileAttributeType.INVALID, 0)
        item.set_attributes_from_info(info, 0, None)
        self._refresh(item_path)
    
    def restore_color(self, item_path):
        """Restore folder color to default"""
        item = Gio.File.new_for_path(item_path)
        info = item.query_info('metadata::custom-icon-name', 0, None)
        info.set_attribute('metadata::custom-icon',      Gio.FileAttributeType.INVALID, 0)
        info.set_attribute('metadata::custom-icon-name', Gio.FileAttributeType.INVALID, 0)
        item.set_attributes_from_info(info, 0, None)
        self._refresh(item_path)
    
    def _refresh(self, item_path):
        """Reload the current file/directory icon"""
        os.utime(item_path, None)



class FolderColorMenu(GObject.GObject, Nautilus.MenuProvider):
    """File Browser Menu"""
    def __init__(self):
        GObject.Object.__init__(self)
        self.foldercolor = FolderColor()
        self.theme_dirname = ''
        self.all_are_directories = True
        self.all_are_files = True
    
    def get_file_items(self, window, items):
        """Nautilus invoke this function in its startup > Create menu entry"""
        # Checks
        if not self._check_generate_menu(items):
            return
        
        # Set current theme directory
        self.theme_dirname = os.path.dirname(self._legacy_filename('blue')['filename'])
        
        # Menu
        return self._generate_menu(items)
    
    def _check_generate_menu(self, items):
        """Menu: Show it?"""
        # No items selected
        if not len(items):
            return False
        
        self.all_are_directories = True
        self.all_are_files = True
        for item in items:
            # GNOME can only handle files
            if item.get_uri_scheme() != 'file':
                return False
            
            if item.is_directory():
                self.all_are_files = False
            else:
                self.all_are_directories = False
        
        # All OK? > Generate menu
        return True
    
    def _generate_menu(self, items):
        """Menu for [directories|files]: [Color,Custom,Restore,Emblems|Emblems,Restore]"""
        # Directories
        if self.all_are_directories:
            # Title menu
            if len(items) > 1:
                top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Folders' Color"), icon='folder_color_picker')
            else:
                top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Folder's Color"),  icon='folder_color_picker')
            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)
            
            # Colors
            for color in self.foldercolor.COLORS:
                icon = self._legacy_filename(color)
                if not icon['name']:
                    continue
                if not self._check_same_theme(icon['filename']):
                    continue
                
                name = ''.join(['ChangeFolderColorMenu::Colors"', color, '"'])
                item = Nautilus.MenuItem(name=name, label=self.foldercolor.I18N_COLORS[color], icon=icon['name'])
                item.connect('activate', self._menu_activate_color, icon['name'], items)
                submenu.append_item(item)
            
            # Custom color
            custom_icon = self._legacy_filename('custom')
            if custom_icon['name'] and self._check_same_theme(custom_icon['filename']) and custom_icon['filename'].lower().endswith('.svg'): # exists + same theme + SVG
                name = ''.join(['ChangeFolderColorMenu::Colors"', 'custom', '"'])
                item = Nautilus.MenuItem(name=name, label=_("Custom"), icon='gtk-edit')
                item.connect('activate', self._menu_activate_custom_color, custom_icon['name'], items)
                submenu.append_item(item)
            
            # Separator if there are emblems
            for emblem in self.foldercolor.EMBLEMS:
                if self.foldercolor.get_icon(emblem)['name']:
                    item_sep = Nautilus.MenuItem(name='ChangeFolderColorMenu::Sep1', label=_("Emblem:"), sensitive=False)
                    submenu.append_item(item_sep)
                    break
            
            # Emblems
            for emblem in self.foldercolor.EMBLEMS:
                if self.foldercolor.get_icon(emblem)['name']:
                    name = ''.join(['ChangeFolderColorMenu::Colors"', emblem, '"'])
                    item = Nautilus.MenuItem(name=name, label=self.foldercolor.I18N_EMBLEMS[emblem], icon=emblem)
                    item.connect('activate', self._menu_activate_emblem, emblem, items)
                    submenu.append_item(item)
        
            # Restore
            if self._check_generate_restore(items):
                item_sep = Nautilus.MenuItem(name='ChangeFolderEmblemMenu::Sep', label=_("Restore:"), sensitive=False)
                submenu.append_item(item_sep)
                
                item_restore = Nautilus.MenuItem(name='ChangeFolderColorMenu::Restore', label=_("Default"), icon='undo')
                item_restore.connect('activate', self._menu_activate_restore_all, items)
                submenu.append_item(item_restore)
            
        # Files
        else:
            # Title menu
            if self.all_are_files:
                if len(items) > 1:
                    top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Files' Emblem"), icon='folder_color_picker')
                else:
                    top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("File's Emblem"),  icon='folder_color_picker')
            else:
                top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Emblem"),  icon='folder_color_picker')
            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)
            
            # Emblems
            exist_emblems = False
            for emblem in self.foldercolor.EMBLEMS:
                if self.foldercolor.get_icon(emblem)['name']:
                    exist_emblems = True
                    name = ''.join(['ChangeFolderColorMenu::Colors"', emblem, '"'])
                    item = Nautilus.MenuItem(name=name, label=self.foldercolor.I18N_EMBLEMS[emblem], icon=emblem)
                    item.connect('activate', self._menu_activate_emblem, emblem, items)
                    submenu.append_item(item)
        
            # Restore
            if exist_emblems and self._check_generate_restore(items):
                item_sep = Nautilus.MenuItem(name='ChangeFolderEmblemMenu::Sep', label=_("Restore:"), sensitive=False)
                submenu.append_item(item_sep)
                
                item_restore = Nautilus.MenuItem(name='ChangeFolderColorMenu::Restore', label=_("Default"), icon='undo')
                item_restore.connect('activate', self._menu_activate_restore_emblem, items)
                submenu.append_item(item_restore)
            
        return top_menuitem,
    
    def _check_same_theme(self, filename):
        """Don't mix icon themes"""
        if os.path.dirname(filename) == self.theme_dirname:
            return True
        else:
            return False
    
    def _check_generate_restore(self, items):
        """Menu: Show restore?"""
        # For each dir, search custom icon or emblem
        for item in items:
            if item.is_gone():
                continue
            
            # Get metadata file/folder
            item_path = unquote(item.get_uri()[7:])
            item = Gio.File.new_for_path(item_path)
            info = item.query_info('metadata', 0, None)
            # If any metadata > restore menu
            if info.get_attribute_as_string('metadata::custom-icon-name'):
                return True
            if info.get_attribute_as_string('metadata::custom-icon'):
                return True
            if info.get_attribute_as_string('metadata::emblems'):
                return True
        
        return False
    
    def _menu_activate_color(self, menu, icon, items):
        """Menu: Clicked color"""
        for each_item in items:
            if each_item.is_gone():
                continue
            
            item_path = unquote(each_item.get_uri()[7:])
            self.foldercolor.set_color(item_path, self._get_skel_folder(item_path, icon)['name'])
    
    def _menu_activate_restore_all(self, menu, items):
        """Menu: Clicked restore"""
        for each_item in items:
            if each_item.is_gone():
                continue
            
            item_path = unquote(each_item.get_uri()[7:])
            self.foldercolor.restore_color(item_path)
            self.foldercolor.restore_emblem(item_path)
    
    def _menu_activate_restore_emblem(self, menu, items):
        """Menu: Clicked restore"""
        for each_item in items:
            if each_item.is_gone():
                continue
            
            item_path = unquote(each_item.get_uri()[7:])
            self.foldercolor.restore_emblem(item_path)
    
    def _menu_activate_emblem(self, menu, emblem, items):
        """Menu: Clicked emblem"""
        for each_item in items:
            if each_item.is_gone():
                continue
            
            item_path = unquote(each_item.get_uri()[7:])
            self.foldercolor.set_emblem(item_path, emblem)
    
    def _menu_activate_custom_color(self, menu, icon, items):
        """Menu: Clicked custom"""
        custom_color = self.custom_color_dialog()
        if custom_color == None: # Cancel
            return
        
        for each_item in items:
            if each_item.is_gone():
                continue
            
            item_path = unquote(each_item.get_uri()[7:])
            custom_icon = self._get_skel_folder(item_path, icon)
            
            src_file = custom_icon['filename']
            dst_file = ''.join([self.foldercolor.PATH_CUSTOM_COLOR, '/', custom_icon['name'], '-', custom_color['middle'], '.svg'])
            self._cp_file(src_file, dst_file, custom_color)
            
            self.foldercolor.set_color(item_path, dst_file, True)
    
    def custom_color_dialog(self):
        """Pick color dialog"""
        dialog = Gtk.ColorChooserDialog()
        dialog.set_use_alpha(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # Color
            color = dialog.get_rgba()
            dialog.destroy()
            red   = (color.red   * 255)
            green = (color.green * 255)
            blue  = (color.blue  * 255)
            # Light
            hex_light = "%02x%02x%02x" % (red, green, blue)
            # Middle
            red = red - self.foldercolor.GRADIENT_RANGE
            if red < 0:
                red = 0
            green = green - self.foldercolor.GRADIENT_RANGE
            if green < 0:
                green = 0
            blue = blue - self.foldercolor.GRADIENT_RANGE
            if blue < 0:
                blue = 0
            hex_middle = "%02x%02x%02x" % (red, green, blue)
            # Dark
            red = red - self.foldercolor.GRADIENT_RANGE
            if red < 0:
                red = 0
            green = green - self.foldercolor.GRADIENT_RANGE
            if green < 0:
                green = 0
            blue  = blue  - self.foldercolor.GRADIENT_RANGE
            if blue < 0:
                blue = 0
            hex_dark = "%02x%02x%02x" % (red, green, blue)
            return {'light' : hex_light,
                    'middle': hex_middle,
                    'dark'  : hex_dark}
        
        dialog.destroy()
        return None
    
    def _cp_file(self, src_file, dst_file, pick_color):
        """Parsing custom template to a custom icon"""
        if not os.path.exists(self.foldercolor.PATH_CUSTOM_COLOR):
            try:
                os.makedirs(self.foldercolor.PATH_CUSTOM_COLOR)
            except OSError as exception:
                pass
            except:
                pass
        
        f_input  = open(src_file, 'r') # This has to exists always
        f_output = open(dst_file, 'w')
        f_generate  = f_input.read().replace(self.foldercolor.VALUE_LIGHT, pick_color['light']).replace(self.foldercolor.VALUE_MIDDLE, pick_color['middle']).replace(self.foldercolor.VALUE_DARK, pick_color['dark'])
        f_output.write(f_generate)
    
    def _legacy_filename(self, color):
        """Search for available folder colors (scope for legacy too)"""
        # Theme priority
        icon = self.foldercolor.get_icon('folder_color_'+color) # folder_color_blue (legacy)
        if icon['name'] and  not '/hicolor/' in icon['filename']:
            return icon
        icon = self.foldercolor.get_icon('folder-'+color)       # folder-blue
        if icon['name'] and not '/hicolor/' in icon['filename']:
            return icon
        icon = self.foldercolor.get_icon('folder_'+color)       # folder_custom (legacy)
        if icon['name'] and  not '/hicolor/' in icon['filename']:
            return icon
        # hicolor
        icon = self.foldercolor.get_icon('folder_color_'+color) # folder_color_blue (legacy)
        if icon['name']:
            return icon
        icon = self.foldercolor.get_icon('folder-'+color)       # folder-blue
        if icon['name']:
            return icon
        icon = self.foldercolor.get_icon('folder_'+color)       # folder_custom (legacy)
        if icon['name']:
            return icon
        # Not found
        return icon
    
    def _get_skel_folder(self, folder, color):
        """Default directories"""
        skel_color = ''
        # Search folder_color_blue_<desktop>
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_DESKTOP):
            skel_color = color + '_desktop'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOCUMENTS):
            skel_color = color + '_documents'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD):
            skel_color = color + '_downloads'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_MUSIC):
            skel_color = color + '_music'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES):
            skel_color = color + '_pictures'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_PUBLIC_SHARE):
            skel_color = color + '_public'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_TEMPLATES):
            skel_color = color + '_templates'
        if folder == GLib.get_user_special_dir(GLib.USER_DIRECTORY_VIDEOS):
            skel_color = color + '_videos'
        skel_folder = self.foldercolor.get_icon(skel_color)
        if skel_folder['name'] and self._check_same_theme(skel_folder['filename']):
            return skel_folder
        
        # Search folder-blue-<desktop>
        skel_color = skel_color.replace('_', '-')
        skel_folder = self.foldercolor.get_icon(skel_color)
        if skel_folder['name'] and self._check_same_theme(skel_folder['filename']):
            return skel_folder
        
        return self.foldercolor.get_icon(color)
