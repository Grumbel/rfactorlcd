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


import math


def rounded_rectangle(cr, x, y, w, h, radius):

    if isinstance(radius, tuple):
        nw_r, ne_r, se_r, sw_r = radius
    else:
        nw_r = ne_r = se_r = sw_r = radius

    degrees = math.pi / 180.0

    cr.new_sub_path();
    if nw_r == 0:
        cr.move_to(x, y)
    else:
        cr.arc(x + nw_r, y + nw_r, nw_r, 180 * degrees, 270 * degrees);

    if ne_r == 0:
        cr.line_to(x + w, y)
    else:
        cr.arc(x + w - ne_r, y + ne_r, ne_r, -90 * degrees, 0 * degrees);

    if se_r == 0:
        cr.line_to(x + w, y + h)
    else:
        cr.arc(x + w - se_r, y + h - se_r, se_r, 0 * degrees, 90 * degrees);

    if sw_r == 0:
        cr.line_to(x, y + h)
    else:    
        cr.arc(x + sw_r, y + h - sw_r, sw_r, 90 * degrees, 180 * degrees);   
    cr.close_path();


# EOF #
