#!/usr/bin/env python
#-*- coding: utf-8 -*-

def main(lines, args):
    if len(lines) < 1:
        print "Usage: friend (add | rm | list)"
        return (None, None)
    if lines[0] in ('add', 'rm', 'list'):
        return (lines[0], lines[1:])
    print "Usage: friend (add | rm | list)"
    return (None, None)

def add(attr, args):
    user = args['backend'].get('user-' + args['user'])
    if user is None:
        print "user error? (add)"
        user = {'friends': [], 'password': passwd, 'msg': []}
    print attr[0]
    if attr[0] not in user['friends']:
        user['friends'].append(attr[0])
    args['backend'].set('user-' + args['user'], user)

def list(attr, args):
    user = args['backend'].get('user-' + args['user'])
    if user is None:
        print "user error? (list)"
        user = {'friends': [], 'password': passwd, 'msg': []}
    print user['friends']
    frs = user['friends']
    frlist = []
    for fr in frs:
        if fr in args['users']: frlist.append((fr, 'online'))
        else: frlist.append((fr, 'offline'))
    return ('pr', frlist)

def pr(attr, args):
    for fr in attr:
        print fr[0], fr[1]

def rm(attr, args):
    user = args['backend'].get('user-' + args['user'])
    if user is None:
        print "user error? (rm)"
        user = {'friends': [], 'password': passwd, 'msg': []}
    if attr[0] in user['friends']:
        user['friends'].remove(attr[0])
    args['backend'].set('user-' + args['user'], user)
