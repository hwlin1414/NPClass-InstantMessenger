#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import argparse
import sys
import socket, ssl
import select
import backends
import handle

cfgfile = ('server.conf.example', 'server.conf')

def get_backend(cfg):
    if 'backend' not in cfg['defaults']:
        print "no backend selected"
        sys.exit(1)
    if cfg['defaults']['backend'] not in cfg:
        print "backend not configured"
        sys.exit(1)
    if not hasattr(backends, cfg['defaults']['backend']):
        print "backend not found"
        sys.exit(1)
    dbconf = cfg[cfg['defaults']['backend']]
    del dbconf['__name__']
    backend = getattr(backends, cfg['defaults']['backend']).database(**dbconf)
    return backend.open()

def main(args, cfg, backend):
    users = {}
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile = cfg['defaults']['cert'], keyfile = cfg['defaults']['key'])
    svsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    svsock.bind((args['listen'], args['port']))
    svsock.listen(socket.SOMAXCONN)
    listen = [svsock, sys.stdin]
    while True:
        socks = select.select(listen, [], [])
        for sock in socks[0]:
            if sock == sys.stdin:
                line = sys.stdin.readline()
                if line == '\n':
                    print users
                    continue
                handle.cmd(None, line, {'cfg': cfg, 'backend': backend, 'users': users, 'sock': sock, 'user': None}, 'main2')
                pass
            elif sock == svsock:
                newsock, fromaddr = sock.accept()
                listen.append(context.wrap_socket(newsock, server_side=True))
            else:
                try:
                    u = None
                    for _ in users:
                        if users[_]['sock'] == sock: u = _
                    handle.recv(sock, {'cfg': cfg, 'backend': backend, 'users': users, 'sock': sock, 'user': u})
                except socket.error, e:
                    todel = None
                    for _ in users:
                        if users[_]['sock'] == sock: todel = _
                    if todel is not None: del users[todel]
                    sock.close()
                    listen.remove(sock)

if __name__ == "__main__":
    cfg = {
        'listen': '0.0.0.0',
        'port': '4096',
    }
    Config = ConfigParser.ConfigParser(cfg, allow_no_value = True)
    for file in cfgfile:
        Config.read(file)
        if Config.has_section('defaults'):
            cfg = Config._sections

    parser = argparse.ArgumentParser(description = "Instant Messanger Server", prog = sys.argv[0])
    parser.add_argument('-l', dest = 'listen', help = "Listen interface")
    parser.add_argument('-p', dest = 'port', type=int, help = "Listen port")
    parser.add_argument('-d', dest = 'debug', action="store_true", help = "Debug mode")
    parser.set_defaults(**cfg['defaults'])
    args = vars(parser.parse_args(sys.argv[1:]))
    if args['debug']: print args

    backend = get_backend(cfg)
    if backend is None: 
        print "backend error"
        sys.exit(1)
    try:
        main(args, cfg, backend)
    except KeyboardInterrupt, e:
        print ""
        sys.exit(0)
