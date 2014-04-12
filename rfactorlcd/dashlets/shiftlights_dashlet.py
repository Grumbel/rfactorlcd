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


class ShiftlightsDashlet(rfactorlcd.Dashlet):
 
    def __init__(self, *args):
        super(ShiftlightsDashlet, self).__init__(*args)

        self.rpm = 0
        self.max_rpm = 0

    def set_geometry(self, x, y, w, h):
        super(ShiftlightsDashlet, self).set_geometry(x, y, w, h)

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

        n = 15
        r = self.h/2 * 0.8
        for i in range(0, n):
            cr.new_path()
            cr.arc((i+0.5) * self.w / n,
                   self.h/2, r,
                   0, 2 * math.pi)
            
            p = ((i+1.0) / n)
            if p * 0.9 > (rpm_p - 0.5) * 2:
                cr.set_source_rgb(0.4, 0.4, 0.4)
                cr.fill_preserve()
                cr.set_source_rgb(0.2, 0.2, 0.2)
                cr.stroke()
            else:
                if i >= 10:
                    cr.set_source_rgb(0, 0.8, 1.0)
                    cr.fill_preserve()
                    cr.set_source_rgb(0, 0.6, 0.8)
                    cr.stroke()
                elif i >= 5:
                    cr.set_source_rgb(1, 0, 0)
                    cr.fill_preserve()
                    cr.set_source_rgb(0.8, 0, 0)
                    cr.stroke()
                else:
                    cr.set_source_rgb(0, 1, 0)
                    cr.fill_preserve()
                    cr.set_source_rgb(0, 0.8, 0)
                    cr.stroke()


# EOF #
