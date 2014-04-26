# -*- coding: utf-8 -*-
#
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
import rfactorlcd.canvas as canvas


def celsius(kelvin):
    return kelvin - 273.15


def wear_color(v):
    return (max(0.0, min(1.0, v * -2.0 + 2.0)),
            max(0.0, min(1.0, v * 2.0)),
            0)


class CarDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(CarDashlet, self).__init__(*args)
        self.dent_severity = [0, 0, 0, 0, 0, 0, 0, 0]
        self.detached = False
        self.overheating = False
        self.wheels = None

        car_w = self.car_w = 150
        car_h = self.car_h = 300

        wheel_w = self.wheel_w = 60
        wheel_h = self.wheel_h = 80

        self.group = canvas.Group()

        self.gfx_dent = [
            # front
            self.group.add_rectangle(30, -20, car_w - 60, 20,
                                     stroke_color=(0, 0, 0),
                                     fill_color=self.dent_color(0)),
            # front/left
            self.group.add_rounded_rectangle(-20, -20, 60, 80,
                                             (32, 0, 0, 0),
                                             stroke_color=(0, 0, 0),
                                             fill_color=self.dent_color(1)),
            # left side
            self.group.add_rectangle(-20, 60, 20, car_h - 120,
                                     stroke_color=(0, 0, 0),
                                     fill_color=self.dent_color(2)),
            # back/left
            self.group.add_rounded_rectangle(-20, car_h-60, 60, 80,
                                             (0, 0, 0, 32),
                                             stroke_color=(0, 0, 0),
                                             fill_color=self.dent_color(3)),
            # back
            self.group.add_rectangle(30, car_h, car_w - 60, 20,
                                     stroke_color=(0, 0, 0),
                                     fill_color=self.dent_color(4)),
            # back/right
            self.group.add_rounded_rectangle(car_w-40, car_h-60, 60, 80,
                                             (0, 0, 32, 0),
                                             stroke_color=(0, 0, 0),
                                             fill_color=self.dent_color(5)),
            # right side
            self.group.add_rectangle(car_w, 60, 20, car_h-120,
                                     stroke_color=(0, 0, 0),
                                     fill_color=self.dent_color(6)),
            # front/right
            self.group.add_rounded_rectangle(car_w-40, -20, 60, 80,
                                             (0, 32, 0, 0),
                                             stroke_color=(0, 0, 0),
                                             fill_color=self.dent_color(7)),
        ]

        # car body
        self.gfx_body = self.group.add_rounded_rectangle(0, 0, car_w, car_h, (32, 32, 32, 32),
                                                         line_width=3.0,
                                                         stroke_color=(0, 0, 0),
                                                         fill_color=self.lcd_style.shadow_color)

        def make_wheel(root, wheel):
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

            group = root.add_group()

            parts = []
            for i in range(0, 3):
                offset = -8 if wheel in (0, 2) else 8
                parts.append((group.add_rounded_rectangle(w_x + i*wheel_w/3 + offset, w_y,
                                                          wheel_w/3, wheel_h,
                                                          rounding[i],
                                                          stroke_color=None,
                                                          fill_color=(1, 1, 1)),

                              group.add_text(w_x + wheel_w/2 + offset*1.5 + (i - 1) * 32,
                                             w_y - (15 if wheel in (0, 1) else -wheel_h - 25),
                                             "Temp",
                                             anchor=canvas.Anchor.S,
                                             font_size=16,
                                             fill_color=self.lcd_style.foreground_color)))

                flat = group.add_rounded_rectangle(w_x + offset, w_y,
                                                   wheel_w, wheel_h,
                                                   (12.0, 12.0, 12.0, 12.0),
                                                   stroke_color=(0.0, 1.0, 1.0),
                                                   line_width=8.0)
                flat.visible = False

            status = group.add_text(w_x + wheel_w/2 + (-85 if wheel in (0, 2) else 85),
                                    w_y + wheel_h/2 - 8,
                                    "-#-",
                                    anchor=canvas.Anchor.S,
                                    font_size=14,
                                    fill_color=self.lcd_style.foreground_color)
            group.add_text(w_x + wheel_w/2 + (-85 if wheel in (0, 2) else 85),
                           w_y + wheel_h/2 + 8,
                           "kPa",
                           anchor=canvas.Anchor.S,
                           font_size=14,
                           fill_color=self.lcd_style.foreground_color)

            group.add_rectangle(w_x + wheel_w/2 + (-55 if wheel in (0, 2) else 55) - 8,
                                w_y + wheel_h,
                                16, wheel_h,
                                anchor=canvas.Anchor.SW,
                                stroke_color=self.lcd_style.shadow_color,
                                fill_color=None)
            wear = group.add_rectangle(w_x + wheel_w/2 + (-55 if wheel in (0, 2) else 55) - 8,
                                       w_y + wheel_h,
                                       16, wheel_h,
                                       anchor=canvas.Anchor.SW,
                                       stroke_color=None,
                                       fill_color=(1, 0, 0))

            brake = group.add_text(w_x + wheel_w/2,
                                   w_y + wheel_h/2 + 8 + (60 if wheel in (0, 1) else -60),
                                   "99°",
                                   anchor=canvas.Anchor.S,
                                   font_size=16,
                                   fill_color=self.lcd_style.foreground_color)

            return (parts, flat, wear, brake, status)

        self.gfx_wheels = [make_wheel(self.group, 0),
                           make_wheel(self.group, 1),
                           make_wheel(self.group, 2),
                           make_wheel(self.group, 3)]

        self.gfx_engine = self.group.add_rectangle(car_w/2 - 30, 30, 60, 60,
                                                   line_width=3.0,
                                                   stroke_color=(0, 0, 0))

        self.group.add_text(-100, car_h/2 - 12,
                            "Water",
                            anchor=canvas.Anchor.S,
                            font_size=16)
        self.gfx_water = self.group.add_text(-100,
                                             car_h/2 + 8,
                                             "Temp",
                                             anchor=canvas.Anchor.S,
                                             font_size=16)

        self.group.add_text(car_w + 100, car_h/2 - 12,
                            "Oil",
                            anchor=canvas.Anchor.S,
                            font_size=16)
        self.gfx_oil = self.group.add_text(car_w + 100,
                                           car_h/2 + 8,
                                           "Temp",
                                           anchor=canvas.Anchor.S,
                                           font_size=16)

        self.group.add_rectangle(car_w/2, car_h - 80 + 4, 80, 60,
                                 anchor=canvas.Anchor.CENTER,
                                 stroke_color=None,
                                 fill_color=(0, 0, 0))
        self.group.add_text(car_w/2, car_h - 80,
                            "Fuel",
                            anchor=canvas.Anchor.S,
                            font_size=16)
        self.gfx_fuel = self.group.add_text(car_w/2, car_h - 62,
                                            "0L",
                                            anchor=canvas.Anchor.S,
                                            font_size=16)

    def reshape(self, x, y, w, h):
        scale = min(w, h) / 400.0
        self.group.translate = (self.w/2 - self.car_w/2 * scale,
                                self.h/2 - self.car_h/2 * scale)
        self.group.scale = (scale, scale)

    def update_state(self, state):
        self.dent_severity = state.dent_severity
        self.wheels = state.wheels
        self.overheating = state.overheating
        self.detached = state.detached
        self.queue_draw()

        for i, item in enumerate(self.gfx_dent):
            item.style.fill_color = self.dent_color(i)

        for i, (parts, flat, wear, brake, status) in enumerate(self.gfx_wheels):
            flat.visible = self.wheels[i].flat
            for j, (wheel_section, temp) in enumerate(parts):
                temp.text = "%3.0f" % celsius(self.wheels[i].temperature[j])
                wheel_section.style.fill_color = self.wheel_color(i, j)

            status.text = "%3.0f" % self.wheels[i].pressure
            wear.h = self.wheel_h * self.wheels[i].wear
            wear.style.fill_color = wear_color(self.wheels[i].wear)

            brake.text = "%3.0f°" % celsius(self.wheels[i].brake_temp)

        if self.overheating:
            self.gfx_engine.style.fill_color = (1, 0, 0)
        else:
            self.gfx_engine.style.fill_color = (0, 1, 0)

        if self.detached:
            self.gfx_body.style.fill_color = (1, 0, 0)
        else:
            self.gfx_body.style.fill_color = (0.5, 0.5, 0.5)

        self.gfx_oil.text = "%3.0f°" % state.oil_temp
        self.gfx_water.text = "%3.0f°" % state.water_temp
        self.gfx_fuel.text = "%3.1fL" % state.fuel

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
        if self.wheels[wheel].detached:
            return (0, 0, 0)
        else:
            temp = celsius(self.wheels[wheel].temperature[side])
            blue = 1.0 - min(max(0.0, float(temp - 70) / (120 - 70)), 1.0)
            red = min(max(0.0, float(temp - 30) / (70 - 30)), 1.0)
            green = min(max(0.0, float(temp - 100) / (150 - 100)), 1.0)
            return (red, green, blue)

    def draw(self, cr):
        self.group.render(cr)


# EOF #
