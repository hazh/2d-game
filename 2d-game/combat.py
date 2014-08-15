#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import helpers
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

class Combat(object):

    def __init__(self, entity1, entity2):
        self.entity1 = entity1
        self.entity2 = entity2

    def fight(self):
        self.entity1.hand.get().use(self.entity2)
        self.entity2.hand.get().use(self.entity1)

        if self.entity1.hp <= 0:
            self.entity1.die()
            self.entity2.combat = None
        if self.entity2.hp <= 0:
            self.entity2.die()
            self.entity1.combat = None

        print "fight!"