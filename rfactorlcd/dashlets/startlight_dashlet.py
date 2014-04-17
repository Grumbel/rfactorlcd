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


class StartlightDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(StartlightDashlet, self).__init__(*args)

        self.start_light = 0
        self.num_red_lights = 0

    def reshape(self, x, y, w, h):
        pass

    def update_state(self, state):
        if self.start_light != state.start_light or \
           self.num_red_lights != state.num_red_lights:
            self.start_light = state.start_light
            self.num_red_lights = state.num_red_lights
            self.queue_draw()

    def draw(self, cr):
        if self.num_red_lights > 0:
            r = (self.w / self.num_red_lights) / 2
            for i in range(self.num_red_lights):
                cr.arc(i * r * 2 + r, self.h/2, r * 0.9, 0, 2*math.pi)

                if self.start_light > self.num_red_lights:
                    cr.set_source_rgb(0, 1, 0)
                    cr.fill()
                elif i < self.start_light:
                    cr.set_source_rgb(1, 0, 0)
                    cr.fill()
                else:
                    cr.set_line_width(2.0)
                    cr.set_source_rgb(*self.lcd_style.shadow_color)
                    cr.stroke()


# EOF #
