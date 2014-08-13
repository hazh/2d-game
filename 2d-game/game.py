#!/usr/bin/env python

try:
    import os
    import sys
    import math
    import random
    import pygame
    from pygame.locals import *
    import screen
    import camera
    import world as WORLD
    import entity
    import item
    import helpers
    import pathfinder
except ImportError, err:
    print "cannot load module(s)!",
    sys.exit(2)

#####
#
# group.draw() draws each sprite to surface at the sprite's rect
# blit() draws surface onto other surface
#
# do i want to create an background image composed of all tiles and blit() that to screen?
# or add each tile to a group and draw() the group?
#
# it comes down to how scrolling is handled. Do i create a camera class?
# how does the camera ony render a certain area of the map, (its viewport), is this a rect?



# implement draw method for entities
# check whether entity collides with current viewport
# if so draw them
# entity location needs to be tracked independantly in order to do this


#
#####

class Game(object):
    
    def __init__(self):
        #set physics variables
        self.clock = pygame.time.Clock()
        self.__physics_FPS = 100.0
        self.__dt = 1.0 / self.__physics_FPS
        self.time_current = self.get_time()
        self.accumulator = 0.0
        #set program variables    
        self.tile_size = 32
        self.name = "2d-game"

    def load(self):
        #initialise objects
        self.screen = screen.Screen((1280, 720), self.name)
        self.camera = camera.Camera((1280, 720))
        self.images = helpers.Image()
        tile_images = {
            "tile_grass": self.images.tile_grass,
            "tile_dirt": self.images.tile_dirt,
            "tile_wall": self.images.tile_wall
        }

        world = WORLD.World("level.map", tile_images)
        player = entity.Player(self.images.player)
        self.entities = pygame.sprite.Group(player)
        self.objects = dict(world=world, player=player)
        self.path_finder = pathfinder.PathFinder(world.nodes)

    def get_time(self):
        #returns time passed in seconds
        return float(pygame.time.get_ticks()) / 1000.0

    def handle_input(self):
        dt = self.__dt
        player = self.objects["player"]
        world = self.objects["world"]
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_location = self.get_mouse_location(mouse_position)
                self.set_entity_path(player, mouse_location)
        for direction, rect in self.camera.scroll_rects.items():
            if rect.collidepoint(mouse_position) and self.camera.is_scrollable(direction, (world.width, world.height)):
                self.camera.move(direction)

    def get_mouse_location(self, mouse_position):
        x = (self.camera.left + mouse_position[0]) / self.tile_size
        y = (self.camera.top + mouse_position[1]) / self.tile_size
        return (x, y)

    def set_entity_path(self, entity, goal):
        start = entity.location
        try:
            path = self.path_finder.find(start, goal)
            entity.path = path
        except:
            pass

    def update(self, dt):
        self.handle_input()
        #call update method for all entities
        self.entities.update(dt, self.camera.viewport)  
        
    def render(self):
        bg = self.objects["world"].image.copy()
        self.entities.draw(bg)
        self.screen.surface.blit(bg, bg.get_rect(), self.camera.viewport)
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
