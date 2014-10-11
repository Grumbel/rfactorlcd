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


import math
import cairo

import rfactorlcd


class RPMDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(RPMDashlet, self).__init__(*args)

        self.background = None

        self.inner_r = 250.0
        self.outer_r = 300.0

        self.start_angle = 90
        self.end_angle = 360

        self.rpm = 0
        self.gear = 0
        self.max_rpm = 10000
        self.dmax_rpm = 10000

    def reshape(self, x, y, w, h):
        max_radius = min(w, h) / 2

        self.inner_r = max_radius * 0.8
        self.outer_r = max_radius

    def update_state(self, state):
        if self.rpm != state.rpm or \
           self.max_rpm != state.max_rpm or \
           self.gear != state.gear:

            self.rpm = state.rpm
            self.max_rpm = state.max_rpm
            self.dmax_rpm = int(self.max_rpm + 999) / 1000 * 1000
            self.gear = state.gear

            if self.max_rpm != 0:
                self.background = None
                self.queue_draw()

    def draw(self, cr):
        if self.dmax_rpm == 0:
            cr.move_to(self.w/2, self.h/2)
            cr.show_text("inactive")
            return

        # drawing background to an offscreen buffer so it doesn't have
        # to be regenerated each time
        if not self.background or \
           self.background.get_width() != self.w or \
           self.background.get_height() != self.h:

            self.background = cr.get_target().create_similar(cairo.CONTENT_COLOR, int(self.w), int(self.h))
            surf_cr = cairo.Context(self.background)

            surf_cr.set_source_rgb(*self.lcd_style.background_color)
            surf_cr.paint()

            surf_cr.save()
            surf_cr.translate(self.w/2, self.h/2)
            self.draw_background(surf_cr)
            surf_cr.restore()

        cr.set_source_surface(self.background)
        cr.paint()

        cr.save()
        cr.translate(self.w/2, self.h/2)
        cr.set_source_rgb(*self.lcd_style.foreground_color)

        # display the rpm/max_rpm
        cr.set_font_size(self.outer_r/6)
        cr.move_to(-self.outer_r/2 + 30, -self.outer_r/2 + 30)
        cr.show_text("%6d" % self.rpm)

        self.draw_needle(cr)
        cr.restore()

        self.draw_gear(cr)

    def draw_needle(self, cr):
        p = self.rpm / self.dmax_rpm

        cr.save()
        cr.rotate(math.radians(self.start_angle + (self.end_angle - self.start_angle - 1) * p))

        cr.new_path()
        cr.arc(0, 0, 10, math.pi/2, math.pi + math.pi/2)
        cr.line_to(self.outer_r, -2)
        cr.line_to(self.outer_r, 2)
        cr.close_path()

        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.fill_preserve()

        cr.set_source_rgb(*self.lcd_style.highlight_dim_color)
        cr.set_line_width(4.0)
        cr.stroke()
        cr.restore()

        cr.new_path()
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_line_width(4.0)
        cr.arc(0, 0, self.outer_r / 10.0, 0, 2*math.pi)
        cr.fill_preserve()
        cr.set_source_rgb(*self.lcd_style.shadow_color)
        cr.stroke()
        cr.close_path()

    def draw_background(self, cr):
        cr.move_to(0, 0)

        cr.set_line_width(6.0)
        cr.set_source_rgb(*self.lcd_style.shadow_color)
        for rpm in range(0, int(self.dmax_rpm+1), 200):
            p = rpm / float(self.dmax_rpm)
            deg = self.start_angle + (self.end_angle - self.start_angle) * p
            rad = math.radians(deg)

            x = math.cos(rad)
            y = math.sin(rad)

            cr.move_to(x * self.inner_r,
                       y * self.inner_r)
            cr.line_to(x * (self.inner_r + (self.outer_r - self.inner_r) * 0.75),
                       y * (self.inner_r + (self.outer_r - self.inner_r) * 0.75))
            cr.stroke()

        # draw max_rpm needle
        cr.set_line_width(6.0)
        cr.set_source_rgb(*self.lcd_style.highlight_dim_color)
        p = self.max_rpm / float(self.dmax_rpm)
        deg = self.start_angle + (self.end_angle - self.start_angle) * p
        rad = math.radians(deg)
        x = math.cos(rad)
        y = math.sin(rad)
        cr.move_to(0, 0)
        cr.line_to(x * self.outer_r,
                   y * self.outer_r)
        cr.stroke()

        cr.set_line_width(8.0)
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        for rpm in range(0, int(self.dmax_rpm+1), 1000):
            p = rpm / float(self.dmax_rpm)
            deg = self.start_angle + (self.end_angle - self.start_angle) * p
            rad = math.radians(deg)
            if True:
                x = math.cos(rad)
                y = math.sin(rad)

                cr.move_to(x * self.inner_r,
                           y * self.inner_r)
                cr.line_to(x * self.outer_r,
                           y * self.outer_r)
                cr.stroke()
            else:
                step_s = 0.08
                cr.arc_negative(0, 0, self.outer_r, rad + step_s, rad - step_s)
                cr.arc(0, 0, self.inner_r, rad - step_s, rad + step_s)
                cr.close_path()
                cr.set_source_rgb(*self.lcd_style.shadow_color)
                cr.fill()

            cr.set_font_size(30)
            txt = "%d" % (rpm / 1000)
            x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents(txt)
            cr.move_to(x * self.inner_r * 0.9 - width/2
                       - self.w/100.0,  # random beauty offset
                       y * self.inner_r * 0.9 + height/2)
            cr.show_text(txt)

    def draw_gear(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(self.w/2 + self.outer_r * 0.25,
                   self.h/2 + self.outer_r * 0.9)
        cr.set_font_size(self.outer_r)
        if self.gear == 0:
            cr.show_text("N")
        elif self.gear == -1:
            cr.show_text("R")
        else:
            cr.show_text(str(self.gear))


# EOF #
