#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  

class Screen(object):
    def __init__(self, size, caption):
        self.size = size
        self.surface = pygame.display.set_mode(size)
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect()
        pygame.display.set_caption(caption)
        self.font = pygame.font.SysFont("monospace", 15)