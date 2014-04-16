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


import types
import pkgutil
import sys

import rfactorlcd


dashlets = {}
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__, __name__ + "."):
    if module_name in sys.modules:
        modules = sys.modules[module_name]
    else:
        module = loader.find_module(module_name).load_module(module_name)

    for k, v in module.__dict__.items():
        if isinstance(v, types.TypeType) and \
           issubclass(v, rfactorlcd.Dashlet):
            if k in dashlets:
                raise RuntimeError("duplicate dashlet: %s" % k)
            else:
                dashlets[k] = v


# EOF #
