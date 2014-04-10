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


import math


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


class SpeedDashlet(Dashlet):

    def __init__(self, *args):
        super(SpeedDashlet, self).__init__(*args)
        self.speed = 0

    def update_state(self, state):
        if self.speed != state.speed:
            self.speed = state.speed
            self.queue_draw()

    def draw(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(self.w/2, self.h/2)
        cr.set_font_size(180)
        cr.show_text("%3d" % self.speed)
        cr.set_font_size(90)
        cr.show_text("km/h")


class TempDashlet(Dashlet):

    def __init__(self, *args):
        super(TempDashlet, self).__init__(*args)
        self.oil_temp = 0
        self.water_temp = 0
        self.fuel = 0

    def update_state(self, state):
        if self.oil_temp != state.oil_temp or \
           self.water_temp != state.water_temp or \
           self.fuel != state.fuel:

            self.oil_temp = state.oil_temp
            self.water_temp = state.water_temp
            self.fuel = state.fuel

            self.queue_draw()

    def draw(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_font_size(60)

        cr.move_to(0, 0)
        cr.show_text("Oil:")
        cr.move_to(250, 0)
        cr.show_text("%5.1f" % self.oil_temp)

        cr.move_to(0, 80)
        cr.show_text("Water:")
        cr.move_to(250, 80)
        cr.show_text("%5.1f" % self.water_temp)

        cr.move_to(0, 160)
        cr.show_text("Fuel:")
        cr.move_to(250, 160)
        cr.show_text("%5.1f" % self.fuel)


class RPMDashlet(Dashlet):

    def __init__(self, *args):
        super(RPMDashlet, self).__init__(*args)

        self.inner_r = 250.0
        self.outer_r = 300.0

        self.rpm = 0
        self.max_rpm = 5000
        self.gear = 0

    def set_geometry(self, x, y, w, h):
        super(RPMDashlet, self).set_geometry(x, y, w, h)

        max_radius = min(w, h) / 2

        self.inner_r = max_radius * 0.8
        self.outer_r = max_radius

    def update_state(self, state):
        if self.rpm != state.rpm or \
           self.max_rpm != state.max_rpm or \
           self.gear != state.gear:

            self.rpm = state.rpm
            self.max_rpm = state.max_rpm
            self.gear = state.gear

            self.queue_draw()

    def draw(self, cr):
        cr.save()
        cr.translate(self.w/2, self.h/2)
        cr.set_source_rgb(*self.lcd_style.foreground_color)

        # display the rpm/max_rpm
        cr.set_font_size(self.outer_r/6)
        cr.move_to(-self.outer_r/2, -self.outer_r/2)
        cr.show_text("%6d" % self.rpm)
        cr.move_to(-self.outer_r/2, -self.outer_r/3)
        cr.show_text("%6d" % self.max_rpm)

        # draw the background pattern
        cr.move_to(0, 0)
        start = 90
        end = 360
        for deg in range(start, end+1, 10):  # int((end - start) / int((max_rpm + 500)/1000))):
            rad = math.radians(deg)
            if False:
                x = math.sin(rad)
                y = math.cos(rad)

                cr.move_to(x * self.inner_r,
                           y * self.inner_r)
                cr.line_to(x * self.outer_r,
                           y * self.outer_r)
                cr.stroke()
            else:
                step_s = 0.08
                cr.arc_negative(0, 0, self.outer_r, rad + step_s, rad - step_s)
                cr.arc(0, 0, self.inner_r, rad - step_s, rad + step_s)
                cr.close_path()
                cr.set_source_rgb(*self.lcd_style.shadow_color)
                cr.fill()
        cr.save()

        # draw the needle
        if self.max_rpm != 0:
            rpm_p = self.rpm / self.max_rpm

            cr.rotate(math.radians(start + (end - start - 1) * (rpm_p)))
            cr.arc(0, 0, 20, math.pi/2, math.pi + math.pi/2)
            cr.line_to(self.outer_r * 1.05, -2)
            cr.line_to(self.outer_r * 1.05, 2)
            cr.close_path()

            cr.set_source_rgb(*self.lcd_style.highlight_color)
            cr.fill_preserve()

            cr.set_source_rgb(*self.lcd_style.highlight_dim_color)
            cr.stroke()
            cr.restore()

        cr.restore()

        self.draw_gear(cr)

    def draw_gear(self, cr):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(self.w/2 + self.outer_r * 0.25,
                   self.h/2 + self.outer_r * 0.9)
        cr.set_font_size(self.outer_r)
        if self.gear == 0:
            cr.show_text("N")
        elif self.gear == -1:
            cr.show_text("R")
        else:
            cr.show_text(str(self.gear))


# EOF #
