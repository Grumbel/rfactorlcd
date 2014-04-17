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


class LapDashlet(rfactorlcd.Text2Dashlet):

    def __init__(self, *args):
        super(LapDashlet, self).__init__(*args)
        self.lap_number = 0
        self.max_laps = 0

    def update_state(self, state):
        if self.lap_number != state.lap_number or \
           self.max_laps != state.max_laps:

            self.lap_number = state.lap_number
            self.max_laps = state.max_laps

            self.left_item.text = "Lap:"
            self.right_item.text = "%2d/%d" % (self.lap_number+1, self.max_laps)


# EOF #
