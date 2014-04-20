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
import rfactorlcd.gfx as gfx


class Alignment:
    CENTER = 0
    LEFT = 1
    RIGHT = 2


class Anchor:
    CENTER = 0

    W = 1 << 0
    E = 1 << 1

    N = 1 << 2
    S = 1 << 3

    NW = N | W
    NE = N | E

    SW = S | W
    SE = S | E


class Style(object):

    def __init__(self):
        self.line_width = 1
        self.fill_color = None
        self.stroke_color = (1, 1, 1)

    def merge(self, style):
        self.line_width = style.get('line_width', self.line_width)
        self.fill_color = style.get('fill_color', self.fill_color)
        self.stroke_color = style.get('stroke_color', self.stroke_color)

    def render_path(self, cr):
        cr.set_line_width(self.line_width)

        if self.fill_color is not None:
            cr.set_source_rgb(*self.fill_color)
            if self.stroke_color is not None:
                cr.fill_preserve()
            else:
                cr.fill()

        if self.stroke_color is not None:
            cr.set_source_rgb(*self.stroke_color)
            cr.stroke()


class Item(object):

    def __init__(self, **style):
        self.invalidated = True
        self.visible = True
        self.recalc_bounds()
        self.style = Style()
        self.style.merge(style)

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
        if self.visible:
            self._render(cr)

    def _render(self, cr):
        raise NotImplementedError()


class Group(Item):

    def __init__(self, **style):
        super(Group, self).__init__(**style)
        self.children = []
        self.translate = None
        self.scale = None

    def add_group(self):
        child = Group()
        self.add_child(child)
        return child

    def add_child(self, child):
        self.children.append(child)

    def add_text(self, x, y, text, anchor=Anchor.NW, font_size=None, **style):
        child = Text(x, y, text, anchor, font_size, **style)
        self.add_child(child)
        return child

    def add_rectangle(self, x, y, w, h, **style):
        child = Rectangle(x, y, w, h, **style)
        self.add_child(child)
        return child

    def add_rounded_rectangle(self, x, y, w, h, radius, **style):
        child = RoundedRectangle(x, y, w, h, radius, **style)
        self.add_child(child)
        return child

    def add_circle(self, x, y, r, **style):
        self.add_arc(x, y, r)

    def add_arc(self, x, y, r, start=0, end=2*math.pi, **style):
        pass

    def _render(self, cr):
        cr.save()

        if self.translate is not None:
            cr.translate(*self.translate)

        if self.scale is not None:
            cr.scale(*self.scale)

        for child in self.children:
            child.render(cr)
        cr.restore()

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

    def _render(self, cr):
        self.make_path()
        self.style.render_path(cr)


class Rectangle(Item):

    def __init__(self, x, y, w, h, **style):
        super(Rectangle, self).__init__(**style)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def _render(self, cr):
        cr.rectangle(self.x, self.y, self.w, self.h)
        self.style.render_path(cr)


class RoundedRectangle(Item):

    def __init__(self, x, y, w, h, radius, **style):
        super(RoundedRectangle, self).__init__(**style)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.radius = radius

    def _render(self, cr):
        gfx.rounded_rectangle(cr, self.x, self.y, self.w, self.h, self.radius)
        self.style.render_path(cr)


class Text(Item):

    def __init__(self, x, y, text,  anchor=Anchor.NW, font_size=16, **style):
        super(Text, self).__init__(**style)
        self._text = text
        self.x = x
        self.y = y
        self.anchor = anchor
        self.font_size = font_size

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def _render(self, cr):
        cr.set_font_size(self.font_size)

        x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents(self._text)

        x = self.x
        y = self.y

        self.w = width
        self.h = height

        if self.anchor & Anchor.W:
            x += 0
        elif self.anchor & Anchor.E:
            x -= self.w
        else:
            x -= self.w/2

        if self.anchor & Anchor.N:
            y += 0
        elif self.anchor & Anchor.S:
            y -= self.h
        else:
            y -= self.h/2

        if self.style.fill_color is None:
            cr.set_source_rgb(1, 1, 1)
        else:
            cr.set_source_rgb(*self.style.fill_color)
        cr.move_to(x - x_bearing,
                   y - y_bearing)
        cr.show_text(self._text)


# EOF #
