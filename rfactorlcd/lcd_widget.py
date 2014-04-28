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
import logging

import rfactorlcd


class LCDWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.rf_state = rfactorlcd.rFactorState()
        self.lcd_style = rfactorlcd.Style.black_on_white()

        self.workspace = rfactorlcd.Workspace()
        self.workspace.set_lcd_style(self.lcd_style)

        self.dashlet_selection = rfactorlcd.DashletSelection(self.lcd_style, self.workspace)

        self.dashlet_insert_pos = None

        #self.set_events(gtk.MOTION_NOTIFY)

        self.set_events(gtk.gdk.EXPOSURE_MASK
                        | gtk.gdk.LEAVE_NOTIFY_MASK
                        | gtk.gdk.KEY_PRESS_MASK
                        | gtk.gdk.KEY_RELEASE_MASK
                        | gtk.gdk.BUTTON_PRESS_MASK
                        | gtk.gdk.BUTTON_RELEASE_MASK
                        | gtk.gdk.POINTER_MOTION_MASK
                        | gtk.gdk.POINTER_MOTION_HINT_MASK)

        self.set_can_focus(True)
        self.connect("motion_notify_event", self.on_motion_notify)
        self.connect("button_press_event", self.on_button_press)
        self.connect("button_release_event", self.on_button_release)
        self.connect("key_press_event", self.on_key_press)

        self.menu = gtk.Menu()
        for k, dashlet_class in sorted(rfactorlcd.dashlets.items(), key=lambda k: k[0]):
            menu_item = gtk.MenuItem("Add %s" % k)
            self.menu.append(menu_item)
            menu_item.connect("activate",
                              lambda arg, dashlet_class=dashlet_class:
                              self.on_menu_item(arg, dashlet_class))
            menu_item.show()

    def on_menu_item(self, menu_item, dashlet_class):
        print "on_menu_item", menu_item, dashlet_class
        dashlet = dashlet_class(self, self.lcd_style)
        dashlet.set_geometry(self.dashlet_insert_pos[0],
                             self.dashlet_insert_pos[1],
                             256, 256)
        self.workspace.dashlets.append(dashlet)
        self.queue_draw()

    def on_key_press(self, widget, event):
        if event.keyval == gtk.keysyms.Delete:
            for dashlet in self.dashlet_selection.dashlets:
                self.workspace.remove_dashlet(dashlet)
            self.dashlet_selection.clear()
            self.queue_draw()

        elif event.keyval == gtk.keysyms.Page_Up:
            # FIXME: this is not the proper way to raise a group
            for dashlet in self.dashlet_selection.dashlets:
                self.workspace.raise_dashlet(dashlet)
            self.queue_draw()

        elif event.keyval == gtk.keysyms.Page_Down:
            # FIXME: this is not the proper way to lower a group
            for dashlet in self.dashlet_selection.dashlets:
                self.workspace.lower_dashlet(dashlet)
            self.queue_draw()

    def on_button_press(self, widget, event):
        logging.info("LCDWidget button press %s %s %s", event.x, event.y, event.button)
        if event.button == 1:
            self.dashlet_selection.on_button_press(event)
            self.queue_draw()

        elif event.button == 3:
            self.dashlet_insert_pos = (event.x, event.y)
            self.menu.popup(None, None, None, event.button, event.time)

    def on_button_release(self, widget, event):
        logging.info("LCDWidget button release %s %s %s", event.x, event.y, event.button)
        if event.button == 1:
            self.dashlet_selection.on_button_release(event)
            self.queue_draw()

    def on_motion_notify(self, widget, event):
        self.dashlet_selection.on_move(event)
        self.queue_draw()

    def set_lcd_style(self, style):
        self.lcd_style = style
        self.workspace.set_lcd_style(style)

    def on_expose_event(self, widget, event):
        if self.window:
            cr = self.window.cairo_create()

            # Restrict Cairo to the exposed area; avoid extra work
            if event:
                cr.rectangle(event.area.x, event.area.y,
                             event.area.width, event.area.height)
                cr.clip()

            cr.set_antialias(cairo.ANTIALIAS_NONE)
            cr.set_line_width(8.0)
            cr.select_font_face(self.lcd_style.font,
                                self.lcd_style.font_slant,
                                self.lcd_style.font_weight)

            if True:
                cr.set_source_rgb(*self.lcd_style.background_color)
            else:
                cr.set_source_rgb(random.random(),
                                  random.random(),
                                  random.random())
            cr.paint()

            self.workspace.draw(cr)

            self.dashlet_selection.render(cr)

    def update_state(self, tag, payload):
        self.rf_state.dispatch_message(tag, payload)
        self.workspace.update_state(self, self.rf_state)

# EOF #
