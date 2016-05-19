#!/usr/bin/env python
#-*- coding: utf-8 -*-

def main(lines, args):
    return ('hand', lines[0])

def hand(attr, args):
    if attr['user'] in args['users']:
        pkt = json.dumps({'mod_name': 'talk', 'mod_func': 'ask', 'attr': args['user']})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['users'][attr['user']]['sock'].send(pack)
    else:
        return ('pr', "error: user not online")

def pr(attr, args):
    print "%s: %s" % (attr[0], attr[1])
