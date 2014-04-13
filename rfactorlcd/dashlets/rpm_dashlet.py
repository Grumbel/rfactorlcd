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

import rfactorlcd


class RPMDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(RPMDashlet, self).__init__(*args)

        self.inner_r = 250.0
        self.outer_r = 300.0

        self.start_angle = 90
        self.end_angle = 360

        self.rpm = 0
        self.max_rpm = 5000
        self.gear = 0

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
            self.gear = state.gear

            self.queue_draw()

    def draw(self, cr):
        cr.save()
        cr.translate(self.w/2, self.h/2)
        cr.set_source_rgb(*self.lcd_style.foreground_color)

        # display the rpm/max_rpm
        cr.set_font_size(self.outer_r/6)
        cr.move_to(-self.outer_r/2, -self.outer_r/2)
        cr.show_text("%6d" % self.rpm)
        cr.move_to(-self.outer_r/2, -self.outer_r/3)
        cr.show_text("%6d" % self.max_rpm)

        self.draw_background(cr)
        self.draw_needle(cr)
        cr.restore()

        self.draw_gear(cr)

    def draw_needle(self, cr):
        p = self.rpm / self.max_rpm

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
        for deg in range(self.start_angle, self.end_angle + 1, 10):  # int((end - start) / int((max_rpm + 500)/1000))):
            rad = math.radians(deg)
            if True:
                x = math.sin(rad)
                y = math.cos(rad)

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
