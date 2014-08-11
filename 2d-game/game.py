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

class Game(object):
    
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
        world = WORLD.World("level.map", self.tile_size)
        player = PLAYER.Player(self.tile_size)
        self.entities = pygame.sprite.Group(player)
        self.objects = dict(world=world, player=player)
        
        self.path_finder = pathfinder.PathFinder(world.map)

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
                self.move_entity(player, mouse_location)

    def get_mouse_location(self, mouse_position):
        x = (self.objects["world"].rect.left + mouse_position[0]) / self.tile_size
        y = (self.objects["world"].rect.top + mouse_position[1]) /self.tile_size
        return (x, y)

    def move_entity(self, entity, goal):
        start = entity.location
        path = self.path_finder.find(start, goal)
        entity.path = path

    def update(self, dt):
        self.handle_input()
        #call update method for all entities
        self.entities.update(dt)  
        
    def render(self):
        dirty_tiles = self.objects["world"].tiles.draw(self.screen)
        dirty_entities = self.entities.draw(self.screen)
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
                self.update(dt)
                self.accumulator -= dt
            #render
            self.render()

def main():
    pygame.init()
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
