#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import struct
import json

def main2(lines, args):
    if len(lines) < 1:
        print "Usage: kick USER"
        for u in args['users']:
            print "\t" + u
        return None
    if lines[0] == 'console':
        print "You cannot kick your self XDD"
        return None
    pkt = json.dumps({'mod_name': 'kick', 'mod_func': 'ex', 'attr': "You are kicked by admin(console)"})
    pack = struct.pack('!I', len(pkt)) + pkt
    args['users'][lines[0]]['sock'].send(pack)
    
    del args['users'][lines[0]]
    return None

def ex(attr, args):
    print attr
    sys.exit(0)
