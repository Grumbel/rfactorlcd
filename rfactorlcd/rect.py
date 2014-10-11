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


class Rect:
    @staticmethod
    def from_points(x1, y1, x2, y2):
        return Rect(x1, y1, x2 - x1, y2 - y1)

    def copy(rect):
        return Rect(rect.x,
                    rect.y,
                    rect.w,
                    rect.h)

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    @property
    def x1(self):
        return self.x

    @property
    def y1(self):
        return self.y

    @x1.setter
    def x1(self, x1):
        self.w = self.w + (self.x - x1)
        self.x = x1

    @y1.setter
    def y1(self, y1):
        self.h = self.h + (self.y - y1)
        self.y = y1

    @property
    def x2(self):
        return self.x + self.w

    @x2.setter
    def x2(self, x2):
        self.w = x2 - self.x

    @property
    def y2(self):
        return self.y + self.h

    @y2.setter
    def y2(self, y2):
        self.h = y2 - self.y

    def __str__(self):
        return "(%.3f, %.3f, %.3f, %.3f)" % (self.x, self.y, self.w, self.h)

    def overlaps(self, other):
        return not (self.x2 < other.x or
                    self.y2 < other.y or
                    self.x >= other.x2 or
                    self.y >= other.y2)

    def contains(self, x, y):
        return ((self.x <= x < self.x2) and
                (self.y <= y < self.y2))


# EOF #
