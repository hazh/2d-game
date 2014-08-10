#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  

class Player(pygame.sprite.Sprite):
    
    def __init__(self, tile_size = 64):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = helpers.load_image("player.png")
        self.tile_size = tile_size
        #player position relative to screen
        self.position = [0, 0]
        #player position relative to map
        self.location = [0, 0]
        self.movement_cooldown = 0.0
        self.movement_limit = 0.16
        self.movement_points = [0, 0, 0, 0] #up, right, down, left
        
    def update(self):
        #set rect according to position
        #for other entities the position will be their location relative to map
        x, y = self.get_position()
        self.rect.top = y
        self.rect.left = x

    def get_position(self):
        x = int(self.position[0])
        y = int(self.position[1])
        return x, y

    def get_coordinates(self):
        x = int(self.location[0]) / self.tile_size
        y = int(self.location[1]) / self.tile_size
        return x, y

    def get_movement_points(self, i):
        return self.movement_points[i]

    def set_movement_points(self, direction):
        if direction == "up":
            self.movement_points[0] = self.tile_size
        if direction == "right":
            self.movement_points[1] = self.tile_size
        if direction == "down":
            self.movement_points[2] = self.tile_size
        if direction == "left":
            self.movement_points[3] = self.tile_size

    def modify_movement_points(self, i, modifier):
        if self.movement_points[i] != 0:
            self.movement_points[i] += modifier
        else:
            pass