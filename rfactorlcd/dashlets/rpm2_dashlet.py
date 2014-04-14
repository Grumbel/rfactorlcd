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


class RPM2Dashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(RPM2Dashlet, self).__init__(*args)
        self.rpm = 0
        self.max_rpm = 0

    def update_state(self, state):
        if self.rpm != state.rpm or \
           self.max_rpm != state.max_rpm:
            self.rpm = state.rpm
            self.max_rpm = state.max_rpm
            self.queue_draw()

    def draw(self, cr):
        if self.max_rpm == 0:
            rpm_p = 0.0
        else:
            rpm_p = self.rpm / self.max_rpm

        inner_r = 600.0
        outer_r = 700.0

        inner_squish = 0.4
        outer_squish = 0.6

        inner_offset = 50
        inner_trail = 0.0

        inner_ramp = 0.98

        cr.save()
        cr.translate(self.w/2, self.h/2)

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
