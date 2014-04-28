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


import cairo


class Style:

    @staticmethod
    def white_on_black():
        style = Style()

        style.background_color = (1.0, 1.0, 1.0)
        style.shadow_color = (0.5, 0.5, 0.5)
        style.highlight_color = (1.0, 0, 0)
        style.highlight_dim_color = (0.5, 0, 0)
        style.foreground_color = (0, 0, 0)

        return style

    @staticmethod
    def black_on_white():
        style = Style()

        style.background_color = (0, 0, 0)
        style.shadow_color = (0.5, 0.5, 0.5)
        style.highlight_color = (1.0, 0, 0)
        style.highlight_dim_color = (0.5, 0, 0)
        style.foreground_color = (1.0, 1.0, 1.0)

        return style

    def __init__(self):
        self.font = "Droid Sans Mono"
        self.font_slant = cairo.FONT_SLANT_NORMAL
        self.font_weight = cairo.FONT_WEIGHT_NORMAL

        self.background_color = (1.0, 1.0, 1.0)
        self.shadow_color = (0.5, 0.5, 0.5)
        self.highlight_color = (1.0, 0, 0)
        self.highlight_dim_color = (0.5, 0, 0)
        self.foreground_color = (0, 0, 0)
        self.select_color = (0.25, 0.5, 1)


# EOF #
