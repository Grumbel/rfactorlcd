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


class rFactorState(object):

    def __init__(self, data="15/17,1,0.107,1.438,1.658,21.598,29.738,31.855,1:23.190,0.0,0,30.0,63.4,26.9,0.0,0.0"):
        self.data = data

        cols = data.split(",")
        self.position = cols[0]
        self.unknowns = cols[1:5]
        self.sector = cols[5:8]
        self.laptime = cols[8]
        self.speed = float(cols[9])
        self.gear = int(cols[10])
        self.fuel = float(cols[11])
        self.oil_temp = float(cols[12])
        self.water_temp = float(cols[13])
        self.rpm = float(cols[14])
        self.max_rpm = float(cols[15])

    def to_vracingDisplayPRO(self):
        result = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            self.position,
            self.unknowns[0],
            self.unknowns[1],
            self.unknowns[2],
            self.unknowns[3],
            self.sector[0],
            self.sector[1],
            self.sector[2],
            self.laptime,
            self.speed,
            self.gear,
            self.fuel,
            self.oil_temp,
            self.water_temp,
            self.rpm,
            self.max_rpm)
        
        # print "IN: ", self.data
        # print "OUT: ", result

        return result


# EOF #
