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


class SpeedometerDashlet(rfactorlcd.Dashlet):
    def __init__(self, *args):
        super(SpeedometerDashlet, self).__init__(*args)

        self.inner_r = 200
        self.outer_r = 250

        self.start = 140 - 90
        self.end = 400 - 90

        self.max_speed = 320

    def set_geometry(self, x, y, w, h):
        super(SpeedometerDashlet, self).set_geometry(x, y, w, h)

    def update_state(self, state):
        self.queue_draw()

    def draw(self, cr):
        cr.save()
        cr.translate(self.w/2, self.h/2)
        self.draw_background(cr)
        cr.restore()

    def draw_background(self, cr):
        cr.new_path()
        for deg in range(self.start, self.end + 1,
                         (self.end - self.start) / (self.max_speed / 20)):
            rad = math.radians(deg)

            x = math.sin(rad)
            y = math.cos(rad)

            cr.set_source_rgb(*self.lcd_style.foreground_color)
            cr.set_line_width(12.0)
            cr.move_to(x * self.inner_r,
                       y * self.inner_r)
            cr.line_to(x * self.outer_r,
                       y * self.outer_r)
            cr.stroke()

            cr.set_font_size(30)
            txt = "%d" % deg
            x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents(txt)
            cr.move_to(x * self.inner_r * 0.87 - width/2,
                       y * self.inner_r * 0.87 + height/2)
            cr.show_text(txt)

# EOF #
