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

from dtk.ui.frame import *
from dtk.ui.panel import *
from dtk.ui.utils import *

from utils import *
from constant import *

from progressbar import *
from show_time import *
from play_control_panel import *
from volume_button import *


class ToolBar2(object):            
    def __init__(self, background_pixbuf = app_theme.get_pixbuf("bg.png")):
        self.background_pixbuf = background_pixbuf
        self.panel = Panel(0, 42)
        self.vbox = gtk.VBox()
        self.progressbar = ProgressBar()        
        media_player["app"].window.connect("configure-event",
                                           self.modify_panel)

        # panel signal.
        self.panel.connect("expose-event", self.panel_expose)
        media_player["screen"].screen.connect("motion-notify-event",
                                       self.show_panel)
        self.hbox = gtk.HBox()
        # hbox add child widget.
        self.show_time = ShowTime()
        self.play_control_panel = PlayControlPanel()
        volume_hframe = HorizontalFrame()
        self.volume_button = VolumeButton()
        volume_hframe.add(self.volume_button)
        
        self.hbox.pack_start(self.show_time.time_box)
                
        self.hbox.pack_start(self.play_control_panel.hbox_hframe)
        self.hbox.pack_start(volume_hframe, True, True)
   
        
        self.vbox.pack_start(self.progressbar.hbox, False, False)
        self.vbox.pack_start(self.hbox, True, True)
        
        self.panel.add(self.vbox)        
        
    def show_panel(self, widget, event):
        if media_player["mp"].state == 1:
            if widget.allocation.height - 42 <= event.y <= widget.allocation.height:                
                if media_player["fullscreen_state"] or not media_player["common_state"]:
                    self.panel.resize(widget.allocation.width , 
                                      PANEL_HEIGHT)
                    x,y = media_player["app"].window.window.get_root_origin()
                    if not media_player["common_state"]:
                        self.panel.move(x+2, y + widget.allocation.height - 43)
                    else:    
                        self.panel.move(x+2, y + widget.allocation.height)    
                    self.panel.show_all()
            else:
                self.panel.hide_all()
                self.panel.resize(widget.allocation.width , 
                                  PANEL_HEIGHT)
        return False
        
    def modify_panel(self, widget, event):    
        self.hide_toolbar2()
        
    def panel_expose(self, widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        # Draw background.
        background_pixbuf = self.background_pixbuf.get_pixbuf()
        image = background_pixbuf.scale_simple(w, h, gtk.gdk.INTERP_BILINEAR)
        cr.set_source_pixbuf(image, x, y)
        cr.paint_with_alpha(1)
        widget.propagate_expose(widget.get_child(), event)
        return True
                    
    def show_toolbar2(self):    
        self.panel.show_all()
        
    def hide_toolbar2(self):    
        self.panel.hide_all()
                
if __name__ == "__main__":    
    tb = ToolBar2()
    tb.show_all()
    gtk.main()