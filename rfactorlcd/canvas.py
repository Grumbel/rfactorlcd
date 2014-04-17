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


# import cairo
import math


class Alignment:
    LEFT = 1 << 0
    RIGHT = 1 << 1
    CENTER = LEFT | RIGHT

    TOP = 1 << 2
    BOTTOM = 1 << 3
    MIDDLE = TOP | BOTTOM


class Properties(object):

    def __init__(self):
        self.line_width = 1
        self.fill_color = None
        self.stroke_color = (1, 1, 1)

    def merge(self, style):
        self.line_width = style.get('line_width')
        self.fill_color = style.get('fill_color')
        self.stroke_color = style.get('stroke_color')


class Item(object):

    def __init__(self):
        self.invalidated = True
        self.recalc_bounds()

    def recalc_bounds(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def get_bounds(self, cr):
        return (self.x, self.y,
                self.w, self.h)

    def invalidate(self):
        self.invalidated = True

    def render(self, cr):
        self.invalidated = False


class Group(Item):

    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_text(self, x, y, text, alignment=Alignment.TOP | Alignment.LEFT, font_style=None, **style):
        child = Text(x, y, text, alignment, font_style, **style)
        self.add_child(child)
        return child

    def add_rectangle(self, x, y, w, h, **style):
        child = Rectangle(x, y, w, h, **style)
        self.add_child(child)
        return child

    def add_circle(self, x, y, r, **style):
        self.add_arc(x, y, r)

    def add_arc(self, x, y, r, start=0, end=2*math.pi, **style):
        pass

    def render(self, cr):
        for child in self.children:
            child.render(cr)


class Path(Item):

    def __init__(self, **style):
        super(Path, self).__init__(**style)
        self.points = []

    def clear(self):
        self.points = []

    def move_to(self, x, y):
        self.points.append(('M', (x, y)))

    def rel_move_to(self, x, y):
        self.points.append(('m', (x, y)))

    def line_to(self, x, y):
        self.points.append(('L', (x, y)))

    def rel_line_to(self, x, y):
        self.points.append(('m', (x, y)))

    def close_path(self):
        self.points.append(('Z'))

    def finish(self):
        pass

    def make_path(self, cr):
        """http://www.w3.org/TR/SVG11/paths.html#PathDataClosePathCommand"""

        cr.new_path()
        for cmd, params in self.points:
            if cmd == 'M':
                cr.move_to(*params)
            elif cmd == 'm':
                cr.rel_move_to(*params)
            elif cmd == 'L':
                cr.line_to(*params)
            elif cmd == 'l':
                cr.rel_line_to(*params)
            elif cmd == 'Z':
                cr.close_path()
            else:
                raise RuntimeError("unknown path command: '%s' - %s" % (cmd, params))

    def render(self, cr):
        self.make_path()

        cr.set_line_width(self.style.line_width)

        if self.style.fill_color is not None:
            self.style.apply_fill_color(cr)
            if self.style.stroke_color is not None:
                cr.fill_preserve()
            else:
                cr.fill()

        if self.style.stroke_color is not None:
            self.style.apply_stroke_color(cr)
            cr.stroke()


class Rectangle(Item):

    def __init__(self, x, y, w, h, **style):
        super(Rectangle, self).__init__(**style)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def render(self, cr):
        cr.rectangle(self.x, self.y, self.w, self.h)
        if self.style.stroke_color is not None:
            cr.set_source_rgb(self.style.stroke_color)
            cr.stroke()


class Text(Item):

    def __init__(self, x, y, text,  alignment = None, font_style = None, **style):
        self.text = text
        self.x = x
        self.y = y

    def set_text(self, text):
        self.text = text

    def render(self, cr):
        x = self.x
        y = self.y

        x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents(self.text)

        self.w = width
        self.h = height

        if self.alignment & (Alignment.LEFT | Alignment.RIGHT):
            x -= self.w / 2
        elif self.alignment & Alignment.RIGHT:
            x -= self.w

        if self.alignment & (Alignment.TOP | Alignment.BOTTOM):
            y -= self.h / 2
        elif self.alignment & Alignment.BOTTOM:
            y -= self.h

        cr.move_to(x, y)
        cr.show_text(self.text)
        pass


# EOF #
