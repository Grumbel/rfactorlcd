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


import argparse
import cairo
import gtk
import math
import socket
import threading
import glib
import datetime
import os

import rfactorlcd


# 17/17 position
# 1
# 0.615
# 0.000
# 0.000
# 39.197
# 0.000
# 0.000
# 2:27.362 some lap time
# 0.0 speed
# 0 gear
# 100.0 fuel
# 63.5 oil
# 26.9 water
# 0.0 rpm
# 0.0 maxrpm


def is_olpc():
    try:
        with open("/etc/fedora-release") as f:
            content = f.read()
        return content[0:4] == "OLPC"
    except IOError:
        return False


class RPMWidget(object):

    def __init__(self, x, y, w, h):
        pass

    def draw(self, cr):
        pass


class rFactorLCDWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.rf_state = rfactorlcd.rFactorState()
        self.lcd_style = rfactorlcd.Style.white_on_black()

    def on_expose_event(self, widget, event):
        if self.window:
            cr = self.window.cairo_create()

            # Restrict Cairo to the exposed area; avoid extra work
            if event:
                cr.rectangle(event.area.x, event.area.y,
                             event.area.width, event.area.height)
                cr.clip()

            cr.set_source_rgb(*self.lcd_style.background_color)
            cr.paint()
            self.draw(cr, 1200, 900, self.rf_state)

    def update_state(self, state):
        self.rf_state = state
        self.queue_draw()

    def draw(self, cr, w, h, state):
        cr.set_antialias(cairo.ANTIALIAS_NONE)
        cr.set_line_width(8.0)
        # cr.set_line_cap(cairo.LINE_CAP_ROUND)

        cr.select_font_face(self.lcd_style.font,
                            self.lcd_style.font_slant,
                            self.lcd_style.font_weight)

        # self.draw_rpm_meter(cr, 700, 480, state.rpm, state.max_rpm)
        self.draw_rpm_meter2(cr, 350, 350, state.rpm, state.max_rpm)
        self.draw_gear(cr, 430, 630, state.gear)
        self.draw_speed(cr, 650, 200, state.speed)
        self.draw_laptime(cr, 50, 770, state.laptime)
        self.draw_position(cr, 50, 870, state.position)
        self.draw_temp(cr, 700, 300, state.oil_temp, state.water_temp, state.fuel)
        self.draw_unknows(cr, 750, 550, state.unknowns)

    def draw_temp(self, cr, cx, cy, oil, water, fuel):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_font_size(60)

        cr.move_to(cx, cy)
        cr.show_text("Oil:")
        cr.move_to(cx+250, cy)
        cr.show_text("%5.1f" % oil)

        cr.move_to(cx, cy + 80)
        cr.show_text("Water:")
        cr.move_to(cx+250, cy + 80)
        cr.show_text("%5.1f" % water)

        cr.move_to(cx, cy + 160)
        cr.show_text("Fuel:")
        cr.move_to(cx+250, cy + 160)
        cr.show_text("%5.1f" % fuel)

    def draw_unknows(self, cr, cx, cy, unknowns):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.set_font_size(50)
        for i, v in enumerate(unknowns):
            cr.move_to(cx, cy + 60 * i)
            cr.show_text(v)

    def draw_position(self, cr, cx, cy, position):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(cx, cy)
        cr.set_font_size(100)
        cr.show_text(position)

    def draw_speed(self, cr, cx, cy, speed):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(cx, cy)
        cr.set_font_size(150)
        cr.show_text("%3d" % speed)
        cr.set_font_size(75)
        cr.show_text("km/h")

    def draw_laptime(self, cr, cx, cy, laptime):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(cx, cy)
        cr.set_font_size(100)
        cr.show_text(laptime)

    def draw_gear(self, cr, cx, cy, gear):
        cr.set_source_rgb(*self.lcd_style.foreground_color)
        cr.move_to(cx, cy)
        cr.set_font_size(300)
        if gear == 0:
            cr.show_text("N")
        elif gear == -1:
            cr.show_text("R")
        else:
            cr.show_text(str(gear))

    def draw_rpm_meter2(self, cr, cx, cy, rpm, max_rpm):
        inner_r = 250.0
        outer_r = 300.0

        cr.save()
        cr.translate(cx, cy)
        cr.set_source_rgb(*self.lcd_style.foreground_color)

        start = 90
        end = 360
        for deg in range(start, end+1, 5):
            rad = math.radians(deg)
            x = math.sin(rad)
            y = math.cos(rad)

            cr.move_to(x * inner_r,
                       y * inner_r)
            cr.line_to(x * outer_r,
                       y * outer_r)
        cr.stroke()

        cr.save()
        rpm_p = rpm / max_rpm

        cr.rotate(math.radians(start + (end - start - 1) * (rpm_p)))
        cr.move_to(-30, 0)
        cr.line_to(0, 30)
        cr.line_to(outer_r * 1.05, 2)
        cr.line_to(outer_r * 1.05, -2)
        cr.line_to(0, -30)
        cr.close_path()

        cr.set_source_rgb(*self.lcd_style.highlight_color)
        cr.fill_preserve()

        cr.set_source_rgb(*self.lcd_style.highlight_dim_color)
        cr.stroke()
        cr.restore()

        cr.restore()

    def draw_rpm_meter(self, cr, cx, cy, rpm, max_rpm):
        rpm_p = rpm / max_rpm

        inner_r = 600.0
        outer_r = 700.0

        inner_squish = 0.4
        outer_squish = 0.6

        inner_offset = 50
        inner_trail = 0.0

        inner_ramp = 0.98

        cr.save()
        cr.translate(cx, cy)

        start = 150
        end = 260
        for deg in range(start, end, 2):
            p = 1.0 - (float(deg - start) / (end - start - 1))

            if p > rpm_p:
                cr.set_source_rgb(0.85, 0.85, 0.85)
            else:
                cr.set_source_rgb(0.0, 0.0, 0.0)

            rad = math.radians(deg)
            x = math.sin(rad)
            y = math.cos(rad)

            ix = math.sin(inner_ramp * rad - inner_trail)
            iy = math.cos(inner_ramp * rad - inner_trail)

            cr.move_to(ix * inner_r, iy * inner_r * inner_squish)
            cr.line_to(x * outer_r + inner_offset, y * outer_r * outer_squish)
            cr.stroke()

        cr.restore()


