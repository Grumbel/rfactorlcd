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
import io


def perc2py(text):
    """Assetto Corsa strings end with a '%', not with a traditional '\0'"""
    return text.split(b'%', 1)[0]

def utf16topy(asciz):
    return perc2py(asciz).decode("utf-16").encode("latin-1")


class HandshakeResponse:
    def __init__(self, data):
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

    def __str__(self):
        sout = io.BytesIO()
        print >>sout, "[Handshake]"
        print >>sout, "name:", self.name
        print >>sout, "driver:", self.driver
        print >>sout, "id:", self.identifier
        print >>sout, "version:", self.version
        print >>sout, "track_name:", self.track_name
        print >>sout, "track_config:", self.track_config
        return sout.getvalue()

class RTLap:
    def __init__(self, rawdata):
        data = struct.unpack("<II100s50s2sI", rawdata)
        (self.carIdentifierNumber,
         self.lap,
         self.driverName,
         self.carName,
         self.unknown,
         self.time,
         ) = data
        self.driverName = utf16topy(self.driverName)
        self.carName = perc2py(self.carName)

    def __str__(self):
        sout = io.BytesIO()
        print >>sout, "[Lap]"
        print >>sout, "id:", self.carIdentifierNumber
        print >>sout, "lap:", self.lap
        print >>sout, "driver:", self.driverName
        print >>sout, "carName:", self.carName
        print >>sout, "time:", self.time
        print >>sout, "unknown:", repr(self.unknown)
        return sout.getvalue()

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

    def __str__(self):
        sout = io.BytesIO()

        print >>sout, "[CarInfo]"
        print >>sout, "id:", self.identifier
        print >>sout, "size:", self.size
        print >>sout, "km/h:",  self.speed_Kmh
        print >>sout, "mps:", self.speed_Mph
        print >>sout, "m/s:", self.speed_Ms

        print >>sout, "isAbsEnabled:", self.isAbsEnabled
        print >>sout, "isAbsInAction:", self.isAbsInAction
        print >>sout, "isTcInAction:", self.isTcInAction
        print >>sout, "isTcEnabled:", self.isTcEnabled
        print >>sout, "isInPit:", self.isInPit
        print >>sout, "isEngineLimiterOn:", self.isEngineLimiterOn

        print >>sout, "accG_vertical:", self.accG_vertical
        print >>sout, "accG_horizontal:", self.accG_horizontal
        print >>sout, "accG_frontal:", self.accG_frontal

        print >>sout, "lapTime:", self.lapTime
        print >>sout, "lastLap:", self.lastLap
        print >>sout, "bestLap:", self.bestLap
        print >>sout, "lapCount:", self.lapCount

        print >>sout, "unknown:", self.unknown

        print >>sout, "gas:", self.gas
        print >>sout, "brake:", self.brake
        print >>sout, "clutch:", self.clutch
        print >>sout, "engineRPM:", self.engineRPM
        print >>sout, "steer:", self.steer
        print >>sout, "gear:", self.gear
        print >>sout, "cgHeight:", self.cgHeight

        print >>sout, "wheelAngularSpeed:", self.wheelAngularSpeed
        print >>sout, "slipAngle:", self.slipAngle
        print >>sout, "slipAngle_ContactPatch:", self.slipAngle_ContactPatch

        print >>sout, "wheelAngularSpeed:", self.wheelAngularSpeed
        print >>sout, "slipAngle:", self.slipAngle
        print >>sout, "slipAngle_ContactPatch:", self.slipAngle_ContactPatch
        print >>sout, "slipRatio:", self.slipRatio
        print >>sout, "tyreSlip:", self.tyreSlip
        print >>sout, "ndSlip:", self.ndSlip
        print >>sout, "load:", self.load
        print >>sout, "Dy:", self.Dy
        print >>sout, "Mz:", self.Mz
        print >>sout, "tyreDirtyLevel:", self.tyreDirtyLevel

        print >>sout, "camberRAD:", self.camberRAD
        print >>sout, "tyreRadius:", self.tyreRadius
        print >>sout, "tyreLoadedRadius:", self.tyreLoadedRadius

        print >>sout, "suspensionHeight:", self.suspensionHeight

        print >>sout, "carPositionNormalized:", self.carPositionNormalized
        print >>sout, "carSlope:", self.carSlope
        print >>sout, "carCoordinates:", self.carCoordinates

        return sout.getvalue()


# EOF #
