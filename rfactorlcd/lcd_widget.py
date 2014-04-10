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
import math

import rfactorlcd


class LCDWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.rf_state = rfactorlcd.rFactorState()
        self.lcd_style = rfactorlcd.Style.white_on_black()

        rpm_dashlet = rfactorlcd.RPMDashlet(self, self.lcd_style)
        rpm_dashlet.set_geometry(100, 100, 400, 400)

        self.dashlets = [rpm_dashlet]

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

            cr.set_source_rgb(*self.lcd_style.background_color)
            cr.paint()
            self.draw(cr, 1200, 900, self.rf_state)

            for dashlet in self.dashlets:
                cr.save()
                dashlet.draw(cr)
                cr.restore()

    def update_state(self, state):
        self.rf_state = state

        for dashlet in self.dashlets:
            dashlet.update_state(state)

        self.queue_draw()

    def draw(self, cr, w, h, state):
        cr.set_antialias(cairo.ANTIALIAS_NONE)
        cr.set_line_width(8.0)
        # cr.set_line_cap(cairo.LINE_CAP_ROUND)

        cr.select_font_face(self.lcd_style.font,
                            self.lcd_style.font_slant,
                            self.lcd_style.font_weight)
        # font_face = cr.get_font_face()
        # print(font_face)

        # self.draw_rpm_meter(cr, 700, 480, state.rpm, state.max_rpm)
        self.draw_speed(cr, 650, 200, state.speed)
        self.draw_laptime(cr, 50, 770, state.laptime)
        self.draw_position(cr, 50, 870, state.position)
        self.draw_temp(cr, 700, 300, state.oil_temp, state.water_temp, state.fuel)
        self.draw_unknows(cr, 750, 550, state.unknowns)
        self.draw_sectors(cr, 750, 750, state.sector)

    def draw_temp(self, cr, cx, cy, oil, water, fuel):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_font_size(60)

        cr.move_to(cx, cy)
        cr.show_text("Oil:")
        cr.move_to(cx+250, cy)
        cr.show_text("%5.1f" % oil)

        cr.move_to(cx, cy + 80)
        cr.show_text("Water:")
        cr.move_to(cx+250, cy + 80)
        cr.show_text("%5.1f" % water)

        cr.move_to(cx, cy + 160)
        cr.show_text("Fuel:")
        cr.move_to(cx+250, cy + 160)
        cr.show_text("%5.1f" % fuel)

    def draw_sectors(self, cr, cx, cy, sector):
        for i, v in enumerate(sector):
            cr.move_to(cx, cy + 45 * i)
            cr.show_text("S%d:" % (i + 1))
            cr.move_to(cx + 100, cy + 45 * i)
            cr.show_text("%-6s" % v)

    def draw_unknows(self, cr, cx, cy, unknowns):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_font_size(45)
        for i, v in enumerate(unknowns):
            cr.move_to(cx, cy + 45 * i)
            cr.show_text("%6s" % v)

    def draw_position(self, cr, cx, cy, position):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(cx, cy)
        cr.set_font_size(75)
        cr.show_text("POS: %s" % position)

    def draw_speed(self, cr, cx, cy, speed):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(cx, cy)
        cr.set_font_size(180)
        cr.show_text("%3d" % speed)
        cr.set_font_size(90)
        cr.show_text("km/h")

    def draw_laptime(self, cr, cx, cy, laptime):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(cx, cy)
        cr.set_font_size(75)
        cr.show_text("LAP: %s" % laptime)

    def draw_rpm_meter(self, cr, cx, cy, rpm, max_rpm):
        if max_rpm == 0:
            rpm_p = 0.0
        else:
            rpm_p = rpm / max_rpm

        inner_r = 600.0
        outer_r = 700.0

        inner_squish = 0.4
        outer_squish = 0.6

        inner_offset = 50
        inner_trail = 0.0

        inner_ramp = 0.98

        cr.save()
        cr.translate(cx, cy)

        start = 150
        end = 260
        for deg in range(start, end, 2):
            p = 1.0 - (float(deg - start) / (end - start - 1))

            if p > rpm_p:
                cr.set_source_rgb(0.85, 0.85, 0.85)
            else:
                cr.set_source_rgb(0.0, 0.0, 0.0)

            rad = math.radians(deg)
            x = math.sin(rad)
            y = math.cos(rad)

            ix = math.sin(inner_ramp * rad - inner_trail)
            iy = math.cos(inner_ramp * rad - inner_trail)

            cr.move_to(ix * inner_r, iy * inner_r * inner_squish)
            cr.line_to(x * outer_r + inner_offset, y * outer_r * outer_squish)
            cr.stroke()

        cr.restore()


# EOF #
