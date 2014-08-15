#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import item
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

    def get(self, i):
        return self.items[i]

    def __str__(self):
        str = "inventory: "
        l = len(self.items) - 1
        for item in self.items:
            if item == self.items[l]:
                end = "."
            else:
                end = ", "
            str += item.name + end
        return str

class Bag(Inventory):
    def __init__(self):
        Inventory.__init__(self, length = 25)

class UniqueInventory(Inventory):
    def __init__(self, type):
        Inventory.__init__(self, length = 1)
        self.type = type

    def add(self, item):
        if item.inventory_type == self.type:
            self.items[0] = item
            return True
        else:
            print "Wrong item type for this inventory"
            return False

    def empty(self):
        self.items[0] = None

    def get(self):
        return self.items[0]

class Hand(UniqueInventory):
    def __init__(self):
        UniqueInventory.__init__(self, type = "hand")

    def get(self):
        if self.items[0] != None:
            return self.items[0]
        else:
            return item.Fist(helpers.load_image("key.png"))