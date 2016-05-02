#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import argparse
import sys
import os

if __name__ == "__main__":
    cfg = {
        'server': 'localhost',
        'port': '4096',
    }

    parser = argparse.ArgumentParser(description = "Instant Messanger Client", prog = sys.argv[0])
    parser.add_argument('-p', dest = 'port', type=int, help = "Listen port")
    parser.add_argument('server', help = "Server")
    parser.set_defaults(**cfg)
    args = vars(parser.parse_args(sys.argv[1:]))
    print args
