#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys

def main(lines, args):
    return ('logout', None)

def ex(attr, args):
    sys.exit(0)

def logout(attr, args):
    del args['users'][args['user']]
    return ('ex', None)
