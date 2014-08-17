#!/usr/bin/env python

try:
    import os
    import sys
    import pygame    
    import helpers
    import widget
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)

class Combat(object):

    def __init__(self, entity1, entity2):
        self.entity1 = entity1
        self.entity2 = entity2

    def fight(self):

        ######  SEND MODIFERS TO TARGET RENDER METHOD TO ADD TO CONTAINER 




        weapon1 = self.entity1.hand.get()
        weapon1.use(self.entity2)   
        weapon2 = self.entity2.hand.get()
        weapon2.use(self.entity1)
        
        self.entity1.append_notifications(str(weapon2.use_modifier)) 

        if self.entity1.hp <= 0:
            self.entity1.die()
            self.entity2.combat = None
        if self.entity2.hp <= 0:
            self.entity2.die()
            self.entity1.combat = None