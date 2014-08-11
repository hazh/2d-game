#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import tile as TILE
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

#KEY = {
    #".": TileGrass,
    #"%": TileDirt,
    #"#": TileWall,
    #}

class World(object):

    def __init__(self, world_name = "", tile_size = 32):
        self.tile_size = tile_size
        #os independant file paths
        self.world_path = os.path.join("data", world_name)
        self.map = []
        self.tileset_path = "tiles.png"
        self.tiles = pygame.sprite.Group()
        self.load()

    def load(self):
        self.map_from_file = self.get_map_from_file()
        #set some variables for later use
        self.width = len(self.map_from_file[0]) * self.tile_size
        self.height = len(self.map_from_file) * self.tile_size
        self.tileset_image, self.tileset_rect = helpers.load_image(self.tileset_path)
        self.image, self.rect = self.create()

    def get_map_from_file(self):
        #reads the map_from_file from file
        world_file = open(self.world_path, "r")
        map_from_file =  world_file.read().split("\n")
        world_file.close()
        return map_from_file

    def create(self):
        image = pygame.Surface((self.width, self.height)).convert()
        for y, line in enumerate(self.map_from_file):
            for x, char in enumerate(line):
                if char == ".":
                    tile = TILE.TileGrass()
                elif char == "%":
                    tile = TILE.TileDirt()
                elif char == "#":
                    tile = TILE.TileWall()
                tile.set_image(self.tileset_image, (x, y))
                tile.add(self.tiles)
                image.blit(tile.image, (x * self.tile_size, y * self.tile_size))
                self.map.append((x, y, tile))
        return image, image.get_rect()