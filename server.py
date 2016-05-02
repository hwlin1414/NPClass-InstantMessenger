#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import argparse
import sys
import os

if __name__ == "__main__":
    cfg = {
        'listen': '0.0.0.0',
        'port': '4096',
    }

    parser = argparse.ArgumentParser(description = "Instant Messanger Server", prog = sys.argv[0])
    parser.add_argument('-l', dest = 'listen', help = "Listen interface")
    parser.add_argument('-p', dest = 'port', type=int, help = "Listen port")
    parser.add_argument('-d', dest = 'daemonize', action="store_true", help = "Daemonize")
    parser.set_defaults(**cfg)
    args = vars(parser.parse_args(sys.argv[1:]))
    print args
