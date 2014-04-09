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

    def __init__(self, data=None):
        if data:
            cols = data.split(",")
            self.position = cols[0]
            self.unknowns = cols[1:7]
            self.laptime = cols[8]
            self.speed = float(cols[9])
            self.gear = int(cols[10])
            self.fuel = float(cols[11])
            self.oil_temp = float(cols[12])
            self.water_temp = float(cols[13])
            self.rpm = float(cols[14])
            self.max_rpm = float(cols[15])
            if self.max_rpm == 0:
                self.max_rpm = 1
        else:
            self.unknowns = ["u1", "u2", "u3", "u4", "u5", "u6"]
            self.position = "17/17"
            self.speed = 100
            self.gear = 3
            self.laptime = "2:27.36"
            self.oil_temp = 30.5
            self.water_temp = 29.5
            self.fuel = 10.0
            self.rpm = 4000.0
            self.max_rpm = 6000.0


# EOF #
