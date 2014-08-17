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
            "name": "fist",
            "inventory_type": "hand"
        },
        "2": {
            "name": "key",
            "inventory_type": "hand"
        },
        "3": {
            "name": "sword",
            "inventory_type": "hand"
        },
        "4": {
            "name": "bandage",
            "inventory_type": None
        }
    }

    def __init__(self, image, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.id = id
        self.name = self._items[id]["name"]
        self.inventory_type = self._items[id]["inventory_type"]
        self.use_modifier = -10

    #if item has no use() method then it will be used as a blunt weapon (when in hand inventory slot)

    def use(self, target):
        target.modify_hp(self.use_modifier)

class Fist(Item):
    def __init__(self, image):
        Item.__init__(self, image, id = "1")

class Key(Item):
    def __init__(self, image):
        Item.__init__(self, image, id = "2")

    def use(self, target):
        pass

class Sword(Item):
    def __init__(self, image):
        Item.__init__(self, image, id = "3")
        self.use_modifier = -40

    def use(self, target):
        target.modify_hp(self.use_modifier)
        target.bleeding = True

class Bandage(Item):
    def __init__(self, image):
        Item.__init__(self, image, id = "4")
        self.use_modifier = 40

    def use(self, target):
        target.bleeding = False
        target.modify_hp(self.use_modifier)