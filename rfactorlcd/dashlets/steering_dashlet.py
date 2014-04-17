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


class SteeringDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(SteeringDashlet, self).__init__(*args)
        self.steering = 0
        self.rotation = math.pi / 2

    def update_state(self, state):
        if self.steering != state.steering:
            self.steering = state.steering

    def draw(self, cr):
        r = min(self.w, self.h)/2.0

        cr.set_source_rgb(*self.lcd_style.shadow_color)
        cr.save()
        cr.translate(self.w/2, self.h/2)
        cr.rotate(self.rotation * self.steering)

        cr.move_to(-r, 0)
        cr.line_to(r, 0)

        cr.move_to(0, 0)
        cr.line_to(0, r)
        cr.stroke()
        cr.restore()

        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.new_path()
        cr.arc(self.w/2, self.h/2,
               r, 0, 2.0 * math.pi)
        cr.stroke()

        cr.new_path()
        cr.arc(self.w/2, self.h/2,
               r/5.0, 0, 2.0 * math.pi)
        cr.fill()


# EOF #
