#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import inventory
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  

class Entity(pygame.sprite.Sprite):
    
    def __init__(self, image, spawn_location = (1, 1), tile_size = 32):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.tile_size = tile_size
        #entity position relative to screen
        self.rect.left, self.rect.top = 32, 32
        self.path = []
        self.movement_cooldown = 0.0
        self.movement_limit = 0.08
        self.movement_points = [0, 0, 0, 0] #up, right, down, left:

        ########self.hand = inventory.Hand()
        
    def update(self, dt, camera_viewport):
        self.handle_movement(dt)
        self.set_location(camera_viewport)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def set_location(self, offset):
        self.location =  (round((self.rect.left + offset[0]) / self.tile_size), round((self.rect.top + offset[1]) / self.tile_size))

    def handle_movement(self, dt):
        self.movement_cooldown += dt
        if self.movement_cooldown >= self.movement_limit and self.path != []:
            current = self.location
            next = self.path.pop()
            if next[1] < current[1]:
                self.movement_points[0] = self.tile_size
            elif next[0] > current[0]:
                self.movement_points[1] = self.tile_size
            elif next[1] > current[1]:
                self.movement_points[2] = self.tile_size
            elif next[0] < current[0]:
                self.movement_points[3] = self.tile_size
            self.movement_cooldown = 0.0     

        #the amount required to decrease movement_points each cycle
        #so that one whole tile is travelled in the time between setting movement points (above)
        s = self.tile_size / (self.movement_limit * 100) 

        if self.movement_points[0] > 0:
            self.move(0, -s)
            self.modify_movement_points(0, -s)
        elif self.movement_points[1] > 0:
            self.move(s, -0)
            self.modify_movement_points(1, -s)
        elif self.movement_points[2] > 0:
            self.move(0, s)
            self.modify_movement_points(2, -s)
        elif self.movement_points[3] > 0:
            self.move(-s, 0)
            self.modify_movement_points(3, -s)

    def modify_movement_points(self, i, modifier):
        if self.movement_points[i] != 0:
            self.movement_points[i] += modifier
        else:
            pass

    def open_inventory(self):
        pass

class Player(Entity):
    def __init__(self, image):
        Entity.__init__(self, image)
