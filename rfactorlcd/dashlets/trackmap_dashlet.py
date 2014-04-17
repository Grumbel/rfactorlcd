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


class TrackmapDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(TrackmapDashlet, self).__init__(*args)

        self.vehicles = []
        self.lap_dist = 1.0

    def update_state(self, state):
        self.vehicles = state.vehicles
        self.lap_dist = state.lap_dist
        self.queue_draw()

    def draw(self, cr):
        # need to add vehicle coordinates to the protocol
        pass

# EOF #
