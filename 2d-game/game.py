#!/usr/bin/env python

try:
    import os
    import sys
    import math
    import random
    import pygame
    from pygame.locals import *
    import world as WORLD
    import player as PLAYER
    import helpers
    import pathfinder
except ImportError, err:
    print "cannot load module(s)!",
    sys.exit(2)

class Game:
    
    def __init__(self):
        #set physics variables
        self.clock = pygame.time.Clock()
        self.__physics_FPS = 100.0
        self.__dt = 1.0 / self.__physics_FPS
        self.time_current = self.get_time()
        self.accumulator = 0.0
        #set program variables
        self.screen_size = (1280, 720)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.tile_size = 32
        self.name = "2d-game"
        self.font = pygame.font.SysFont("monospace", 15)
        #game variables
       
    def load(self):
        self.screen.fill((0, 0, 0))
        pygame.display.set_caption(self.name)
        #initialise objects
        world = WORLD.World("level.map", "key.txt", self.tile_size)
        player = PLAYER.Player(self.tile_size)
        self.entities = pygame.sprite.Group(player)
        self.objects = dict(world=world, player=player)
        
        self.path_finder = pathfinder.PathFinder(world.map)
        self.move()

    def get_time(self):
        #returns time passed in seconds
        return float(pygame.time.get_ticks()) / 1000.0

    def handle_input(self):
        dt = self.__dt
        player = self.objects["player"]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_position = pygame.mouse.get_pos()
                mouse_location = self.get_mouse_location(mouse_position)
                player.set_movement_points("right")

    def get_mouse_location(self, mouse_position):
        x = self.objects["world"].rect.left + mouse_position[0]
        y = self.objects["world"].rect.top + mouse_position[1]
        return (x, y)

    def handle_movement(self):
        player = self.objects["player"]
        s = self.tile_size / (player.movement_limit * 100)
        if player.get_movement_points(0) > 0:
            self.objects["world"].rect.top += s
            player.modify_movement_points(0, -s)
        if player.get_movement_points(1) > 0:
            self.objects["world"].rect.left -= s
            player.modify_movement_points(1, -s)
        if player.get_movement_points(2) > 0:
            self.objects["world"].rect.top -= s
            player.modify_movement_points(2, -s)
        if player.get_movement_points(3) > 0:
            self.objects["world"].rect.left += s
            player.modify_movement_points(3, -s)


    def move(self):
        start, goal = (1,1), (7,8)
        print self.path_finder.find(start, goal)

    def update(self):
        self.handle_input()
        self.handle_movement()
        #call update method for all entities
        self.entities.update()  
        for entity in self.entities:
            #update player location relative to map
            entity.location[0] = entity.position[0] - self.objects["world"].rect.left
            entity.location[1] = entity.position[1] - self.objects["world"].rect.top
        
    def render(self):
        self.screen.blit(self.objects["world"].image, self.objects["world"].rect)
        pygame.display.update()

    def play(self):
        self.load()
        dt = self.__dt
        while True:
            time_new = self.get_time()
            time_frame = time_new - self.time_current
            if time_frame > 0.25:
                time_frame = 0.25
            self.accumulator += time_frame
            self.time_current = time_new        
            #update
            while self.accumulator >= dt:
                self.update()
                self.accumulator -= dt
            #render
            self.render()

def main():
    pygame.init()
    game = Game()
    game.play()

if __name__ == "__main__":
    main()


##########################
when pathfinder looks for neighbours it trys to match 2 length tuples to 3 length tuples
how can i match the coordinates of a neighbour back to the 3 length tuple which contains additional information
maybe try to match tile[x] and tile[y]