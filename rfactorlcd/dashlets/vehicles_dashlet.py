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


def parse_time(v):
    if v == 0 or v == -1.0:
        return "--:--:---"
    minutes = int(v / 60)
    v -= minutes * 60
    seconds = int(v)
    v -= seconds
    mili = int(v * 1000)
    return "%2d:%02d:%03d" % (minutes, seconds, mili)


class VehiclesDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(VehiclesDashlet, self).__init__(*args)
        self.vehicles = []
        self.font_size = self.h / 32.0
        self.column_width = [5, 22, 10, 10, 10, 10, 10]
        self.column_offset = self.column_width

    def reshape(self, x, y, w, h):
        self.font_size = h / 32.0

        total_w = 0
        self.column_offset = []
        for w in self.column_width:
            self.column_offset.append(total_w)
            total_w += w

        for i in range(0, len(self.column_offset)):
            self.column_offset[i] = self.column_offset[i] / float(total_w) * self.w

    def update_state(self, state):
        self.vehicles = state.vehicles
        self.queue_draw()

    def draw(self, cr):
        if len(self.vehicles) > 0:
            cr.set_font_size(self.font_size)

            cr.set_source_rgb(*self.lcd_style.highlight_color)
            self.draw_row(cr, 0, 1, "Name")
            self.draw_row(cr, 0, 2, " Best")
            self.draw_row(cr, 0, 3, " Last")
            self.draw_row(cr, 0, 4, " Sector1")
            self.draw_row(cr, 0, 5, " Sector2")
            self.draw_row(cr, 0, 6, " Sector3")

            for veh in sorted(self.vehicles, lambda a, b: cmp(a.place, b.place)):
                if veh.is_player:
                    cr.set_source_rgb(*self.lcd_style.highlight_color)
                else:
                    cr.set_source_rgb(*self.lcd_style.foreground_color)

                row = veh.place
                self.draw_row(cr, row, 0, "%2d" % veh.place)
                self.draw_row(cr, row, 1, veh.driver_name)
                self.draw_row(cr, row, 2, parse_time(veh.best_lap_time))
                self.draw_row(cr, row, 3, parse_time(veh.last_lap_time))
                self.draw_row(cr, row, 4, parse_time(veh.last_sector1))
                self.draw_row(cr, row, 5, parse_time(veh.last_sector2 - veh.last_sector1))
                self.draw_row(cr, row, 6, parse_time(veh.last_lap_time - veh.last_sector2))

    def draw_row(self, cr, row, col, text):
            cr.move_to(self.column_offset[col], (row + 1.2) * self.font_size * 1.2)

            cr.show_text(text)


# EOF #
