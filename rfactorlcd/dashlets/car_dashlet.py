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


class CarDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(CarDashlet, self).__init__(*args)

    def set_geometry(self, x, y, w, h):
        super(CarDashlet, self).set_geometry(x, y, w, h)

    def update_state(self, state):
        pass  # self.queue_draw()

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
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(30, -20, car_w - 60, 20)
        cr.fill()

        # back
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(30, car_h, car_w - 60, 20)
        cr.fill()

        # left side
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(-20, 40, 20, car_h - 80)
        cr.fill()

        # right side
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(car_w, 40, 20, car_h - 80)
        cr.fill()

        # front/left
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(-20, -20, 60, 80)
        cr.fill()

        # front/right
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(car_w-40, -20, 60, 80)
        cr.fill()

        # back/left
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(-20, car_h-60, 60, 80)
        cr.fill()

        # back/right
        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.rectangle(car_w-40, car_h-60, 60, 80)
        cr.fill()

        # draw car body
        cr.set_source_rgb(*self.lcd_style.shadow_color)
        cr.rectangle(0, 0, car_w, car_h)
        cr.fill()

        # draw wheels
        for w_y in [0, car_h - wheel_h]:
            for w_x in [-wheel_w * 1.3, car_w + wheel_w * 0.3]:
                for i in range(1, 4):
                    cr.set_source_rgb(*self.lcd_style.foreground_color)
                    cr.rectangle(w_x, w_y,
                                 i*wheel_w/3, wheel_h)
                    cr.fill()

        cr.restore()

# EOF #
