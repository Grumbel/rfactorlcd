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

    msg_type = 1

    print "sending register..."
    sock.sendto(struct.pack("<III", 1, 1, msg_type), (host, port))
    while True:
        print "receiving..."
        d, a = sock.recvfrom(4096)
        if msg_type == 1:
            print RTCarInfo(d)
        elif msg_type == 2:
            print RTLap(d)
        else:
            raise RuntimeError("unknown msg_type: %d" % msg_type)

finally:
    print "sending end connection:"
    sock.sendto(struct.pack("<III", 1, 1, 3), (host, port))


# EOF #
