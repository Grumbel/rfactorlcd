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


class Text2Dashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(Text2Dashlet, self).__init__(*args)

        self.left_item = canvas.Text(0, 0, "W", canvas.Anchor.W)
        self.right_item = canvas.Text(0, 0, "E", canvas.Anchor.E)

    def reshape(self, x, y, w, h):
        self.left_item.x = 0
        self.left_item.y = h/2
        self.right_item.x = w
        self.right_item.y = h/2
        self.left_item.font_size = h
        self.right_item.font_size = h

    def draw(self, cr):
        self.left_item.render(cr)
        self.right_item.render(cr)


# EOF #
