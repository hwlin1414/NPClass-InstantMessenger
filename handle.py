import socket
import struct

def recv_pkt(sock):
    l = sock.recv(4)
    (l, ) = struct.unpack('!I', l)
    pack = sock.recv(l)
    return pack

def send_pkt(sock, pack):
    pack = struct.pack('!I', len(pack)) + pack
    sock.send(pack)

def recv(sock):
    pack = recv_pkt(sock)
    s = struct.unpack('!32p', pack)
    print s
