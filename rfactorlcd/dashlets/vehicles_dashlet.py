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


class VehiclesDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(VehiclesDashlet, self).__init__(*args)
        self.vehicles = []

    def update_state(self, state):
        self.vehicles = state.vehicles
        self.queue_draw()

    def draw(self, cr):
        if len(self.vehicles) > 0:
            font_size = self.h / len(self.vehicles)
            y = font_size
            cr.set_font_size(font_size)
            cr.set_source_rgb(*self.lcd_style.foreground_color)
            for veh in sorted(self.vehicles, lambda a, b: cmp(a.place, b.place)):
                cr.move_to(0, font_size)
                cr.show_text("%d %s" % (veh.place, veh.driver_name))
                y += font_size


# EOF #
