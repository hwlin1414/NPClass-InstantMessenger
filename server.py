#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import argparse
import sys
import os
import backends

cfgfile = ('server.conf', )

def get_backend(cfg):
    if 'backend' not in cfg['defaults']:
        print "no backend selected"
        sys.exit(1)
    if cfg['defaults']['backend'] not in cfg:
        print "backend not configured"
        sys.exit(1)
    if not hasattr(backends, cfg['defaults']['backend']):
        print "backend not support"
        sys.exit(1)
    dbconf = cfg[cfg['defaults']['backend']]
    del dbconf['__name__']
    backend = getattr(backends, cfg['defaults']['backend']).database(**dbconf)
    return backend.open()

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
    parser.set_defaults(**cfg)
    args = vars(parser.parse_args(sys.argv[1:]))

    backend = get_backend(cfg)
    if backend is None: 
        print "backend error"
        sys.exit(1)
