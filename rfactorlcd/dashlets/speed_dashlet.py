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


class SpeedDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(SpeedDashlet, self).__init__(*args)
        self.speed = 0

    def update_state(self, state):
        if self.speed != state.speed:
            self.speed = state.speed
            self.queue_draw()

    def draw(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(0, self.h)
        cr.set_font_size(self.h)
        cr.show_text("%3d" % self.speed)
        cr.set_font_size(self.h/2)
        cr.show_text("km/h")


# EOF #
