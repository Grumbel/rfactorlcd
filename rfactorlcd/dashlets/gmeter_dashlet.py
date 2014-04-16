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


import rfactorlcd
import math
import collections

class GMeterDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(GMeterDashlet, self).__init__(*args)
        self.local_accel = (0, 0, 0)
        self.maxlen = 20
        self.accel_history = collections.deque(maxlen=self.maxlen)

    def update_state(self, state):
        
        if self.local_accel != state.local_accel:
            self.accel_history.append(self.local_accel)
            self.local_accel = state.local_accel
            self.queue_draw()


    def draw(self, cr):
        r = min(self.w/2, self.h/2) - 16
        
        # background
        cr.new_path()
        cr.arc(self.w/2, self.h/2, r/3*1, 0, 2*math.pi)
        cr.new_sub_path()
        cr.arc(self.w/2, self.h/2, r/3*2, 0, 2*math.pi)
        cr.new_sub_path()
        cr.arc(self.w/2, self.h/2, r/3*3, 0, 2*math.pi)

        cr.move_to(self.w/2, 0)
        cr.line_to(self.w/2, self.h)
        cr.move_to(0, self.h/2)
        cr.line_to(self.w, self.h/2)

        cr.set_source_rgb(*self.lcd_style.shadow_color)
        cr.set_line_width(4.0)
        cr.stroke()
        
        c = self.lcd_style.highlight_color
        for i, local_accel in enumerate(self.accel_history):
            # meters/sec^2
            accel_x = -local_accel[0] / 9.80665 / 3.0 * r
            accel_y = local_accel[2] / 9.80665 / 3.0 * r

            p = (i+1.0)/self.maxlen
            cr.set_source_rgb(c[0] * p,
                              c[1] * p,
                              c[2] * p)
            cr.arc(self.w/2 + accel_x, self.h/2 + accel_y, 8, 0, 2*math.pi)
            cr.fill()

# EOF #
