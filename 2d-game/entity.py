#!/usr/bin/env python

try:
    import os
    import sys
    import pygame
    import combat
    import container
    import helpers    
    import inventory
    import item
    import widget
except ImportError, err:
    print "cannot load module(s)"
    sys.exit(2)  

class Entity(pygame.sprite.Sprite):
    
    def __init__(self, image, spawn_location = (1, 1), tile_size = 32):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.tile_size = tile_size
        self.rect.left, self.rect.top = spawn_location[0] * tile_size, spawn_location[1] * tile_size
        self.location = spawn_location
        self.location_counter = [0, None]
        self.path = []
        self.movement_cooldown = 0.0
        self.movement_limit = 0.16
        self.movement_points = [0, 0, 0, 0] #up, right, down, left:

        #the amount required to decrease movement_points each cycle
        #so that one whole tile is travelled in the time between setting movement points (above)
        self.s = self.tile_size / (self.movement_limit * 100) 


        self.hp = 100.0
        self.hp_max = 100.0
        self.combat = None
        self.combat_cooldown = 0.0

        self.hand = inventory.Hand()
        
    def update(self, dt):
        if self.combat != None and self.combat_cooldown == 0.0:
            self.combat_cooldown = 250.0
            self.combat.fight()
        elif self.combat_cooldown > 0.0:
            self.combat_cooldown -= 2.0
        self.update_status()
        self.handle_movement(dt)

    def move(self, dir):
        if dir == "up":
            self.rect.move_ip(0, -self.s)
        elif dir == "right":
            self.rect.move_ip(self.s, 0)
        elif dir == "down":
            self.rect.move_ip(0, self.s)
        elif dir == "left":
            self.rect.move_ip(-self.s, 0)
        self.location_counter[0] += self.s
        self.location_counter[1] = dir
        if self.location_counter[0] == 32.0:
            temp = list(self.location)
            if dir == "up":
                temp[1] -= 1
            elif dir == "right":
                temp[0] += 1
            elif dir == "down":
                temp[1] += 1
            elif dir == "left":
                temp[0] -= 1
            self.location = tuple(temp)
            self.location_counter[0] = 0

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

        if self.movement_points[0] > 0:
            self.move("up")
            self.modify_movement_points(0, -self.s)
        elif self.movement_points[1] > 0:
            self.move("right")
            self.modify_movement_points(1, -self.s)
        elif self.movement_points[2] > 0:
            self.move("down")
            self.modify_movement_points(2, -self.s)
        elif self.movement_points[3] > 0:
            self.move("left")
            self.modify_movement_points(3, -self.s)

    def modify_movement_points(self, i, modifier):
        if self.movement_points[i] != 0:
            self.movement_points[i] += modifier
        else:
            pass

    def modify_hp(self, modifier):
        self.hp += modifier

    def update_status(self):
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        elif self.hp <= 0:
            self.die()

    def die(self):
        self.kill()

    def initiate_combat(self, target):
        if self.combat == None:
            self.combat = combat.Combat(self, target)

class Player(Entity):
    def __init__(self, image):
        Entity.__init__(self, image)

    def render(self, surface):
        inv = widget.Label(self.hand.__str__(), 10, 40)
        pygame.draw.rect(surface, (255, 0, 0), (70, 10, self.hp, inv.get_linesize()))
        pygame.draw.rect(surface, (0, 0, 0), (70 + self.hp, 10, self.hp_max - self.hp, inv.get_linesize()))
        hp = widget.Label("hp: " + str(self.hp), 10, 12)
        info = container.Container(0, 0, 200, 200, inv, hp)
        info.draw(surface)

