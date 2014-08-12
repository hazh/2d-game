#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  

class Inventory(object):
    def __init__(self, length):
        self.items = [None] * length

    def add(self, i, item):
        self.items[i] = item

    def remove(self, i):
        self.items[i] = None

    def read(self):
        for item in self.items:
            print item

class Bag(Inventory):
    def __init__(self):
        Inventory.__init__(self, length = 25)

class UniqueInventory(Inventory):
    def __init__(self, type):
        Inventory.__init__(self, length = 1)
        self.type = type

    def add(self, item):
        if item.type == self.type:
            self.items[0] = item
        else:
            print "Wrong item type for this inventory"
            pass

    def empty(self):
        self.items[0] = None

class Hand(UniqueInventory):
    def __init__(self):
        UniqueInventory.__init__(self)
