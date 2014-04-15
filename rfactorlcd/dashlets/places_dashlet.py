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


class PlacesDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(PlacesDashlet, self).__init__(*args)

        self.vehicles = []
        self.lap_dist = 1.0

    def update_state(self, state):
        self.vehicles = state.vehicles
        self.lap_dist = state.lap_dist
        self.queue_draw()

    def draw(self, cr):
        cr.set_line_width(2.0)
        cr.move_to(0, self.h/2)
        cr.line_to(self.w, self.h/2)
        cr.set_source_rgb(*self.lcd_style.shadow_color)
        cr.stroke()

        for vehicle in self.vehicles:
            p = vehicle.lap_dist / self.lap_dist
            p = p % 1.0

            cr.rectangle(p * self.w - 8,
                         self.h / 2 - 8,
                         16, 16)

            if vehicle.is_player:
                cr.set_source_rgb(0, 1.0, 0)
            elif vehicle.place == 1:
                cr.set_source_rgb(1.0, 1.0, 1.0)
            else:
                cr.set_source_rgb(*self.lcd_style.highlight_color)
            cr.fill_preserve()

            cr.set_line_width(1.0)
            cr.set_source_rgb(*self.lcd_style.highlight_dim_color)
            cr.stroke()


# EOF #
