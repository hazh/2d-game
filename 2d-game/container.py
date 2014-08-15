#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

class Container(object):

    def __init__(self, x, y, width, height, *widgets):
        self.widgets = list(widgets)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.left, self.rect.top = x, y

    def draw(self, surface):
        for widget in self.widgets:
            widget.draw(self.surface)
        surface.blit(self.surface, self.rect)

class ScrollingContainer(Container):

    def __init__(self, x, y, width, height, *widgets):
        temp_widgets = list(widgets)
        top = height
        for widget in temp_widgets:
            widget.rect.top = top
            top -= 20
            print widget.rect.top
        widgets = tuple(temp_widgets)
        Container.__init__(self, x, y, width, height, *widgets)

    def append(self, widget):
        if len(self.widgets) > 15:
            self.widgets.pop()
        for w in self.widgets:
            w.rect.top -= 20
        widget.rect.top = self.rect.height -12
        self.widgets.append(widget)