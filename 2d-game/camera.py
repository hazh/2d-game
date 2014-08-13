#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

class Camera(pygame.Rect):
    def __init__(self, size):
        self.left = 0
        self.top = 0
        self.width, self.height = size
        self.rect_size = 20
        self.scroll_rects = {
            "up": pygame.Rect((0, 0), (size[0], self.rect_size)),
            "right": pygame.Rect((size[0]-self.rect_size, 0), (self.rect_size, size[1])),
            "down": pygame.Rect((0, size[1]-self.rect_size), (size[0], self.rect_size)),
            "left": pygame.Rect((0, 0), (self.rect_size, size[1]))
        }

    @property
    def viewport(self):
        return [self.left, self.top, self.width, self.height]

    def move(self, direction):
        if direction == "up":
            self.top -= 4
        if direction == "right":
            self.left += 4
        if direction == "down":
            self.top += 4
        if direction == "left":
            self.left -= 4

    def is_scrollable(self, direction, world_size):
        if direction == "up" and self.top <= 0:
            return False
        if direction == "right" and self.left >= world_size[0] - self.width:
            return False
        if direction == "down" and self.top >= world_size[1] - self.height:
            return False
        if direction == "left" and self.left <= 0:
            return False
        return True
        