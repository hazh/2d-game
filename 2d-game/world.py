#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import ConfigParser
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  

class World:

    def __init__(self, world_name = "", world_key = "", tile_size = 64):
        self.tile_size = tile_size
        #map_from_file is stored in a 2d array
        self.map_from_file = []
        self.map = []
        #the key finds the corresponding tile according to map_from_file character
        self.key = {}
        #os independant file paths
        self.world_path = os.path.join("data", world_name)
        self.key_path = os.path.join("data", world_key)

        self.load_tiles("tiles.png")
        self.load_map_from_file()
        self.image, self.rect = self.create()

    def load_tiles(self, name):
        #load the tileset
        world_image, world_rect = helpers.load_image(name)
        image_width = world_image.get_width()
        self.tiles = []
        #cut each tile from the tileset and append to an array for later use
        for i in range (0, image_width / self.tile_size):
            rect = (i * self.tile_size, 0, self.tile_size, self.tile_size)
            self.tiles.append(world_image.subsurface(rect))
    
    def load_map_from_file(self):
        #reads the map_from_file from file
        world_file = open(self.world_path, "r")
        self.map_from_file = world_file.read().split("\n")
        world_file.close()

        #reads the key from file
        parser = ConfigParser.ConfigParser()
        parser.read(self.key_path)
        for section in parser.sections():
            tile_description = dict(parser.items(section))
            self.key[section] = tile_description

        #set some variables for later use
        self.width = len(self.map_from_file[0]) * self.tile_size
        self.height = len(self.map_from_file) * self.tile_size
        
    def create(self):
        #build the world image, also return its rect
        image = pygame.Surface((self.width, self.height)).convert()
        for y, line in enumerate(self.map_from_file):
            for x, tile in enumerate(line):
                tile = self.key[tile]
                try:
                    tile_id = int(tile["id"])
                except (ValueError, KeyError):
                    tile_id = int(0)
                tile_image = self.tiles[tile_id]
                image.blit(tile_image, (x * self.tile_size, y * self.tile_size))
                if not tile_id == 2:
                    self.map.append((x, y, tile_id))
        return image, image.get_rect()

    def get_tile_id(self, x, y):
        return self.map[y][x][2]

    def get_tile_description(self, tile_id):
        for tile in self.key.iteritems():
            if int(tile[1]["id"]) == tile_id:
                return tile[1]["name"]
               