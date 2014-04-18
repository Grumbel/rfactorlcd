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
import glib
import gtk
import logging
import threading
import sys

import rfactorlcd


class App(object):

    def __init__(self):
        self.lcd = None
        self.fullscreen_active = False
        self.window = None
        self.black_on_white = True
        self.quit = False

    def on_timeout(self):
        data = self.client.release_data()
        for tag, payload in data.items():
            self.lcd.update_state(tag, payload)
        return True

    def on_quit(self, *args):
        self.quit = True
        self.client.shutdown()
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
            self.lcd.set_lcd_style(rfactorlcd.Style.white_on_black())
            self.lcd.queue_draw()
        else:
            self.black_on_white = True
            self.lcd.set_lcd_style(rfactorlcd.Style.black_on_white())
            self.lcd.queue_draw()

    def on_load(self, *args):
        self.lcd.workspace.load("/tmp/testomat.rflcd")
        self.lcd.queue_draw()

    def on_save(self, *args):
        self.lcd.workspace.save("/tmp/testomat.rflcd")

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

        key, modifier = gtk.accelerator_parse('F5')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 self.on_load)

        key, modifier = gtk.accelerator_parse('F6')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 self.on_save)

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
        parser.add_argument('PORT', type=int, default=4580, nargs='?',
                            help='PORT to connect to')
        parser.add_argument("-c", "--config", type=str,
                            help="Config file to load")
        parser.add_argument("-v", "--verbose", action='store_true',
                            help="Be more verbose")
        parser.add_argument("--debug", action='store_true',
                            help="Be even more verbose")
        args = parser.parse_args()

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s: %(message)s")

        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(formatter)
        if args.debug:
            stream_handler.setLevel(logging.DEBUG)
        elif args.verbose:
            stream_handler.setLevel(logging.INFO)
        else:
            stream_handler.setLevel(logging.WARN)

        logfile_handler = logging.FileHandler("rfactorlcd-gui.log", mode='w')
        logfile_handler.setLevel(logging.DEBUG)
        logfile_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(logfile_handler)

        logging.debug("Debug!")
        logging.info("Info!")
        logging.error("Err!")
        logging.warning("Warn!")

        gtk.gdk.threads_init()

        self.window = gtk.Window()
        self.window.set_title("rFactor Remote LCD")
        widget = rfactorlcd.LCDWidget()
        self.lcd = widget
        if args.config:
            self.lcd.workspace.load(args.config)
        else:
            self.lcd.workspace.load_default()
        widget.show()
        self.window.add(widget)
        self.window.present()

        self.window.set_default_size(1200, 900)
        self.window.set_size_request(1200, 900)

        if rfactorlcd.is_olpc():
            self.on_toggle_fullscreen()

        accelgroup = self.create_accelgroup()
        self.window.add_accel_group(accelgroup)

        self.window.connect("delete-event", self.on_quit)
        # window.connect("realize", realize_cb)

        glib.timeout_add(1000 / 180, self.on_timeout)

        self.client = rfactorlcd.NetworkClient(args.HOST, args.PORT)
        self.client_thread = threading.Thread(target=self.client.run)
        self.client_thread.daemon = True
        self.client_thread.start()

        gtk.main()

        self.client.shutdown()
        self.client_thread.join()

if __name__ == '__main__':
    app = App()
    app.main()


# EOF #
