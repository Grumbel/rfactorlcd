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

import rfactorlcd


class DragMode:
    Move = 0
    ResizeLeft = 1 << 0
    ResizeRight = 1 << 1
    ResizeTop = 1 << 2
    ResizeBottom = 1 << 3


class LCDWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.rf_state = rfactorlcd.rFactorState()
        self.lcd_style = rfactorlcd.Style.white_on_black()

        self.workspace = rfactorlcd.Workspace()
        self.workspace.set_lcd_style(self.lcd_style)
        self.workspace.load_default()

        self.active_dashlet = None
        self.drag_dashlet = None
        self.drag_start = None

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
        for item in ["RPMDashlet", "TempDashlet", "SpeedDashlet",
                     "SectorDashlet", "LaptimeDashlet", "PositionDashlet",
                     "RPM2Dashlet", "ShiftlightsDashlet", "CarDashlet",
                     "SpeedometerDashlet"]:
            menu_item = gtk.MenuItem("Add %s" % item)
            self.menu.append(menu_item)
            menu_item.connect("activate", lambda arg, item=item: self.on_menu_item(arg, item))
            menu_item.show()

    def on_menu_item(self, menu_item, dashlet_class):
        dashlet_class = rfactorlcd.__getattribute__(dashlet_class)
        print "on_menu_item", menu_item, dashlet_class
        dashlet = dashlet_class(self, self.lcd_style)
        dashlet.set_geometry(self.dashlet_insert_pos[0],
                             self.dashlet_insert_pos[1],
                             256, 256)
        self.workspace.dashlets.append(dashlet)
        self.queue_draw()

    def on_key_press(self, widget, event):
        if event.keyval == gtk.keysyms.Delete:
            self.workspace.remove_dashlet(self.active_dashlet)
            self.active_dashlet = None
            self.queue_draw()

        elif event.keyval == gtk.keysyms.Page_Up:
            self.workspace.raise_dashlet(self.active_dashlet)
            self.queue_draw()

        elif event.keyval == gtk.keysyms.Page_Down:
            self.workspace.lower_dashlet(self.active_dashlet)
            self.queue_draw()

    def on_button_press(self, widget, event):
        # print "press", event.x, event.y, event.button
        if event.button == 1:
            self.drag_dashlet = self.active_dashlet
            if self.drag_dashlet:
                self.drag_dashlet_origin = (self.drag_dashlet.x, self.drag_dashlet.y,
                                            self.drag_dashlet.w, self.drag_dashlet.h)

                self.drag_mode = DragMode.Move
                border = 20
                if self.drag_dashlet.x + border > event.x:
                    self.drag_mode |= DragMode.ResizeLeft
                elif self.drag_dashlet.x2 - border < event.x:
                    self.drag_mode |= DragMode.ResizeRight

                if self.drag_dashlet.y + border > event.y:
                    self.drag_mode |= DragMode.ResizeTop
                elif self.drag_dashlet.y2 - border < event.y:
                    self.drag_mode |= DragMode.ResizeBottom

                self.drag_start = (event.x, event.y)
        elif event.button == 3:
            self.dashlet_insert_pos = (event.x, event.y)
            self.menu.popup(None, None, None, event.button, event.time)

    def on_button_release(self, widget, event):
        print "release", event.x, event.y, event.button
        if event.button == 1:
            self.drag_dashlet = None

    def on_motion_notify(self, widget, event):
        if self.drag_dashlet is not None:
            x = event.x - self.drag_start[0]
            y = event.y - self.drag_start[1]

            if self.drag_mode == DragMode.Move:
                self.drag_dashlet.set_geometry(self.drag_dashlet_origin[0] + x,
                                               self.drag_dashlet_origin[1] + y)

            if self.drag_mode & DragMode.ResizeLeft:
                self.drag_dashlet.set_geometry(x=self.drag_dashlet_origin[0] + x,
                                               w=self.drag_dashlet_origin[2] - x)

            if self.drag_mode & DragMode.ResizeRight:
                self.drag_dashlet.set_geometry(w=self.drag_dashlet_origin[2] + x)

            if self.drag_mode & DragMode.ResizeTop:
                self.drag_dashlet.set_geometry(y=self.drag_dashlet_origin[1] + y,
                                               h=self.drag_dashlet_origin[3] - y)

            if self.drag_mode & DragMode.ResizeBottom:
                self.drag_dashlet.set_geometry(h=self.drag_dashlet_origin[3] + y)

            self.queue_draw()
        else:
            active_dashlet = self.workspace.find_dashlet_at(event.x, event.y)
            if active_dashlet != self.active_dashlet:
                self.active_dashlet = active_dashlet
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

            if self.active_dashlet:
                border = 20
                cr.set_line_width(4.0)
                cr.set_source_rgb(*self.lcd_style.shadow_color)
                cr.rectangle(self.active_dashlet.x, self.active_dashlet.y,
                             border, self.active_dashlet.h)
                cr.rectangle(self.active_dashlet.x + self.active_dashlet.w - border, self.active_dashlet.y,
                             border, self.active_dashlet.h)

                cr.rectangle(self.active_dashlet.x, self.active_dashlet.y,
                             self.active_dashlet.w, border)
                cr.rectangle(self.active_dashlet.x, self.active_dashlet.y + self.active_dashlet.h - border,
                             self.active_dashlet.w, border)
                cr.stroke()

                cr.set_line_width(6.0)
                cr.set_source_rgb(*self.lcd_style.highlight_color)
                cr.rectangle(self.active_dashlet.x, self.active_dashlet.y,
                             self.active_dashlet.w, self.active_dashlet.h)
                cr.stroke()

    def update_state(self, state):
        self.rf_state = state
        self.workspace.update_state(self, state)


# EOF #
