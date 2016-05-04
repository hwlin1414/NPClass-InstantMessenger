#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import argparse
import sys
import os
import socket, ssl
import select

def main(args):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE
    context.check_hostname = False
    context.load_default_certs()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(sock)
    try:
        ssl_sock.connect((args['server'], args['port']))
    except socket.error, e:
        print "socket error %d: %s" % (e.args[0], e.args[1])
    listen = [ssl_sock, sys.stdin]
    while True:
        handles = select.select(listen, [], [])
        for handle in handles[0]:
            if handle == sys.stdin:
                try:
                    ssl_sock.send(sys.stdin.readline()),
                except socket.error:
                    ssl_sock.close()
                    listen.remove(ssl_sock)
                    return
            else:
                try:
                    msg = handle.recv(256)
                    if len(msg) == 0: raise socket.error
                    print "%s: %s" % (str(handle.getpeername()), msg) ,
                except socket.error, e:
                    handle.close()
                    listen.remove(handle)
                    return

if __name__ == "__main__":
    cfg = {
        'server': 'localhost',
        'port': '4096',
    }

    parser = argparse.ArgumentParser(description = "Instant Messanger Client", prog = sys.argv[0])
    parser.add_argument('-p', dest = 'port', type=int, help = "Listen port")
    parser.add_argument('-d', dest = 'debug', action="store_true", help = "Debug mode")
    parser.add_argument('server', help = "Server")
    parser.set_defaults(**cfg)
    args = vars(parser.parse_args(sys.argv[1:]))
    if args['debug']: print args
    try:
        main(args)
    except KeyboardInterrupt, e:
        print ""
        sys.exit(0)
