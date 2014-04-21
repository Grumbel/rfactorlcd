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


def find(lst, pred):
    for el in lst:
        if pred(el):
            return el
    return None


def format_time(v):
    if v == 0 or v == -1.0:
        return "--:--:---"
    minutes = int(v / 60)
    v -= minutes * 60
    seconds = int(v)
    v -= seconds
    mili = int(v * 1000)
    return "%1d:%02d:%03d" % (minutes, seconds, mili)


class LaptimeDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(LaptimeDashlet, self).__init__(*args)
        self.laptime = "0:00"

        self.group = canvas.Group()

        self.t_x = self.w/2.0 + 160
        self.t_y = 0
        def make_text(text):
            left = self.group.add_text(self.t_x - 8, self.t_y,
                                       text,
                                       font_size=38,
                                       anchor=canvas.Anchor.NE)
            right = self.group.add_text(self.t_x + 8 + 250, self.t_y,
                                        "{time}",
                                        font_size=38,
                                        anchor=canvas.Anchor.NE)
            self.t_y += 40
            return left, right

        self.gfx_current_label, self.gfx_current_time = make_text("Current:")
        self.gfx_behind_label, self.gfx_behind_time = make_text("Behind:")
        self.gfx_ahead_label, self.gfx_ahead_time = make_text("Ahead:")
        self.gfx_best_label, self.gfx_best_time = make_text("Best:")
        self.gfx_best_driver_, self.gfx_best_driver = make_text("")

        # current (last lap time is held for 15sec)
        # ahead
        # behind
        # best lap: time
        #           driver

        # current
        # sector N: time
        # self split ...
        # best split: ...
        #             driver

    def reshape(self, x, y, w, h):
        pass

    def update_state(self, state):
        if state.player is not None:
            current = state.current_e_t - state.player.lap_start_et
            if current < 15.0:
                current = state.player.last_lap_time
            self.gfx_current_time.text = "  %s" % format_time(current)

            behind_driver, behind_time = self.get_behind(state)
            self.gfx_behind_label.text = behind_driver
            self.gfx_behind_time.text = "-%s" % format_time(behind_time)

            ahead_driver, ahead_time = self.get_ahead(state)
            if ahead_time == 0.0:
                self.gfx_ahead_time.text = "%s" % format_time(ahead_time)
                self.gfx_ahead_label.text = "%s:" % ahead_driver
            else:
                self.gfx_ahead_time.text = "+%s" % format_time(ahead_time)
                self.gfx_ahead_label.text = "%s:" % ahead_driver

            self.gfx_best_time.text = format_time(state.best_lap_time)
            self.gfx_best_driver.text = state.best_lap_driver

    def get_behind(self, state):
        place = state.player.place - 1
        veh = find(state.vehicles, lambda v: v.place == place)
        if veh is not None:
            return veh.driver_name, state.player.time_behind_next
        else:
            return "-", 0.0

    def get_ahead(self, state):
        place_behind = state.player.place + 1
        veh = find(state.vehicles, lambda v: v.place == place_behind)
        if veh is not None:
            return veh.driver_name, veh.time_behind_next
        else:
            return "-", 0.0

    def draw(self, cr):
        self.group.render(cr)


# EOF #
