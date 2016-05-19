#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import struct
import json

def main(lines, args):
    if len(lines) < 1:
        print "Usage: talk USER"
        return None
    args['sendto'] = lines[0]
    args['handle_stdin'] = hand
    print ">",
    sys.stdout.flush()
    return ('check', {'to': args['sendto']})

def hand(args):
    line = sys.stdin.readline().rstrip()
    if args['arg']['debug']: print "hand got line: %s" % (line)
    if line == 'exit':
        ex(None, args)
        return
    pkt = json.dumps({'mod_name': 'talk', 'mod_func': 'route', 'attr': {'to': args['sendto'], 'msg': line}})
    pack = struct.pack('!I', len(pkt)) + pkt
    args['sock'].send(pack)
    print ">",
    sys.stdout.flush()

def ex(attr, args):
    if attr is not None: print attr
    args['handle_stdin'] = None
    return None

def check(attr, args):
    if attr['to'] not in args['users']:
        return ('ex', "error: user not online")
    return None
    
def route(attr, args):
    if attr['to'] in args['users']:
        attr['from'] = args['user']
        pkt = json.dumps({'mod_name': 'talk', 'mod_func': 'pr', 'attr': attr})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['users'][attr['to']]['sock'].send(pack)
    else:
        return ('ex', "error: user not online")

def pr(attr, args):
    print "%s: %s" % (attr['from'], attr['msg'])
    print ">",
    sys.stdout.flush()
