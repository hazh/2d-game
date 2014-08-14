#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import container 
    import helpers
    import widget
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

class Console(object):

    def __init__(self):
        self.container = container.ScrollingContainer(10, 410, 500, 300)

    def log(self, text):
        self.container.append(widget.Label("> " + text, 0, 0))  

    def draw(self, surface):
        self.container.draw(surface)