class App(object):

    def __init__(self):
        self.lcd = None
        self.fullscreen_active = False
        self.window = None
        self.black_on_white = False
        self.quit = False
        self.host = None
        self.port = None
        self.sock = None
        self.cv = threading.Condition()

    def update_network(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
        if not os.path.isdir("logs"):
            os.mkdir("logs")
        with open(os.path.join("logs", time_str + ".log"), "wt") as fout:
            try:
                print "Connecting to %s:%s" % (self.host, self.port)
                self.sock.connect((self.host, self.port))

                while not self.quit:
                    self.sock.sendall("\n")
                    received = self.sock.recv(1024)
                    fout.write(received)

                    try:
                        self.new_state = rfactorlcd.rFactorState(received)
                        glib.idle_add(self.update_state)
                    except Exception as e:
                        print "exception:", e
            finally:
                self.sock.close()

    def update_state(self):
        self.lcd.update_state(self.new_state)
        self.new_state = None

    def on_quit(self, *args):
        self.quit = True
        try:
            self.sock.shutdown(socket.SHUT_WR)
        except:
            pass
        gtk.main_quit()

    def on_toggle_fullscreen(self, *args):
        if self.fullscreen_active:
            self.window.unfullscreen()
            self.fullscreen_active = False
        else:
            self.window.fullscreen()
            self.fullscreen_active = True

    def on_toggle_style(self, *args):
        if self.black_on_white:
            self.black_on_white = False
            self.lcd.lcd_style = rfactorlcd.Style.white_on_black()
            self.lcd.queue_draw()
        else:
            self.black_on_white = True
            self.lcd.lcd_style = rfactorlcd.Style.black_on_white()
            self.lcd.queue_draw()

    def create_accelgroup(self):
        accelgroup = gtk.AccelGroup()

        key, modifier = gtk.accelerator_parse('Escape')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 self.on_quit)

        key, modifier = gtk.accelerator_parse('f')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 self.on_toggle_fullscreen)

        key, modifier = gtk.accelerator_parse('i')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 self.on_toggle_style)

        # key, modifier = gtk.accelerator_parse('space')
        # accelgroup.connect_group(key,
        #                          modifier,
        #                          gtk.ACCEL_VISIBLE,
        #                          lambda *args: renderer.stopwatch.start_stop_watch())
        # key, modifier = gtk.accelerator_parse('Return')
        # accelgroup.connect_group(key,
        #                          modifier,
        #                          gtk.ACCEL_VISIBLE,
        #                          lambda *args: renderer.stopwatch.clear_stop_watch())

        return accelgroup

    def main(self):
        parser = argparse.ArgumentParser(description='rFactor Remote LCD')
        parser.add_argument('HOST', type=str, nargs='?', default="127.0.0.1",
                            help='HOST to connect to')
        parser.add_argument('PORT', type=int, default=2999, nargs='?',
                            help='PORT to connect to')
        args = parser.parse_args()

        self.host = args.HOST
        self.port = args.PORT

        gtk.gdk.threads_init()

        self.window = gtk.Window()
        self.window.set_title("rFactor Remote LCD")
        widget = rFactorLCDWidget()
        self.lcd = widget
        widget.show()
        self.window.add(widget)
        self.window.present()

        self.window.set_default_size(1200, 900)
        self.window.set_size_request(1200, 900)

        if is_olpc():
            self.toggle_fullscreen()

        accelgroup = self.create_accelgroup()
        self.window.add_accel_group(accelgroup)

        self.window.connect("delete-event", self.on_quit)
        # window.connect("realize", realize_cb)

        threading.Thread(target=self.update_network).start()

        gtk.main()


if __name__ == '__main__':
    app = App()
    app.main()


# EOF #
