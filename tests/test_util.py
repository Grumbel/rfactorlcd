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


import unittest
import struct
import os

import rfactorlcd
from rfactorlcd.dashlets.gmeter_dashlet import GMeterDashlet


class UtilTestCase(unittest.TestCase):

    def test_dashlets_import(self):
        """Make sure that the plugin modules are not reloaded, to avoid
        getting incompatible types with the name names and super() failing as
        a result, see:

        http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/
        """

        a = rfactorlcd.dashlets["GMeterDashlet"]
        b = GMeterDashlet

        self.assertEqual(a, b)

        a_obj = a(None, None)
        b_obj = b(None, None)
        
        self.assertTrue(isinstance(a_obj, b))
        self.assertTrue(isinstance(b_obj, a))


if __name__ == '__main__':
    unittest.main()


# EOF #
