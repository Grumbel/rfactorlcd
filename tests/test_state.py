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
import struct
import os

import rfactorlcd


class rFactorLCDTestCase(unittest.TestCase):

    def test_state_parsing(self):
        state = rfactorlcd.rFactorState()
        with open(os.path.join(os.path.dirname(__file__), "../raw.log"), "rb") as fin:
            while True:
                data = fin.read(8)
                if data == "":
                    break
                tag, size = struct.unpack("4sI", data)
                print tag, size
                state.dispatch_message(tag, fin.read(size - 8))


if __name__ == '__main__':
    unittest.main()


# EOF #
