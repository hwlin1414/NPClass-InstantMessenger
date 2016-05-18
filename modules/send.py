#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
import struct

def main(lines, args):
    return ('hand', {'user': lines[0], 'msg': ' '.join(lines[1:])})
    
def hand(attr, args):
    if attr['user'] in args['users']:
        pkt = json.dumps({'mod_name': 'send', 'mod_func': 'pr', 'attr': (args['user'], attr['msg'])})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['users'][attr['user']]['sock'].send(pack)
    else:
        users = args['backend'].get('users')
        if attr['user'] not in users:
            return ('pr', ('error', "User Not Found"))

        user = args['backend'].get('user-' + attr['user'])
        if user is None:
            print "user error? (add)"
            user = {'friends': [], 'password': passwd, 'msg': []}
        user['msg'].append((args['user'], attr['msg']))
        args['backend'].set('user-' + attr['user'], user)
        

def pr(attr, args):
    print "%s: %s" % (attr[0], attr[1])

def main2(lines, args):
    hand({'user': lines[0], 'msg': lines[1]}, args)
