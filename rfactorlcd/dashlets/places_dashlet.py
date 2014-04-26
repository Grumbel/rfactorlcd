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


class PlacesDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(PlacesDashlet, self).__init__(*args)

        self.group = canvas.Group()
        self.gfx_track = self.group.add_rectangle()
        self.gfx_vehicles = []
        self.lap_dist = 1.0

    def update_state(self, state):
        # create new graphics, if number of vehicles changed
        if len(self.gfx_vehicles) != len(state.vehicles):
            self.group = canvas.Group()
            self.gfx_track = self.group.add_rectangle(fill_color=self.lcd_style.shadow_color,
                                                      stroke_color=None)
            self.gfx_vehicles = []
            for veh in state.vehicles:
                self.gfx_vehicles.append((self.group.add_rectangle(anchor=canvas.Anchor.CENTER, stroke_color=(0, 0, 0)),
                                          self.group.add_text(anchor=canvas.Anchor.S, baseline=canvas.Baseline.MIDDLE,
                                                              fill_color=(0, 0, 0))))

        self.gfx_track.x = 0
        self.gfx_track.y = self.h/2 - 2
        self.gfx_track.w = self.w
        self.gfx_track.h = 4

        # update graphics
        for i, veh in enumerate(state.vehicles):
            p = veh.lap_dist / state.lap_dist

            rect, text = self.gfx_vehicles[i]
            text.x = rect.x = p * self.w
            text.y = rect.y = self.h / 2
            rect.w = self.h/2
            rect.h = self.h/2

            text.font_size = self.h / 2.5
            text.text = str(veh.place)

            if veh.is_player:
                rect.style.fill_color = (0, 1.0, 0)
            elif veh.place == 1:
                rect.style.fill_color = (1.0, 1.0, 1.0)
            else:
                rect.style.fill_color = self.lcd_style.highlight_color

        self.queue_draw()

    def draw(self, cr):
        self.group.render(cr)


# EOF #
