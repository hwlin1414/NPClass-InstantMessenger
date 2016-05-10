import socket
import struct
import shlex
import json
import modules

def recv_pkt(sock):
    l = sock.recv(4)
    if len(l) == 0: raise socket.error
    elif len(l) < 4:
        print "Recieve Length Error"
        return None
    (l, ) = struct.unpack('!I', l)
    pack = sock.recv(l)
    if len(pack) != l:
        print "Recieve Length Error"
        return None
    return pack

def send_pkt(sock, mod_name, mod_func, attr):
    pkt = json.dumps({'mod_name': mod_name, 'mod_func': mod_func, 'attr': attr})
    pack = struct.pack('!I', len(pkt)) + pkt
    sock.send(pack)

def cmd(sock, lines):
    lines = shlex.split(lines)
    if len(lines) < 2:
        print "Command Length Error"
    try:
        mod = getattr(modules, lines[0])
        func = getattr(mod, 'main')
    except AttributeError, e:
        print "Command Not Found"
        return
    ret = func(lines[1:])
    if ret is not None:
        (func, attr) = ret
        send_pkt(sock, lines[0], func, attr)

def recv(sock):
    pack = recv_pkt(sock)
    if pack is None: return False
    print pack
    pack = json.loads(pack)
    try:
        mod = getattr(modules, pack['mod_name'])
        func = getattr(mod, pack['mod_func'])
    except AttributeError, e:
        print "Unknown Pack Recieved:"
        print pack
        return True
    ret = func(pack['attr'])
    if ret is not None:
        (func, attr) = ret
        send_pkt(sock, pack['mod_name'], func, attr)
