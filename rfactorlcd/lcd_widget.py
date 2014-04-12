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


class LCDWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.rf_state = rfactorlcd.rFactorState()
        self.lcd_style = rfactorlcd.Style.white_on_black()

        rpm_dashlet = rfactorlcd.RPMDashlet(self, self.lcd_style)
        rpm_dashlet.set_geometry(100, 100, 300, 300)

        temp_dashlet = rfactorlcd.TempDashlet(self, self.lcd_style)
        temp_dashlet.set_geometry(600, 300, 450, 250)

        speed_dashlet = rfactorlcd.SpeedDashlet(self, self.lcd_style)
        speed_dashlet.set_geometry(500, 150, 400, 200)

        sector_dashlet = rfactorlcd.SectorDashlet(self, self.lcd_style)
        sector_dashlet.set_geometry(800, 550, 300, 300)

        laptime_dashlet = rfactorlcd.LaptimeDashlet(self, self.lcd_style)
        laptime_dashlet.set_geometry(50, 600, 800, 100)

        position_dashlet = rfactorlcd.PositionDashlet(self, self.lcd_style)
        position_dashlet.set_geometry(50, 750, 800, 100)

        shiftlights_dashlet = rfactorlcd.ShiftlightsDashlet(self, self.lcd_style)
        shiftlights_dashlet.set_geometry(00, 0, 1200, 80)

        # rpm2_dashlet = rfactorlcd.RPM2Dashlet(self, self.lcd_style)
        # rpm2_dashlet.set_geometry(600, 400, 400, 300)

        self.dashlets = [rpm_dashlet, speed_dashlet, temp_dashlet,
                         sector_dashlet, laptime_dashlet, position_dashlet, 
                         shiftlights_dashlet]

        self.active_dashlet = None
        self.drag_dashlet = None
        self.drag_start = None

        #self.set_events(gtk.MOTION_NOTIFY)

        self.set_events(gtk.gdk.EXPOSURE_MASK
                        | gtk.gdk.LEAVE_NOTIFY_MASK
                        | gtk.gdk.BUTTON_PRESS_MASK
                        | gtk.gdk.BUTTON_RELEASE_MASK
                        | gtk.gdk.POINTER_MOTION_MASK
                        | gtk.gdk.POINTER_MOTION_HINT_MASK)

        self.connect("motion_notify_event", self.on_motion_notify)
        self.connect("button_press_event", self.on_button_press)
        self.connect("button_release_event", self.on_button_release)

    def on_button_press(self, widget, event):
        print "press", event.x, event.y, event.button
        if event.button == 1:
            self.drag_dashlet = self.active_dashlet
            if self.drag_dashlet:
                self.drag_dashlet_origin = (self.drag_dashlet.x, self.drag_dashlet.y)
                self.drag_start = (event.x, event.y)

    def on_button_release(self, widget, event):
        print "release", event.x, event.y, event.button
        if event.button == 1:
            self.drag_dashlet = None

    def on_motion_notify(self, widget, event):
        if self.drag_dashlet is not None:
            x = event.x - self.drag_start[0]
            y = event.y - self.drag_start[1]

            self.drag_dashlet.x = self.drag_dashlet_origin[0] + x
            self.drag_dashlet.y = self.drag_dashlet_origin[1] + y

            self.queue_draw()
        else:
            active_dashlet = None
            for dashlet in self.dashlets:
                if dashlet.x <= event.x < dashlet.x2 and \
                   dashlet.y <= event.y < dashlet.y2:
                    active_dashlet = dashlet
                    break

            if active_dashlet != self.active_dashlet:
                self.active_dashlet = active_dashlet
                self.queue_draw()

    def set_lcd_style(self, style):
        self.lcd_style = style

        for dashlet in self.dashlets:
            dashlet.lcd_style = self.lcd_style

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

            for dashlet in self.dashlets:
                cr.save()
                cr.translate(dashlet.x, dashlet.y)
                dashlet.draw(cr)
                cr.restore()

                if dashlet == self.active_dashlet:
                    cr.set_source_rgb(*self.lcd_style.highlight_color)
                    cr.rectangle(dashlet.x, dashlet.y,
                                 dashlet.w, dashlet.h)
                    cr.stroke()

    def update_state(self, state):
        self.rf_state = state

        for dashlet in self.dashlets:
            dashlet.update_state(state)

            if dashlet.needs_redraw:
                self.queue_draw_area(int(dashlet.x), int(dashlet.y),
                                     int(dashlet.w), int(dashlet.h))


# EOF #
