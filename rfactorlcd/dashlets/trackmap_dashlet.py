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


class TrackmapDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(TrackmapDashlet, self).__init__(*args)

        self.vehicles = []
        self.lap_dist = 1.0
        self.background = None

    def reshape(self, x, y, w, h):
        pass

    def update_state(self, state):
        self.vehicles = state.vehicles
        self.lap_dist = state.lap_dist
        self.queue_draw()

    def draw(self, cr):
        if self.background is None:
            self.background = cr.get_target().create_similar(cairo.CONTENT_COLOR, int(self.w), int(self.h))

        cr.move_to(0, 0)
        cr.set_source_surface(self.background)
        cr.paint()

        cr.new_path()
        for veh in self.vehicles:
            x = -veh.pos[0] / 5.0 + self.background.get_width()/2
            y = -veh.pos[2] / 5.0 + self.background.get_height()/2

            cr.arc(x, y, 2, 0, 2*math.pi)

            if veh.is_player:
                cr.set_source_rgb(*self.lcd_style.highlight_color)
            else:
                cr.set_source_rgb(*self.lcd_style.foreground_color)
            cr.fill()

        cr = cairo.Context(self.background)
        for veh in self.vehicles:
            x = -veh.pos[0] / 5.0 + self.background.get_width()/2
            y = -veh.pos[2] / 5.0 + self.background.get_height()/2

            cr.arc(x, y, 4, 0, 2*math.pi)

            cr.set_source_rgb(*self.lcd_style.shadow_color)
            cr.fill()


# EOF #
