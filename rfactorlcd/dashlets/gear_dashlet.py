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
import rfactorlcd.canvas as canvas

class GearDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(GearDashlet, self).__init__(*args)
        self.gear = 0
        self.text_item = canvas.Text(0, 0, "N")
        self.text_item.alignment = canvas.Alignment.CENTER

    def reshape(self, x, y, w, h):
        pass # self.text_item.style.font_size(h)

    def update_state(self, state):
        if self.gear != state.gear:
            self.gear = state.gear

    def draw(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        #self.text_item.render(cr)

        cr.set_font_size(self.h)
        cr.move_to(0, self.h)

        if self.gear == 0:
            cr.show_text("N")
        elif self.gear == -1:
            cr.show_text("R")
        else:
            cr.show_text(str(self.gear))

# EOF #