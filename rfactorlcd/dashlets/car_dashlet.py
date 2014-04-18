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


import rfactorlcd
import rfactorlcd.gfx as gfx


def celsius(kelvin):
    return kelvin - 273.15


class CarDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(CarDashlet, self).__init__(*args)
        self.dent_severity = [0, 0, 0, 0, 0, 0, 0, 0]
        self.wheels = None

    def reshape(self, x, y, w, h):
        pass

    def update_state(self, state):
        self.dent_severity = state.dent_severity
        self.wheels = state.wheels
        self.queue_draw()

    def dent_color(self, part):
        severity = self.dent_severity[part]

        if severity == 0:
            return self.lcd_style.shadow_color
        elif severity == 1:
            return (1, 1, 0)
        elif severity == 2:
            return (1, 0, 0)
        else:
            return (1, 1, 1)

    def wheel_color(self, wheel, side):
        temp = celsius(self.wheels[wheel].temperature[side])
        blue = 1.0 - min(max(0.0, float(temp - 70) / (120 - 70)), 1.0)
        red = min(max(0.0, float(temp - 30) / (70 - 30)), 1.0)
        return (red, 0, blue)

    def draw(self, cr):
        car_w = 150
        car_h = 300

        wheel_w = 60
        wheel_h = 80

        cr.save()
        cr.translate(self.w/2 - car_w/2,
                     self.h/2 - car_h/2)

        # draw dentable body parts

        # front
        cr.set_source_rgb(*self.dent_color(0))
        cr.rectangle(30, -20, car_w - 60, 20)
        cr.fill()

        # back
        cr.set_source_rgb(*self.dent_color(4))
        cr.rectangle(30, car_h, car_w - 60, 20)
        cr.fill()

        # left side
        cr.set_source_rgb(*self.dent_color(2))
        cr.rectangle(-20, 40, 20, car_h - 80)
        cr.fill()

        # right side
        cr.set_source_rgb(*self.dent_color(6))
        cr.rectangle(car_w, 40, 20, car_h - 80)
        cr.fill()

        # front/left
        cr.set_source_rgb(*self.dent_color(1))
        cr.rectangle(-20, -20, 60, 80)
        cr.fill()

        # front/right
        cr.set_source_rgb(*self.dent_color(7))
        cr.rectangle(car_w-40, -20, 60, 80)
        cr.fill()

        # back/left
        cr.set_source_rgb(*self.dent_color(3))
        cr.rectangle(-20, car_h-60, 60, 80)
        cr.fill()

        # back/right
        cr.set_source_rgb(*self.dent_color(5))
        cr.rectangle(car_w-40, car_h-60, 60, 80)
        cr.fill()

        # draw car body
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        gfx.rounded_rectangle(cr, 
                              0, 0, car_w, car_h,
                              (32, 32, 32, 32))
        cr.fill()

        # draw wheels
        if self.wheels:
            for wheel in range(0, 4):
                if wheel in (0, 1):
                    w_y = 0
                else:
                    w_y = car_h - wheel_h

                if wheel in (0, 2):
                    w_x = -wheel_w * 1.3
                else:
                    w_x = car_w + wheel_w * 0.3

                rounding = [(12.0, 0.0, 0.0, 12.0),
                            (0.0, 0.0, 0.0, 0.0),
                            (0.0, 12.0, 12.0, 0.0)]

                for i in range(0, 3):
                    cr.set_source_rgb(*self.wheel_color(wheel, i))
                    offset = -8 if wheel in (0, 2) else 8
                    gfx.rounded_rectangle(cr, 
                                          w_x + i*wheel_w/3 + offset, w_y,
                                          wheel_w/3, wheel_h,
                                          rounding[i])
                    cr.fill()

                    cr.set_font_size(12)
                    cr.set_source_rgb(*self.lcd_style.foreground_color)
                    cr.move_to(w_x + i * wheel_w/1.5, w_y - 10)
                    cr.show_text("%3.1f" % celsius(self.wheels[wheel].temperature[i]))

                force = self.wheels[wheel].lateral_force
                cr.set_source_rgb(*self.lcd_style.highlight_color)
                cr.rectangle(w_x + wheel_w/2,
                             w_y + wheel_h/2 - 10,
                             wheel_w * force/8000.0, 20)
                cr.fill()

                force = self.wheels[wheel].rotation
                cr.set_source_rgb(*self.lcd_style.highlight_color)
                cr.rectangle(w_x + wheel_w/2 - 10,
                             w_y + wheel_h/2,
                             20, wheel_h * force/150.0)
                cr.fill()

        cr.restore()

# EOF #
