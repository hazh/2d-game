#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

class Widget(object):

    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = x, y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Label(Widget, pygame.font.Font):

    def __init__(self, text, x, y):
        f = None
        pygame.font.Font.__init__(self, f, 15)
        self.surface = self.render(text, True, (255,255,255), (0,0,0))
        Widget.__init__(self, self.surface, x, y)