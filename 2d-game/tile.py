#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, location, id, name, tile_size = 32, weight = 1):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.left, self.rect.top = location[0] * tile_size, location[1] * tile_size
        self.id = id
        self.name = name
        self.tile_size = tile_size
        self.weight = weight

    def get_id(self):
        return self.id

    def get_weight(self):
        return self.weight

    def on_traverse(self):
        pass

class TileDirt(Tile):
    def __init__(self, image, location):
        Tile.__init__(self, image, location, id = 1, name = "Dirt", weight = 2)

class TileGrass(Tile):
    def __init__(self, image, location):
        Tile.__init__(self, image, location, id = 0, name = "Grass")

class TileWall(Tile):
    def __init__(self, image, location):
        Tile.__init__(self, image, location, id = 2, name = "Wall", weight = "inf")