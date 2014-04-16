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


import ConfigParser

import rfactorlcd


class Workspace(object):

    def __init__(self):
        self.dashlets = []
        self.lcd_style = None

    def clear(self):
        self.dashlets = []

    def find_dashlet_at(self, x, y):
        for dashlet in reversed(self.dashlets):
            if dashlet.x <= x < dashlet.x2 and \
               dashlet.y <= y < dashlet.y2:
                return dashlet
        return None

    def find_dashlets(self, x, y, w, h):
        return [dashlet for dashlet in self.dashlets if
                dashlet.x >= x and dashlet.y >= y and
                dashlet.x2 < x+w and dashlet.y2 >= y+h]

    def remove_dashlet(self, dashlet):
        self.dashlets.remove(dashlet)

    def raise_dashlet(self, dashlet):
        idx = self.dashlets.index(dashlet)
        for i in range(idx + 1, len(self.dashlets)):
            self.dashlets[i], self.dashlets[i-1] = self.dashlets[i-1], self.dashlets[i]
            if self.dashlets[i-1].overlaps(self.dashlets[i]):
                break

    def lower_dashlet(self, dashlet):
        idx = self.dashlets.index(dashlet)
        for i in range(idx - 1, -1, -1):
            self.dashlets[i], self.dashlets[i+1] = self.dashlets[i+1], self.dashlets[i]
            if self.dashlets[i+1].overlaps(self.dashlets[i]):
                break

    def draw(self, cr):
        for dashlet in self.dashlets:
            cr.save()
            cr.translate(dashlet.x, dashlet.y)
            dashlet.draw(cr)
            cr.restore()

    def update_state(self, widget, state):
        for dashlet in self.dashlets:
            dashlet.update_state(state)

            if dashlet.needs_redraw:
                widget.queue_draw_area(int(dashlet.x), int(dashlet.y),
                                       int(dashlet.w), int(dashlet.h))

    def set_lcd_style(self, lcd_style):
        self.lcd_style = lcd_style
        for dashlet in self.dashlets:
            dashlet.lcd_style = self.lcd_style

    def save(self, filename):
        print "saving workspace to %s" % filename
        config = ConfigParser.ConfigParser()

        for i, dashlet in enumerate(self.dashlets):
            sec = "Dashlet%d" % i
            config.add_section(sec)
            config.set(sec, 'type', dashlet.__class__.__name__)
            config.set(sec, 'x', dashlet.x)
            config.set(sec, 'y', dashlet.y)
            config.set(sec, 'w', dashlet.w)
            config.set(sec, 'h', dashlet.h)

        with open(filename, 'wb') as fout:
            config.write(fout)

    def load(self, filename):
        dashlet_classes = rfactorlcd.get_dashlets()
        print "loading workspace from %s" % filename
        dashlets = []
        try:
            config = ConfigParser.ConfigParser()

            with open(filename, 'r') as fin:
                config.readfp(fin)

                print config.sections()
                for section in config.sections():
                    print "loading %s" % section
                    try:
                        dashlet_type = config.get(section, "type")
                        print "TYPE: ", dashlet_type
                        dashlet_class = dashlet_classes[dashlet_type]
                        print dashlet_classes

                        if not issubclass(dashlet_class, rfactorlcd.Dashlet):
                            raise Exception("illegal class: %s" % dashlet_type)
                        else:
                            dashlet = dashlet_class(self, self.lcd_style)
                            dashlet.set_geometry(config.getfloat(section, "x"),
                                                 config.getfloat(section, "y"),
                                                 config.getfloat(section, "w"),
                                                 config.getfloat(section, "h"))
                            dashlets.append(dashlet)
                    except Exception as err:
                        print "ERROR: %s" % err
                        raise

            # load successful
            self.dashlets = dashlets

        except Exception as e:
            print "error while loading: %s" % e

    def load_default(self):
        self.load("default.rflcd")


# EOF #
