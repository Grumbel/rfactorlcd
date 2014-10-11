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


import gtk

import rfactorlcd


class DragMode:
    Move = 0
    ResizeLeft = 1 << 0
    ResizeRight = 1 << 1
    ResizeTop = 1 << 2
    ResizeBottom = 1 << 3


class ControlPoint:

    def __init__(self, x, y, w, h, mode):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mode = mode

    def render(self, cr):
        cr.rectangle(self.x - self.w/2,
                     self.y - self.h/2,
                     self.w, self.h)

        cr.set_line_width(4.0)
        cr.set_source_rgb(1, 0, 0)
        cr.fill_preserve()

        cr.set_source_rgb(0.75, 0, 0)
        cr.set_line_width(1.0)
        cr.stroke()

    def contains(self, x, y):
        return (abs(self.x - x) <= self.w and
                abs(self.y - y) <= self.h)


class DashletSelection(object):

    def __init__(self, style, workspace):
        self.lcd_style = style
        self.workspace = workspace
        self.dashlets = []
        self.dashlet_origins = []
        self.drag_start = None
        self.drag_mode = None
        self.control_points = []

    def on_button_press(self, widget, event):
        # print "press", event.x, event.y, event.button
        self.dashlet_selection.on_button_press(self, widget, event)

    def is_active(self):
        return bool(self.dashlet)

    def add(self, dashlet):
        self.dashlets.append(dashlet)
        self.update()

    def remove(self, dashlet):
        self.dashlets.remove(dashlet)
        self.update()

    def set(self, dashlet):
        self.dashlets = [dashlet]
        self.update()

    def clear(self):
        self.dashlets = []
        self.update()

    def update(self):
        bb = self.bounding_box = self.calc_bounding_box()

        self.control_points = [
            ControlPoint(bb.x1 - 8, bb.y1 - 8, 16, 16, DragMode.ResizeLeft | DragMode.ResizeTop),
            ControlPoint(bb.x1 - 8, bb.cy, 16, 16, DragMode.ResizeLeft),
            ControlPoint(bb.x1 - 8, bb.y2 + 8, 16, 16, DragMode.ResizeLeft | DragMode.ResizeBottom),

            ControlPoint(bb.cx, bb.y1 - 8, 16, 16, DragMode.ResizeTop),
            ControlPoint(bb.cx, bb.y2 + 8, 16, 16, DragMode.ResizeBottom),

            ControlPoint(bb.x2 + 8, bb.y1 - 8, 16, 16, DragMode.ResizeRight | DragMode.ResizeTop),
            ControlPoint(bb.x2 + 8, bb.cy, 16, 16, DragMode.ResizeRight),
            ControlPoint(bb.x2 + 8, bb.y2 + 8, 16, 16, DragMode.ResizeRight | DragMode.ResizeBottom),
        ]

    def contains(self, dashlet):
        return dashlet in self.dashlets

    def is_empty(self):
        return self.dashlets == []

    def calc_bounding_box(self):
        if self.dashlets == []:
            return None

        else:
            x1 = self.dashlets[0].x
            y1 = self.dashlets[0].y
            x2 = self.dashlets[0].x2
            y2 = self.dashlets[0].y2

            for dashlet in self.dashlets[1:]:
                x1 = min(dashlet.x, x1)
                y1 = min(dashlet.y, y1)

                x2 = max(dashlet.x2, x2)
                y2 = max(dashlet.y2, y2)

            return rfactorlcd.Rect(x1, y1, x2 - x1, y2 - y1)

    def find_control_point(self, x, y):
        for cp in self.control_points:
            if cp.contains(x, y):
                return cp
        return None

    def on_button_press(self, event):
        control_point = self.find_control_point(event.x, event.y)
        if control_point is not None:
            self.control_points = []
            self.drag_start = (event.x, event.y)
            self.drag_mode = control_point.mode
            self.dashlet_origins = [(dashlet.x, dashlet.y, dashlet.w, dashlet.h)
                                    for dashlet in self.dashlets]
        else:
            dashlet = self.workspace.find_dashlet_at(event.x, event.y)
            if dashlet is None:
                self.clear()
            else:
                if event.state & gtk.gdk.SHIFT_MASK:
                    if self.contains(dashlet):
                        self.remove(dashlet)
                    else:
                        self.add(dashlet)
                else:
                    if not self.contains(dashlet):
                        self.set(dashlet)

                if not self.is_empty():
                    self.control_points = []
                    self.drag_start = (event.x, event.y)
                    self.drag_mode = DragMode.Move
                    self.dashlet_origins = [(d.x, d.y, d.w, d.h)
                                            for d in self.dashlets]

    def on_button_release(self, event):
        self.drag_start = None
        self.drag_mode = None
        self.update()

    def on_move(self, event):
        if self.drag_start is not None:
            x = event.x - self.drag_start[0]
            y = event.y - self.drag_start[1]

            for i, dashlet in enumerate(self.dashlets):
                origins = self.dashlet_origins[i]

                if self.drag_mode == DragMode.Move:
                    dashlet.set_geometry(origins[0] + x, origins[1] + y)
                else:
                    rect = rfactorlcd.Rect.copy(self.bounding_box)

                    if self.drag_mode & DragMode.ResizeLeft:
                        rect.x += x
                        rect.w -= x

                    if self.drag_mode & DragMode.ResizeRight:
                        rect.w += x

                    if self.drag_mode & DragMode.ResizeTop:
                        rect.y += y
                        rect.h -= y

                    if self.drag_mode & DragMode.ResizeBottom:
                        rect.h += y

                    scale_x = rect.w / self.bounding_box.w
                    scale_y = rect.h / self.bounding_box.h

                    dashlet.set_geometry(x=rect.x + (origins[0] - self.bounding_box.x) * scale_x,
                                         y=rect.y + (origins[1] - self.bounding_box.y) * scale_y,
                                         w=origins[2] * scale_x,
                                         h=origins[3] * scale_y)

    def render(self, cr):
        if self.dashlets == []:
            return
        else:
            cr.set_line_width(2.0)
            cr.set_source_rgb(*self.lcd_style.select_color)
            for dashlet in self.dashlets:
                cr.rectangle(dashlet.x, dashlet.y,
                             dashlet.w, dashlet.h)
            cr.stroke()

            if self.control_points != []:
                cr.set_line_width(1.0)
                cr.set_dash([4.0, 4.0])
                cr.rectangle(self.bounding_box.x, self.bounding_box.y,
                             self.bounding_box.w, self.bounding_box.h)
                cr.stroke()
                cr.set_dash([])

                for cp in self.control_points:
                    cp.render(cr)


# EOF #
