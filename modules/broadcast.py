#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import struct
import json

def main2(lines, args):
    if len(lines) < 1:
        print "Usage: broadcast MSG"
        return None
    for u in args['users']:
        if u == 'console':
            continue

        pkt = json.dumps({'mod_name': 'broadcast', 'mod_func': 'pr', 'attr': 'console: ' + ' '.join(lines)})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['users'][u]['sock'].send(pack)
    return None

def pr(attr, args):
    print attr
