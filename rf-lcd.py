#!/usr/bin/env python

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
import sys
import threading
import glib

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
    except IOError as e:
        return False


def create_accelgroup(window):
    accelgroup = gtk.AccelGroup()
    key, modifier = gtk.accelerator_parse('Escape')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             gtk.main_quit)
    key, modifier = gtk.accelerator_parse('f')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: window.fullscreen())
    key, modifier = gtk.accelerator_parse('space')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: renderer.stopwatch.start_stop_watch())
    key, modifier = gtk.accelerator_parse('Return')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: renderer.stopwatch.clear_stop_watch())
    return accelgroup    


class rFactorState(object):

    def __init__(self, data = None):
        if data:
            cols = data.split(",")
            self.position = cols[0]
            self.unknowns = cols[1:7]
            self.laptime = cols[8]
            self.speed = float(cols[9])
            self.gear = int(cols[10])
            self.fuel = float(cols[11])
            self.oil_temp = float(cols[12])
            self.water_temp = float(cols[13])
            self.rpm = float(cols[14])
            self.max_rpm = float(cols[15])
            if self.max_rpm == 0:
                self.max_rpm = 1
        else:
            self.unknowns = ["u1", "u2", "u3", "u4", "u5", "u6"]
            self.position = "17/17"
            self.speed = 100
            self.gear = 3
            self.laptime = "2:27.36"
            self.oil_temp = 30.5
            self.water_temp = 29.5
            self.fuel = 10.0
            self.rpm = 4000.0
            self.max_rpm = 6000.0


class RPMWidget(object):

    def __init__(self, x, y, w, h):
        pass
        
    def draw(self, cr):
        pass


class rFactorLCDWidget(gtk.DrawingArea):
    
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.rf_state = rFactorState()

    def on_expose_event(self, widget, event):
        if self.window:
            cr = self.window.cairo_create()

            # Restrict Cairo to the exposed area; avoid extra work
            if event:
                cr.rectangle(event.area.x, event.area.y,
                             event.area.width, event.area.height)
                cr.clip()


            cr.set_source_rgb(1, 1, 1)
            cr.paint()
            self.draw(cr, 1200, 900, self.rf_state)

    def update_state(self, state):
        self.rf_state = state
        self.queue_draw()
            
    def draw(self, cr, w, h, state):
        cr.set_antialias(cairo.ANTIALIAS_NONE)
        cr.set_line_width(8.0)
        # cr.set_line_cap(cairo.LINE_CAP_ROUND)

        cr.select_font_face("Incosolata", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        # self.draw_rpm_meter(cr, 700, 480, state.rpm, state.max_rpm)
        self.draw_rpm_meter2(cr, 350, 350, state.rpm, state.max_rpm)
        self.draw_gear(cr, 430, 630, state.gear)
        self.draw_speed(cr, 650, 200, state.speed)
        self.draw_laptime(cr, 50, 770, state.laptime)
        self.draw_position(cr, 50, 870, state.position)
        self.draw_temp(cr, 700, 300, state.oil_temp, state.water_temp, state.fuel)
        self.draw_unknows(cr, 750, 550, state.unknowns)
        
    def draw_temp(self, cr, cx, cy, oil, water, fuel):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.set_font_size(75)      
        
        cr.move_to(cx, cy)        
        cr.show_text("Oil:")
        cr.move_to(cx+300, cy)
        cr.show_text("%5.1f" % oil)

        cr.move_to(cx, cy + 80)
        cr.show_text("Water:")
        cr.move_to(cx+300, cy + 80)
        cr.show_text("%5.1f" % water)

        cr.move_to(cx, cy + 160)
        cr.show_text("Fuel:")
        cr.move_to(cx+300, cy + 160)
        cr.show_text("%5.1f" % fuel)

    def draw_unknows(self, cr, cx, cy, unknowns):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.set_font_size(50)
        for i, v in enumerate(unknowns):
            cr.move_to(cx, cy + 60 * i)
            cr.show_text(v)
        
    def draw_position(self, cr, cx, cy, position):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.move_to(cx, cy)
        cr.set_font_size(100)
        cr.show_text(position)

    def draw_speed(self, cr, cx, cy, speed):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.move_to(cx, cy)
        cr.set_font_size(150)
        cr.show_text("%3d" % speed)
        cr.set_font_size(75)
        cr.show_text("km/h")

    def draw_laptime(self, cr, cx, cy, laptime):
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.move_to(cx, cy)
        cr.set_font_size(100)
        cr.show_text(laptime)

    def draw_gear(self, cr, cx, cy, gear):
        cr.set_source_rgb(0.0, 0.0, 0.0)
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
        cr.set_source_rgb(0, 0, 0)

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
        cr.move_to(-50, 0)
        cr.line_to(0, 50)
        cr.line_to(outer_r * 1.05, 2)
        cr.line_to(outer_r * 1.05, -2)
        cr.line_to(0, -50)
        cr.close_path()
        
        cr.set_source_rgb(1.0, 0, 0)
        cr.fill_preserve()

        cr.set_source_rgb(0, 0, 0)
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
            cr.line_to(x * outer_r +  inner_offset, y * outer_r * outer_squish)
            cr.stroke()

        cr.restore()


def update_network():
    global lcd

    host, port = "192.168.3.10", 2999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))

        while True:
            sock.sendall("\n")
            received = sock.recv(1024)
            
            try:
                state = rFactorState(received)
                glib.idle_add(lcd.update_state, state)
            except Exception as e:
                print("exception:", e)
    finally:
        sock.close()


lcd = None

def main():
    global lcd
    parser = argparse.ArgumentParser(description='rFactor Remote LCD')
    parser.add_argument('HOST', type=str, nargs=1,
                        help='HOST to connect to')
    parser.add_argument('PORT', type=int, default=2999, nargs='?',
                        help='PORT to connect to')
    args = parser.parse_args()

    gtk.gdk.threads_init()

    window = gtk.Window()
    window.set_title("rFactor Remote LCD")
    widget = rFactorLCDWidget()
    lcd = widget
    widget.show()
    window.add(widget)
    window.present()

    window.set_default_size(1200,900)
    window.set_size_request(1200,900)

    if is_olpc():
        window.fullscreen()
        
    accelgroup = create_accelgroup(window)
    window.add_accel_group(accelgroup)

    window.connect("delete-event", gtk.main_quit)
    # window.connect("realize", realize_cb)
    
    threading.Thread(target=update_network).start()

    gtk.main()


if __name__ == '__main__':
    main()


# EOF #
