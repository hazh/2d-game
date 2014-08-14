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
            "inventory_type": "hand"
        }
    }

    def __init__(self, image, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.id = id
        self.name = self._items[id]["name"]
        self.inventory_type = self._items[id]["inventory_type"]

    #if item has no use() method then it will be used as a blunt weapon

    def use(self, target):
        target.modify_hp(-40)

class Key(Item):
    def __init__(self, image):
        Item.__init__(self, image, id = "1")