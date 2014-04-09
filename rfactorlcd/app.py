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
import gtk
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
                        state = rfactorlcd.rFactorState(received)
                        glib.idle_add(self.lcd.update_state, state)
                    except Exception as e:
                        print "exception:", e
            finally:
                self.sock.close()

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
        widget = rfactorlcd.LCDWidget()
        self.lcd = widget
        widget.show()
        self.window.add(widget)
        self.window.present()

        self.window.set_default_size(1200, 900)
        self.window.set_size_request(1200, 900)

        if is_olpc():
            self.on_toggle_fullscreen()

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
