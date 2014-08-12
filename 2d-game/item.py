#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  




class Item(pygame.sprite.Sprite):

    _items = {
        "1": {
            "name": "key",
            "type": "hand"
        }
    }

    def __init__(self, id):
        self.id = id
        self.name = _items[id]["name"]

class Key(Item):
    def __init__(self):
        Item.__init__(self, id = "1")