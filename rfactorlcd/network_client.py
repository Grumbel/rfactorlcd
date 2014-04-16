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


import datetime
import errno
import os
import select
import socket
import struct
import threading
import time


class ConnectionClosed(Exception):
    pass


class NetworkClient:

    def __init__(self, host, port=4580):
        self.host = host
        self.port = port
        self.sock = None
        self.lock = threading.Lock()
        self.new_data = {}
        self._shutdown = False

        # with open(os.path.join("logs", time_str + ".log"), "wt") as fout:

    def shutdown(self):
        self._shutdown = True
        try:
            self.sock.shutdown(socket.SHUT_WR)
        except:
            pass

    def run(self):
        time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
        if not os.path.isdir("logs"):
            os.mkdir("logs")
        print "writing log to %s" % time_str

        while not self._shutdown:
            try:
                self.sock = None
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.sock.connect((self.host, self.port))
                    self.sock.setblocking(0)
                    print "connection successful: %s:%s" % (self.host, self.port)
                    while not self._shutdown:
                        self.update()
                except socket.error as err:
                    if err.errno == errno.ECONNREFUSED or \
                       err.errno == errno.ECONNABORTED or \
                       err.errno == errno.ECONNRESET:
                        print "connection error, trying reconnect: %s:%s %s" % (self.host, self.port, err)
                        time.sleep(1)
                    else:
                        raise
                except ConnectionClosed as err:
                    pass
            finally:
                if self.sock is not None:
                    self.sock.close()

    def release_data(self):
        self.lock.acquire()
        result = self.new_data
        self.new_data = {}
        self.lock.release()
        return result

    def update(self):
        stream = ""
        buf = bytearray(4096)
        view = memoryview(buf)
        while not self._shutdown:
            # send keep-alive to signal we are ready for data
            self.sock.sendall("\n")

            # block until there is data
            select.select([self.sock], [], [])

            # read all data
            while not self._shutdown:
                try:
                    print "trying recv"
                    nbytes = self.sock.recv_into(view, 4096)
                    if nbytes == 0:
                        print "connection shutting down"
                        raise ConnectionClosed()
                    print "trying recv done:", nbytes
                    stream += view[0:nbytes].tobytes()
                except socket.error as serr:
                    print serr
                    if serr.errno != errno.EWOULDBLOCK:
                        raise
                    break

            self.lock.acquire()
            while len(stream) >= 8:
                tag, size = struct.unpack_from("4sI", stream)
                if len(stream) < size:
                    # need more data from the network
                    break
                else:
                    # fout.write(stream[0:size])
                    payload = stream[8:size]
                    stream = stream[size:]

                    # if data comes in faster then it gets eaten,
                    # discard it, only keep the latest copy of
                    # each tag
                    self.new_data[tag] = payload
            self.lock.release()


# EOF #
