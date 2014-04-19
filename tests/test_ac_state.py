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
        print "[Handshake]"
        print "name:", data.name
        print "driver:", data.driver
        print "id:", data.identifier
        print "version:", data.version
        print "track_name:", data.track_name
        print "track_config:", data.track_config

    def test_lap_parsing(self):
        print len(lap_data)
        lapinfo = RTLap(lap_data)
        print "[Lap]"
        print "id:", lapinfo.carIdentifierNumber
        print "lap:", lapinfo.lap
        print "driver:", lapinfo.driverName
        print "carName:", lapinfo.carName
        print "time:", lapinfo.time
        print "rest:", repr(lapinfo.rest)

    def test_carinfo_parsing(self):
        print len(car_data)
        car = RTCarInfo(car_data)
        print "[CarInfo]"
        print "id:", car.identifier
        print "size:", car.size
        print "km/h:",  car.speed_Kmh
        print "mps:", car.speed_Mph
        print "m/s:", car.speed_Ms

        print "isAbsEnabled:", car.isAbsEnabled
        print "isAbsInAction:", car.isAbsInAction
        print "isTcInAction:", car.isTcInAction
        print "isTcEnabled:", car.isTcEnabled
        print "isInPit:", car.isInPit
        print "isEngineLimiterOn:", car.isEngineLimiterOn

        print "accG_vertical:", car.accG_vertical
        print "accG_horizontal:", car.accG_horizontal
        print "accG_frontal:", car.accG_frontal

        print "lapTime:", car.lapTime
        print "lastLap:", car.lastLap
        print "bestLap:", car.bestLap
        print "lapCount:", car.lapCount

        print "unknown:", car.unknown

        print "gas:", car.gas
        print "brake:", car.brake
        print "clutch:", car.clutch
        print "engineRPM:", car.engineRPM
        print "steer:", car.steer
        print "gear:", car.gear
        print "cgHeight:", car.cgHeight

        print "wheelAngularSpeed:", car.wheelAngularSpeed
        print "slipAngle:", car.slipAngle
        print "slipAngle_ContactPatch:", car.slipAngle_ContactPatch

        print "wheelAngularSpeed:", car.wheelAngularSpeed
        print "slipAngle:", car.slipAngle
        print "slipAngle_ContactPatch:", car.slipAngle_ContactPatch
        print "slipRatio:", car.slipRatio
        print "tyreSlip:", car.tyreSlip
        print "ndSlip:", car.ndSlip
        print "load:", car.load
        print "Dy:", car.Dy
        print "Mz:", car.Mz
        print "tyreDirtyLevel:", car.tyreDirtyLevel

        print "camberRAD:", car.camberRAD
        print "tyreRadius:", car.tyreRadius
        print "tyreLoadedRadius:", car.tyreLoadedRadius

        print "suspensionHeight:", car.suspensionHeight

        print "carPositionNormalized:", car.carPositionNormalized
        print "carSlope:", car.carSlope
        print "carCoordinates:", car.carCoordinates


if __name__ == '__main__':
    unittest.main()


# EOF #
