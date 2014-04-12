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


import SocketServer
import threading


class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        with open("rfactorlcd-dummy-server.log") as fin:
            while True:
                line = fin.readline()
                if not line:
                    fin.seek(0)
                self.data = self.request.recv(1024)
                self.request.sendall(line)
                # time.sleep(0.001)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def main():
    try:
        host, port = "", 2999
        # server = SocketServer.TCPServer((host, port), MyTCPHandler)
        server = ThreadedTCPServer((host, port), MyTCPHandler)

        print "dummy server is listening on %s:%d" % (host, port)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        server_thread.join()
    except:
        raise


if __name__ == '__main__':
    main()


# EOF #
