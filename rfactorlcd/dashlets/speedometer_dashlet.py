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


class SpeedometerDashlet(rfactorlcd.Dashlet):
    def __init__(self, *args):
        super(SpeedometerDashlet, self).__init__(*args)

        self.background = None

        self.inner_r = 200
        self.outer_r = 250

        self.start_angle = 140
        self.end_angle = 400

        self.max_speed = 320
        self.speed_step = 20

        self.speed = 0

    def reshape(self, x, y, w, h):
        r = min(self.w, self.h) / 2
        self.inner_r = r * 0.8
        self.outer_r = r * 0.95

    def update_state(self, state):
        if self.speed != state.speed:
            self.speed = state.speed
            self.queue_draw()

    def draw(self, cr):
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
        self.draw_needle(cr)
        cr.restore()

    def draw_needle(self, cr):
        p = self.speed / float(self.max_speed)

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
        cr.new_path()

        for speed in range(self.speed_step/2, self.max_speed+1, self.speed_step):
            p = speed / float(self.max_speed)
            deg = self.start_angle + (self.end_angle - self.start_angle) * p
            rad = math.radians(deg)

            x = math.cos(rad)
            y = math.sin(rad)

            cr.set_source_rgb(*self.lcd_style.shadow_color)
            cr.set_line_width(6.0)
            cr.move_to(x * self.inner_r * 1.05,
                       y * self.inner_r * 1.05)
            cr.line_to(x * self.outer_r * 0.95,
                       y * self.outer_r * 0.95)
            cr.stroke()

        for speed in range(0, self.max_speed+1, self.speed_step):
            p = speed / float(self.max_speed)
            deg = self.start_angle + (self.end_angle - self.start_angle) * p
            rad = math.radians(deg)

            x = math.cos(rad)
            y = math.sin(rad)

            cr.set_source_rgb(*self.lcd_style.foreground_color)
            cr.set_line_width(8.0)
            cr.move_to(x * self.inner_r,
                       y * self.inner_r)
            cr.line_to(x * self.outer_r,
                       y * self.outer_r)
            cr.stroke()

            cr.set_font_size(20)
            txt = "%d" % speed
            x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents(txt)
            cr.move_to(x * self.inner_r * 0.9 - width/2
                       - self.w/100.0,  # random beauty offset
                       y * self.inner_r * 0.9 + height/2)
            cr.show_text(txt)

# EOF #
