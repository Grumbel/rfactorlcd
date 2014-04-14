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


class BinaryDecoder:

    def __init__(self, data):
        self.data = data
        self.offset = 0

    def size(self):
        return len(self.data)

    def read_string(self):
        len = struct.unpack_from("B", self.data, self.offset)[0]
        self.offset += 1
        v = struct.unpack_from("%ds" % len, self.data, self.offset)[0]
        self.offset += len
        return v

    def read_char(self):
        v = struct.unpack_from("B", self.data, self.offset)[0]
        self.offset += 1
        return v

    def read_multi_char(self, n):
        v = struct.unpack_from("B" * n, self.data, self.offset)
        self.offset += n
        return v

    def read_short(self):
        v = struct.unpack_from("h", self.data, self.offset)[0]
        self.offset += 2
        return v

    def read_int(self):
        v = struct.unpack_from("i", self.data, self.offset)[0]
        self.offset += 4
        return v

    def read_float(self):
        v = struct.unpack_from("f", self.data, self.offset)[0]
        self.offset += 4
        return v

    def read_vect(self):
        v = struct.unpack_from("fff", self.data, self.offset)
        self.offset += 4 * 3
        return v

    def read_fmt(self, fmt):
        v = struct.unpack_from(fmt, self.offset)
        self.offset += struct.calcsize(fmt)
        return v


# EOF #
