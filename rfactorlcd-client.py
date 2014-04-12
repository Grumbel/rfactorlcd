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


import struct
import socket


class rFactorLCDClient(object):

    def __init__(self):
        self.host = "duo"
        self.port = 4580

    def on_start_session(self, payload):
        print "start_session"

    def on_end_session(self, payload):
        print "end_session"

    def on_start_realtime(self, payload):
        print "start_realtime"

    def on_end_realtime(self, payload):
        print "end_realtime"

    def on_telemetry(self, payload):
        print "telemetry"

    def on_vehicle(self, payload):
        print "vehicle"

    def on_score(self, payload):
        print "score"

    def dispatch_message(self, tag, payload):
        if tag == "STSS":
            self.on_start_session(payload)
        elif tag == "EDSS":
            self.on_end_session(payload)
        elif tag == "STRT":
            self.on_start_realtime(payload)
        elif tag == "EDRT":
            self.on_end_realtime(payload)
        elif tag == "VHCL":
            self.on_vehicle(payload)
        elif tag == "TLMT":
            self.on_telemetry(payload)
        elif tag == "SCOR":
            self.on_score(payload)
        else:
            print "error: unhandled tag: %s" % tag

    def main(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Connecting to %s:%s" % (self.host, self.port)
            self.sock.connect((self.host, self.port))
            stream = ""
            while True:
                self.sock.sendall("\n")
                stream += self.sock.recv(4096 * 4)
                if len(stream) >= 8:
                    tag, size = struct.unpack_from("4sI", stream)
                    if len(stream) >= size:
                        payload = stream[8:size]
                        stream = stream[size:]
                        print tag, size

                        self.dispatch_message(tag, payload)
        finally:
            self.sock.close()


if __name__ == '__main__':
    app = rFactorLCDClient()
    app.main()


# EOF #
