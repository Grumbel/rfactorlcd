#!/usr/bin/env python

# rFactor Remote LCD
# Copyright (C) 2014 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import cairo
import gtk
import random

import rfactorlcd.canvas as canvas


class TestWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.canvas = canvas.Group()
        self.set_size_request(640, 480)

        fsize=32.0

        x, y = (320, 100)
        self.canvas.add_text(x, y, "Center", fill_color=(0,0,0), 
                             anchor=canvas.Anchor.S, baseline=canvas.Baseline.MIDDLE, font_size=fsize)
        self.canvas.add_rectangle(x-4, y-4, 9, 9, fill_color=(1, 0, 0), stroke_color=(0, 0, 0))

        x, y = (320, 200)
        self.canvas.add_text(x, y, "North", fill_color=(0,0,0), anchor=canvas.Anchor.N, font_size=fsize)
        self.canvas.add_text(x, y, "South", fill_color=(0,0,0), anchor=canvas.Anchor.S, font_size=fsize)

        self.canvas.add_text(x, y, "West", fill_color=(0,0,0), anchor=canvas.Anchor.W, font_size=fsize)
        self.canvas.add_text(x, y, "East", fill_color=(0,0,0), anchor=canvas.Anchor.E, font_size=fsize)
        self.canvas.add_rectangle(x-4, y-4, 9, 9, fill_color=(1, 0, 0), stroke_color=(0, 0, 0))

        x, y = (320, 300)
        self.canvas.add_text(x, y, "norwes", fill_color=(0,0,0), anchor=canvas.Anchor.NW, font_size=fsize)
        self.canvas.add_text(x, y, "NorthEast", fill_color=(0,0,0), anchor=canvas.Anchor.NE, font_size=fsize)

        self.canvas.add_text(x, y, "SouthWest", fill_color=(0,0,0), anchor=canvas.Anchor.SW, font_size=fsize)
        self.canvas.add_text(x, y, "SouthEast", fill_color=(0,0,0), anchor=canvas.Anchor.SE, font_size=fsize)
        self.canvas.add_rectangle(x-4, y-4, 9, 9, fill_color=(1, 0, 0), stroke_color=(0, 0, 0))


        x, y = (120, 430)
        self.canvas.add_rectangle(x, y, 400, 1, fill_color=(0,0,0))
        self.canvas.add_text(x + 0, y, "Alpyt", fill_color=(0,0,0), 
                             anchor=canvas.Anchor.SW, baseline=canvas.Baseline.ALPHABETIC, font_size=fsize)
        self.canvas.add_text(x + 80, y, "Topyt", fill_color=(0,0,0), 
                             anchor=canvas.Anchor.SW, baseline=canvas.Baseline.TOP, font_size=fsize)
        self.canvas.add_text(x + 160, y, "Middleyt", fill_color=(0,0,0), 
                             anchor=canvas.Anchor.SW, baseline=canvas.Baseline.MIDDLE, font_size=fsize)
        self.canvas.add_text(x + 240, y, "Bottyt", fill_color=(0,0,0), 
                             anchor=canvas.Anchor.SW, baseline=canvas.Baseline.BOTTOM, font_size=fsize)

    def on_expose_event(self, widget, event):
        print "expose"
        if self.window:
            cr = self.window.cairo_create()
            self.canvas.render(cr)

if __name__ == '__main__':

    gtk.gdk.threads_init()
    window = gtk.Window()

    widget = TestWidget()
    widget.show()

    window.add(widget)
    window.present()

    gtk.main()


# EOF #
