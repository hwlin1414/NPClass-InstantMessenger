#!/usr/bin/env python
#-*- coding: utf-8 -*-
import getpass
import sys
import json
import random
import crypt
import string

def main(lines, args):
    print "login: ", 
    u = sys.stdin.readline().rstrip()
    p = getpass.getpass()
    return ('auth', (u, p))

def prn(attr, args):
    if attr['error'] is not None:
        print attr['error']
        return main(None, None)
    print "login success"
    for msg in attr['msg']:
        print "Message from %s: %s" % (msg[0], msg[1])

def auth(attr, args):
    users = args['backend'].get('users')
    if attr[0] not in users:
        return ('prn', {'error': "User Not Found!"})
    
    user = args['backend'].get('user-' + attr[0])
    if user['password'] == crypt.crypt(attr[1], user['password']):
        args['users'][attr[0]] = {'sock': args['sock']}
        return ('prn', {'error': None, 'msg': user['msg']})
    else:
        return ('prn', {'error': "Password Mismatch"})

def main2(lines, args):
    if len(lines) < 2:
        print("Usage: users NAME PASS")
        return
    users = args['backend'].get('users')
    if users is None: users = []
    if lines[0] not in users:
        users.append(lines[0])
    args['backend'].set('users', users)

    passwd = crypt.crypt(lines[1], '$6$' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6)))
    user = args['backend'].get('user-' + lines[0])
    if user is None:
        user = {'friends': [], 'password': passwd, 'msg': []}
    args['backend'].set('user-' + lines[0], user)
