#!/usr/bin/env python


import socket
import struct
from rfactorlcd.ac_state import HandshakeResponse, RTLap, RTCarInfo

host = "duo"
port = 9996

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    print "sending handshake..."
    sock.sendto(struct.pack("<III", 1, 1, 0), (host, port))

    print "receiving..."
    d, a = sock.recvfrom(4096)
    print HandshakeResponse(d)

    print "sending register..."
    sock.sendto(struct.pack("<III", 1, 1, 1), (host, port))
    while True:
        print "receiving..."
        d, a = sock.recvfrom(4096)
        print RTCarInfo(d)

finally:
    print "sending end connection:"
    sock.sendto(struct.pack("<III", 1, 1, 3), (host, port))


# EOF #
