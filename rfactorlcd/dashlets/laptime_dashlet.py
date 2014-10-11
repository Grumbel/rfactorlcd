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
    """
    Race Mode:

    current (last lap time is held for 15sec)
    ahead
    behind
    best lap: time
              driver

    Practice/Hotlap Mode:

    current
    sector N: time
    self split ...
    best split: ...
                driver
    """
    def __init__(self, *args):
        super(LaptimeDashlet, self).__init__(*args)
        self.laptime = "0:00"

        self.group = canvas.Group()

        self.text_items = []

        def make_text(text):
            left = self.group.add_text(text=text,
                                       baseline=canvas.Baseline.TOP,
                                       anchor=canvas.Anchor.SE)
            right = self.group.add_text(text="{time}",
                                        baseline=canvas.Baseline.TOP,
                                        anchor=canvas.Anchor.SE)
            self.text_items.append((left, right))
            return left, right

        self.gfx_current_label, self.gfx_current_time = make_text("Current:")
        self.gfx_behind_label, self.gfx_behind_time = make_text("Behind:")
        self.gfx_ahead_label, self.gfx_ahead_time = make_text("Ahead:")
        self.gfx_best_label, self.gfx_best_time = make_text("Best:")
        self.gfx_best_driver_, self.gfx_best_driver = make_text("")

        self.reshape(self.x, self.y, self.w, self.h)

    def reshape(self, x, y, w, h):
        font_size = h / 5.0
        t_y = 0
        for left, right in self.text_items:
            left.font_size = font_size
            right.font_size = font_size
            left.y = right.y = t_y
            left.x = self.w / 2.0
            right.x = self.w / 2.0 + 6.0 * font_size
            t_y += font_size

    def update_state(self, state):
        if state.player is not None:
            current = state.current_e_t - state.player.lap_start_et
            if current < 15.0:
                current = state.player.last_lap_time
            self.gfx_current_time.text = "  %s" % format_time(current)

            behind_driver, behind_time = self.get_behind(state)
            self.gfx_behind_label.text = "%s:" % behind_driver
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
