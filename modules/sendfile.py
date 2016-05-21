#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
import struct
import os
import sys

def main(lines, args):
    if len(lines) < 2:
        print "Usage: sendfile USER FILE"
        return None
    if not os.path.exists(lines[1]):
        print "File Not Found"
        return None
    args['file'] = lines[1]
    return ('hand', {'user': lines[0], 'file': lines[1]})
    
def hand(attr, args):
    if attr['user'] in args['users']:
        pkt = json.dumps({'mod_name': 'sendfile', 'mod_func': 'confirm', 'attr': {'from': args['user'], 'to': attr['user'], 'file': attr['file']}})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['users'][attr['user']]['sock'].send(pack)
    else:
        return ('pr', ('error', "User Not Found"))

def pr(attr, args):
    print "%s: %s" % (attr[0], attr[1])

def confirm(attr, args):
    print "file '%s' from %s, recieve [y/n]?" % (attr['from'], attr['file'])
    while True:
        ans = sys.stdin.readline().rstrip()
        if ans in ('y', 'yes', 'Y', 'Yes', 'YES'):
            ans = True
        else: ans = False
        attr['ans'] = ans
        return ('confirmed', attr)

def confirmed(attr, args):
    if attr['ans'] == False:
        pkt = json.dumps({'mod_name': 'sendfile', 'mod_func': 'pr', 'attr': ('error', 'denied from '+args['user'])})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['users'][attr['from']]['sock'].send(pack)
    else:
        pkt = json.dumps({'mod_name': 'sendfile', 'mod_func': 'tr', 'attr': attr})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['users'][attr['from']]['sock'].send(pack)

def tr(attr, args):
    if not os.path.exists(attr['file']):
        print "File Not Found"
        return None
    st = os.stat(attr['file'])
    i = 0
    f = open(attr['file'])
    attr['size'] = st.st_size
    while True:
        buf = f.read(1024)
        if buf is None or len(buf) == 0:
            break
        i += len(buf)
        
        attr['buf'] = buf
        attr['i'] = i
        pkt = json.dumps({'mod_name': 'sendfile', 'mod_func': 'br', 'attr': attr})
        pack = struct.pack('!I', len(pkt)) + pkt
        args['sock'].send(pack)

        print "%.2f transmitted\r" % (float(attr['i']) / attr['size']),
    print "\ntransmitted done!!!"

def br(attr, args):
    pkt = json.dumps({'mod_name': 'sendfile', 'mod_func': 'rr', 'attr': attr})
    pack = struct.pack('!I', len(pkt)) + pkt
    try:
        args['users'][attr['to']]['sock'].send(pack)
    except:
        pass
    return None

def rr(attr, args):
    print "%.2f transmitted\r" % (float(attr['i']) / attr['size']),
    with open(attr['file'] + '.recieve', "a") as myfile:
        myfile.write(attr['buf'])
    if attr['i'] == attr['size']:
        print "\ntransmitted done!!!"
