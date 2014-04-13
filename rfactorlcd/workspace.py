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
                        dashlet_class = rfactorlcd.__getattribute__(dashlet_type)
                        if not issubclass(dashlet_class, rfactorlcd.Dashlet):
                            raise Exception("illegal class: %s" % dashlet_type)
                        else:
                            dashlet = dashlet_class(self, self.lcd_style)
                            dashlet.set_geometry(config.getfloat(section, "x"),
                                                 config.getfloat(section, "y"),
                                                 config.getfloat(section, "w"),
                                                 config.getfloat(section, "h"))
                            dashlets.append(dashlet)
                    except:
                        print "ERROR"
                        raise

            # load successful
            self.dashlets = dashlets

        except Exception as e:
            print "error while loading: %s" % e

    def load_default(self):
        rpm_dashlet = rfactorlcd.RPMDashlet(self, self.lcd_style)
        rpm_dashlet.set_geometry(100, 100, 300, 300)

        temp_dashlet = rfactorlcd.TempDashlet(self, self.lcd_style)
        temp_dashlet.set_geometry(700, 250, 450, 150)

        speed_dashlet = rfactorlcd.SpeedDashlet(self, self.lcd_style)
        speed_dashlet.set_geometry(580, 50, 400, 100)

        sector_dashlet = rfactorlcd.SectorDashlet(self, self.lcd_style)
        sector_dashlet.set_geometry(800, 550, 300, 300)

        laptime_dashlet = rfactorlcd.LaptimeDashlet(self, self.lcd_style)
        laptime_dashlet.set_geometry(50, 600, 800, 50)

        position_dashlet = rfactorlcd.PositionDashlet(self, self.lcd_style)
        position_dashlet.set_geometry(50, 750, 800, 50)

        shiftlights_dashlet = rfactorlcd.ShiftlightsDashlet(self, self.lcd_style)
        shiftlights_dashlet.set_geometry(0, 0, 1200, 80)

        car_dashlet = rfactorlcd.CarDashlet(self, self.lcd_style)
        car_dashlet.set_geometry(1200 - 400, 900 - 400, 400, 400)

        speedometer_dashlet = rfactorlcd.SpeedometerDashlet(self, self.lcd_style)
        speedometer_dashlet.set_geometry(100, 100, 400, 400)

        # rpm2_dashlet = rfactorlcd.RPM2Dashlet(self, self.lcd_style)
        # rpm2_dashlet.set_geometry(600, 400, 400, 300)

        self.dashlets = [
            speedometer_dashlet,
            rpm_dashlet,
            speed_dashlet,
            temp_dashlet,
            # sector_dashlet,
            laptime_dashlet,
            position_dashlet,
            shiftlights_dashlet,
            car_dashlet
        ]

# EOF #
