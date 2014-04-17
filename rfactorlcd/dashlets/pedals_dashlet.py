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


class PedalsDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(PedalsDashlet, self).__init__(*args)

        self.throttle = 0
        self.brake = 0
        self.clutch = 0

    def update_state(self, state):
        if self.throttle != state.throttle or \
           self.brake != state.brake or \
           self.clutch != state.clutch:
            self.throttle = state.throttle
            self.brake = state.brake
            self.clutch = state.clutch
            self.queue_draw()

    def draw(self, cr):
        cr.set_line_width(2.0)
        cr.set_source_rgb(*self.lcd_style.shadow_color)
        for i, p in enumerate([self.throttle, self.brake, self.clutch]):
            cr.rectangle(self.w / 3 * i, 0,
                         self.w / 3, self.h)
        cr.stroke()

        pedal_colors = [(0, 1, 0),
                        (1, 0, 0),
                        (0, 0, 1)]
        for i, p in enumerate([self.throttle, self.brake, self.clutch]):
            cr.set_source_rgb(*pedal_colors[i])
            cr.rectangle(self.w / 3 * i, (1.0 - p) * self.h,
                         self.w / 3, p * self.h)
            cr.fill()


# EOF #
