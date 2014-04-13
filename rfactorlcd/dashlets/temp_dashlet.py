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


class TempDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(TempDashlet, self).__init__(*args)
        self.oil_temp = 0
        self.water_temp = 0
        self.fuel = 0
        self.font_size = 20

    def set_geometry(self, x, y, w, h):
        super(TempDashlet, self).set_geometry(x, y, w, h)
        self.font_size = self.h / 3

    def update_state(self, state):
        if self.oil_temp != state.oil_temp or \
           self.water_temp != state.water_temp or \
           self.fuel != state.fuel:

            self.oil_temp = state.oil_temp
            self.water_temp = state.water_temp
            self.fuel = state.fuel

            self.queue_draw()

    def draw(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_font_size(self.font_size)

        cr.move_to(0, self.font_size)
        cr.show_text("Oil:")
        cr.move_to(250, self.font_size)
        cr.show_text("%5.1f" % self.oil_temp)

        cr.move_to(0, self.font_size * 2)
        cr.show_text("Water:")
        cr.move_to(250, self.font_size * 2)
        cr.show_text("%5.1f" % self.water_temp)

        cr.move_to(0, self.font_size * 3)
        cr.show_text("Fuel:")
        cr.move_to(250, self.font_size * 3)
        cr.show_text("%5.1f" % self.fuel)


# EOF #
