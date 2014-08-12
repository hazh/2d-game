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
    def __init__(self, name):
        self.name = name
        self.image, self.rect = helpers.load_image(name+".png")

class Key(Item):
    def __init__(self):
        super(Key, self).__init__(name = "Key")