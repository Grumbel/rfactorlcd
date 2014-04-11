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


class SectorDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(SectorDashlet, self).__init__(*args)
        self.sector = []
        self.unknowns = []

    def update_state(self, state):
        if self.sector != state.sector or \
           self.unknowns != state.unknowns:
            self.sector = state.sector
            self.unknowns = state.unknowns
            self.queue_draw()

    def draw(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_font_size(45)

        for i, v in enumerate(self.sector):
            cr.move_to(0, 45 * i + 45)
            cr.show_text("S%d:" % (i + 1))
            cr.move_to(100, 45 * i + 45)
            cr.show_text("%-6s" % v)

        for i, v in enumerate(self.unknowns):
            cr.move_to(0, 45 * i + 150 + 45)
            cr.show_text("%6s" % v)


# EOF #
