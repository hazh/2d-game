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
    def __init__(self, id, name, tile_size = 32, weight = 1):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.name = name
        self.tile_size = tile_size
        self.weight = weight

    def set_image(self, tileset_image, location, type):
        self.type = type
        rect = (self.id * self.tile_size, self.type * self.tile_size, self.tile_size, self.tile_size)
        self.image = tileset_image.subsurface(rect)
        self.rect = (location[0] * self.tile_size, location[1] * self.tile_size, self.tile_size, self.tile_size)

    def get_id(self):
        return self.id

    def get_weight(self):
        return self.weight

    def on_traverse(self):
        pass

class TileDirt(Tile):
    def __init__(self):
        super(TileDirt, self).__init__(id = 1, name = "Dirt", weight = 2)

class TileGrass(Tile):
    def __init__(self):
        super(TileGrass, self).__init__(id = 0, name = "Grass")

class TileWall(Tile):
    def __init__(self):
        super(TileWall, self).__init__(id = 2, name = "Wall", weight = "inf")