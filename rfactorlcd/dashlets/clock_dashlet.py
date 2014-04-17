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
import cairo


def format_time(v):
    if v == 0 or v == -1.0:
        return "--:--:---"
    minutes = int(v / 60)
    v -= minutes * 60
    seconds = int(v)
    v -= seconds
    mili = int(v * 1000)
    return "%2d:%02d:%03d" % (minutes, seconds, mili)


class ClockDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(ClockDashlet, self).__init__(*args)       
        self.time = 0.0
        
    def update_state(self, state):
        self.time = state.current_e_t

    def draw(self, cr):
        cr.move_to(0, self.h)
        cr.set_font_size(self.h)
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.show_text(format_time(self.time))
        

# EOF #
