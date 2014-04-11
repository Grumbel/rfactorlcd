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


class Dashlet(object):

    def __init__(self, parent, lcd_style):
        self.parent = parent
        self.lcd_style = lcd_style
        self.x = 0
        self.y = 0
        self.w = 256
        self.h = 256
        self.needs_redraw = True

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    @property
    def x2(self):
        return self.x + self.w

    @property
    def y2(self):
        return self.y + self.h

    def queue_draw(self):
        self.needs_redraw = True

    def set_geometry(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.needs_redraw = True

    def update_state(self, state):
        raise NotImplementedError()

    def draw(self, cr):
        raise NotImplementedError()


# EOF #
