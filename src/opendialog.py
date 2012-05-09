#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dtk.ui.titlebar import Titlebar
from dtk.ui.scrolled_window import ScrolledWindow
from dtk.ui.button import Button
from dtk.ui.draw import draw_pixbuf
from dtk.ui.draw import draw_font
# from dtk.ui.utils import propagate_expose
from utils import app_theme
from utils import allocation
import os
import gtk
import gobject

class OpenDialog(gobject.GObject):
    __gsignals__ = {
        "get-path-name":(gobject.SIGNAL_RUN_LAST,
                         gobject.TYPE_NONE,(gobject.TYPE_STRING,))
        }    
    def __init__ (self, titlebar_name = "打开"):        
        gobject.GObject.__init__(self)
        
        self.button_x_offset = 0
        self.button_y_offset = 0
        self.save_path = self.get_home_path()
        self.init_bool = True
        self.file_name = ""
        self.play_file_geshi = [".rmvb", ".avi", ".mp3", ".mp4", "wav"]
        
        # show file or path of image.
        self.vide_pixbuf = app_theme.get_pixbuf("Videos.ico")
        self.music_pixbuf = app_theme.get_pixbuf("Music.ico")
        self.folder_pixbuf = app_theme.get_pixbuf("Folder.ico")
        
        # self.open_window = Application("OpenDialog", True)
        self.open_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.open_window.connect("destroy", lambda w: self.open_window.destroy())
        self.open_window.set_decorated(False)
        self.title_bar = Titlebar(["close"])
        self.title_bar.close_button.connect("clicked", lambda w:self.open_window.destroy())
        self.main_vbox = gtk.VBox()
        self.main_vbox.pack_start(self.title_bar, False, False)
        self.open_window.add(self.main_vbox)
        
        # self.open_window.window.connect("destroy", self.open_window.destroy)
        self.open_window.set_size_request(500, 400) 
        
        # self.open_window.add_titlebar(["close"],
        #                               app_theme.get_pixbuf("OrdinaryMode.png"),
        #                               titlebar_name, " ", add_separator = True)        
        
        self.scrolled_window_frame = gtk.Alignment()
        self.scrolled_window_frame.set(1, 1, 1, 1)
        self.scrolled_window_frame.set_padding(1, 2, 2, 2)
        self.scrolled_window = ScrolledWindow()
        self.scrolled_window_frame.add(self.scrolled_window)
        self.fixed = gtk.Fixed()

        self.scrolled_window.add_child(self.fixed)    
        
        # main_box add fixed.
        self.main_vbox.pack_start(self.scrolled_window_frame, True, True)
        # bottom button.
        self.hbox_frame = gtk.Alignment()
        self.hbox_frame.set(1, 0, 0, 0)
        self.hbox_frame.set_padding(0, 2, 0, 20)
        self.hbox = gtk.HBox()        
        self.hbox_frame.add(self.hbox)
        self.ok_btn = Button(titlebar_name)
        self.cancel_btn = Button("取消")
        self.hbox.pack_start(self.ok_btn, False, False)
        self.hbox.pack_start(self.cancel_btn, False, False)
        # main_box add hbox_frame
        
        self.main_vbox.pack_start(self.hbox_frame, False, False)
        
        self.open_window.show_all()        
        self.open_window.hide_all()
                
    def fixed_add_button_child(self, text, x, y):
        temp_path = self.save_path + "/" + text
        isfile_bool = False
        
        if os.path.isfile(temp_path):
            # if os.path.splitext(text)
            file1, file2 = os.path.splitext(text)
            if file2.lower() in self.play_file_geshi:
                isfile_bool = True
            
        
        if os.path.isdir(temp_path) or isfile_bool:            
            button = gtk.Button(str(text))
            button.set_size_request(400, -1)
            button.connect("clicked", self.open_file_or_dir, str(text))
            button.connect("expose-event", self.draw_button_bacbground, str(text))                            
            self.fixed.put(button, int(x), int(y))
            self.button_y_offset += 23
            
    def draw_button_bacbground(self, widget, event, text):    
        cr, x, y, w, h = allocation(widget)
        temp_path = self.save_path + "/" + text
        
        music_pixbuf = self.music_pixbuf.get_pixbuf().scale_simple(18, 18, gtk.gdk.INTERP_BILINEAR)
        vide_pixbuf = self.vide_pixbuf.get_pixbuf().scale_simple(18, 18, gtk.gdk.INTERP_BILINEAR)
        folder_pixbuf = self.folder_pixbuf.get_pixbuf().scale_simple(18, 18, gtk.gdk.INTERP_BILINEAR)
        
        
        pixbuf_padding = 2
        if os.path.isdir(temp_path):
            draw_pixbuf(cr, folder_pixbuf, x, y + pixbuf_padding)       
        if os.path.isfile(temp_path):        
            file1, file2 = os.path.splitext(text)
            if file2.lower() in [".mp3","wav"]:            
                draw_pixbuf(cr, music_pixbuf, x, y + pixbuf_padding)    
            else:    
                draw_pixbuf(cr, vide_pixbuf, x, y + pixbuf_padding)
        draw_font(cr, text, 8, "#000000", 
                  x +18 , y , w, h)           
        
        if widget.state == gtk.STATE_PRELIGHT:
            cr.set_source_rgba(1, 0, 0, 0.1)
            cr.rectangle(x, y ,w , h)
            cr.fill()
            
        return True
    
    def open_file_or_dir(self, widget, text):          
        temp_path = self.save_path + "/" + text
        
        if os.path.isfile(temp_path):
            self.filename = temp_path
            self.open_window.destroy()
            self.emit("get-path-name", self.filename)
            
        if os.path.isdir(temp_path):
            self.save_path += "/" + text # save path.
            # clear all button.
            for i in self.get_fixed_childs():
                self.fixed.remove(i)                
                
            self.button_y_offset = 0            
            self.show_file_and_dir(temp_path)
        
    def get_fixed_childs(self): 
        return self.fixed.get_children() #return list.   
    
    def show_dialog(self):
        if self.init_bool:
            self.show_file_and_dir(self.save_path)
            self.init_bool = False
            
        self.open_window.show_all()
        
    def show_file_and_dir(self, path):
        if os.path.isdir(path): # is dir.
            all_dir_and_file = os.listdir(path)
            for file_name in all_dir_and_file:
                self.fixed_add_button_child(str(file_name), self.button_x_offset, self.button_y_offset)                
        self.open_window.show_all()
        
    def get_home_path(self):
        return os.path.expanduser("~")
        
if __name__ == "__main__":    
    open_dialog = OpenDialog()
    open_dialog.show_dialog()
    gtk.main()
