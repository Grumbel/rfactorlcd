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

from rfactorlcd.ac_state import HandshakeResponse, RTLap, RTCarInfo

datadir = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(datadir, "ac-hand.log"), "rb") as fin:
    handshake_response_data = fin.read()

with open(os.path.join(datadir, "ac-1.log"), "rb") as fin:
    car_data = fin.read()

with open(os.path.join(datadir, "ac-2.log"), "rb") as fin:
    lap_data = fin.read()

class AssettoCorsaStateTestCase(unittest.TestCase):

    def test_handshake_parsing(self):
        data = HandshakeResponse(handshake_response_data)
        print data

    def test_lap_parsing(self):
        print len(lap_data)
        lapinfo = RTLap(lap_data)
        print lapinfo
        
    def test_carinfo_parsing(self):
        print len(car_data)
        car = RTCarInfo(car_data)
        print car

if __name__ == '__main__':
    unittest.main()


# EOF #
