#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
import os

class database(object):
    def __init__(self, path='db.json'):
        self.path = path

    def open(self):
        if os.path.exists(self.path) == False:
            f = open(self.path, 'w')
            f.write("{}")
            f.close()
        f = open(self.path)
        self.data = json.load(f)
        f.close()

        self.check()
        return self

    def check(self):
        if self.data is None: self.data = {}

    def get(self, key, default = None):
        if key in self.data: return self.data[key]
        return None

    def set(self, key, val):
        self.data[key] = val
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.data))

    def unset(self, key):
        if key in self.data: del self.data[key]
