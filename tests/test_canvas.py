#!/usr/bin/env python3

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


import unittest

import rfactorlcd
import rfactorlcd.state
import rfactorlcd.canvas as canvas

class CanvasTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_canvas(self):
        root = canvas.Group()
        root.add_text(0, 0, "Left", canvas.Alignment.LEFT)
        root.add_text(0, 0, "Right", canvas.Alignment.RIGHT)
        root.add_text(0, 0, "Top", canvas.Alignment.TOP)
        root.add_text(0, 0, "Bottom", canvas.Alignment.BOTTOM)
        root.add_rectangle(-8, -8, 16, 16)

if __name__ == '__main__':
    unittest.main()


# EOF #
