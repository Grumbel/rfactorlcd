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
	                msg = stream[8:size]
                        stream = stream[size:]
                        print tag, size
			#if tag == "TELM":
			#    print "TeleM", struct.unpack_from("ffff", msg)
			#elif tag == "SCOR":
			#    l = struct.unpack_from("B", msg)
			#    print "Score", struct.unpack_from("%dsIff" % l, msg[1:])
			#else:
			#    print tag
        finally:
            self.sock.close()


if __name__ == '__main__':
    app = rFactorLCDClient()
    app.main()


# EOF #
