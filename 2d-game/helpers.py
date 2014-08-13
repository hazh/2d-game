#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  

class Image(object):
    _images_to_load = ["player", "key", "tile_grass", "tile_dirt", "tile_wall"]
    _loaded = {}
    def __init__(self):
        for name in self._images_to_load:
            self._loaded[name] = load_image(name + ".png")

    @property
    def player(self):
        return self._loaded["player"]

    @property
    def key(self):
        return self._loaded["key"]

    @property
    def tile_grass(self):
        return self._loaded["tile_grass"]

    @property
    def tile_dirt(self):
        return self._loaded["tile_dirt"]

    @property
    def tile_wall(self):
        return self._loaded["tile_wall"]

def load_image(name):
    #load an image and get its rect
    fullname = os.path.join("images", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()        
    except pygame.error, message:
        print "cannot load image:", name
        raise SystemExit, message
    return image        

def load_sound(name):
    #load a sound
    fullname = os.path.join("sounds", name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Cannot load sound:", wav
        raise SystemExit, message
    return sound
