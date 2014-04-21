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
import rfactorlcd.canvas as canvas


class TextDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(TextDashlet, self).__init__(*args)
        self.text_item = canvas.Text(0, 0, "N", canvas.Anchor.CENTER)

    def reshape(self, x, y, w, h):
        self.text_item.x = w/2
        self.text_item.y = h/2
        self.text_item.font_size = h

    def draw(self, cr):
        self.text_item.render(cr)


# EOF #
