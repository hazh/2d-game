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
    
    def __init__(self, tile_size = 32):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = helpers.load_image("player.png")
        self.tile_size = tile_size
        #player position relative to screen
        self.position = (0, 0)
        #player position relative to map
        self.location = (1, 1)
        self.path = []
        self.movement_cooldown = 0.0
        self.movement_limit = 0.16
        self.movement_points = [0, 0, 0, 0] #up, right, down, left:
        
    def update(self):
        self.handle_movement()
        #set rect according to position
        x, y = self.get_position()
        self.rect.top = y
        self.rect.left = x

    def get_position(self):
        x = int(self.location[0] * self.tile_size)
        y = int(self.location[1] * self.tile_size)
        return x, y

    def handle_movement(self):
        s = self.tile_size / (self.movement_limit * 100)

        if self.path != [] and self.movement_points == [0, 0, 0, 0]:
            current = self.location
            next = self.path.pop()
            if next[1] < current[1]:
                self.set_movement_points("up")
            elif next[0] > current[0]:
                self.set_movement_points("right")
            elif next[1] > current[1]:
                self.set_movement_points("down")
            elif next[0] < current[0]:
                self.set_movement_points("left")       

        tmp_list = list(self.location)
        if self.get_movement_points("up") > 0:
            tmp_list[1] -= 1
            self.location = tuple(tmp_list)
            self.modify_movement_points(0, -s)
        elif self.get_movement_points("right") > 0:
            tmp_list[0] += 1
            self.location = tuple(tmp_list)
            self.modify_movement_points(1, -s)
        elif self.get_movement_points("down") > 0:
            tmp_list[1] += 1
            self.location = tuple(tmp_list)
            self.modify_movement_points(2, -s)
        elif self.get_movement_points("left") > 0:
            tmp_list[0] -= 1
            self.location = tuple(tmp_list)
            self.modify_movement_points(3, -s)

    def get_movement_points(self, direction):
        if direction == "up":
            return self.movement_points[0]
        if direction == "right":
            return self.movement_points[1]
        if direction == "down":
            return self.movement_points[2]
        if direction == "left":
            return self.movement_points[3]

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