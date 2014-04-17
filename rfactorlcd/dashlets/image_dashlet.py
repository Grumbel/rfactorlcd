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


class ImageDashlet(rfactorlcd.Dashlet):

    def __init__(self, *args):
        super(ImageDashlet, self).__init__(*args)
        self.image = cairo.ImageSurface.create_from_png("logo.png")

    def update_state(self, state):
        pass

    def draw(self, cr):
        cr.set_source_surface(self.image)
        cr.paint()


# EOF #
