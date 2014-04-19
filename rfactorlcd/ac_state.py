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


import struct

def perc2py(text):
    return text.split(b'%', 1)[0]

def asciz2py(asciz):
    return asciz.split(b'\x00', 1)[0]

def utf16topy(asciz):
    return perc2py(asciz).decode("utf-16")

class HandshakeResponse:
    def __init__(self, data):
        print "-----", len(data)
        (self.name,
         self.driver,
         self.identifier,
         self.version,
         self.track_name,
         self.track_config) = struct.unpack("50s100sII50s50s", data)
        self.name = perc2py(self.name)
        self.driver = utf16topy(self.driver)
        self.track_name = perc2py(self.track_name)
        self.track_config = perc2py(self.track_config)


class RTLap:
    def __init__(self, rawdata):
        print "--------", len(rawdata)
        data = struct.unpack("<II100s50sI2s", rawdata)
        (self.carIdentifierNumber,
         self.lap,
         self.driverName,
         self.carName,
         self.time,
         self.rest) = data
        self.driverName = utf16topy(self.driverName)
        self.carName = perc2py(self.carName)

class RTCarInfo:
    def __init__(self, rawdata):
        data = struct.unpack("<4sI3f6B3fBB4I5fIf40f16fff3f", rawdata)

        self.identifier = data[0]
        self.size = data[1]
        self.speed_Kmh = data[2]
        self.speed_Mph = data[3]
        self.speed_Ms = data[4]

        self.isAbsEnabled = data[5]
        self.isAbsInAction = data[6]
        self.isTcInAction = data[7]
        self.isTcEnabled = data[8]
        self.isInPit = data[9]
        self.isEngineLimiterOn = data[10]

        self.accG_vertical = data[11]
        self.accG_horizontal = data[12]
        self.accG_frontal = data[13]

        self.unknown = data[14:16]

        self.lapTime = data[16]
        self.lastLap = data[17]
        self.bestLap = data[18]
        self.lapCount = data[19]

        self.gas = data[20]
        self.brake = data[21]
        self.clutch = data[22]
        self.engineRPM = data[23]
        self.steer = data[24]
        self.gear = data[25]
        self.cgHeight = data[26]

        self.wheelAngularSpeed = data[27:31]
        self.slipAngle = data[31:35]
        self.slipAngle_ContactPatch = data[35:39]
        self.slipRatio = data[39:43]
        self.tyreSlip = data[43:47]
        self.ndSlip = data[47:51]
        self.load = data[51:55]
        self.Dy = data[55:59]
        self.Mz = data[59:63]
        self.tyreDirtyLevel = data[63:67]

        self.camberRAD = data[67:71]
        self.tyreRadius = data[71:75]
        self.tyreLoadedRadius = data[75:79]

        self.suspensionHeight = data[79:83]

        self.carPositionNormalized = data[83]
        self.carSlope = data[84]
        self.carCoordinates = data[85:88]


# EOF #
