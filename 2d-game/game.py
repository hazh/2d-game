#!/usr/bin/env python

try:
    import os
    import sys
    import math
    import random
    import pygame
    from pygame.locals import *
    import camera
    import console
    import entity
    import helpers
    import item
    import pathfinder
    import screen
    import widget
    import world as WORLD
except ImportError, err:
    print "cannot load module(s)!",
    sys.exit(2)

pygame.init()
SCREEN = screen.Screen((1280, 720), "2d-game")
IMAGES = helpers.Image()

class Game(object):
    
    def __init__(self):
        #set physics variables
        self.clock = pygame.time.Clock()
        self.__physics_FPS = 100.0
        self.__dt = 1.0 / self.__physics_FPS
        self.time_current = self.get_time()
        self.accumulator = 0.0   
        self.tile_size = 32 
        self.camera = camera.Camera((1280, 720))
        tile_images = {
            "tile_grass": IMAGES.tile_grass,
            "tile_dirt": IMAGES.tile_dirt,
            "tile_wall": IMAGES.tile_wall
        }
        world = WORLD.World("level.map", tile_images)
        self.path_finder = pathfinder.PathFinder(world.nodes)
        player = entity.Player(IMAGES.player)
        dummy = entity.Entity(IMAGES.player, spawn_location = (16, 2))
        self.entities = pygame.sprite.Group(player, dummy)
        self.objects = dict(world=world, player=player, dummy=dummy)

        self.console = console.Console()

        k = item.Key(IMAGES.key)
        player.hand.add(k)

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
                self.console.log("location: "+ str(mouse_location))
                self.click_router(mouse_location)
        for direction, rect in self.camera.scroll_rects.items():
            if rect.collidepoint(mouse_position) and self.camera.is_scrollable(direction, (world.width, world.height)):
                self.camera.move(direction)

    def get_mouse_location(self, mouse_position):
        x = (self.camera.left + mouse_position[0]) / self.tile_size
        y = (self.camera.top + mouse_position[1]) / self.tile_size
        return (x, y)

    def click_router(self, location):
        target, type = self.get_target(location)
        if type == "entity" and self.objects["player"].location in self.path_finder.neighbours(location):
            self.objects["player"].initiate_combat(target)
        elif target == True and type == "tile": #checks if target is not wall. if it is a wall, returns target = False
            self.set_entity_path(self.objects["player"], location)

    def get_target(self, location):
        for entity in self.entities:
            if entity.location == location:
                return entity, "entity"
        world = self.objects["world"]
        if world.nodes[location].is_traversable():
            return True, "tile"
        else:
            return False, "tile"

    def set_entity_path(self, entity, goal):
        start = entity.location
        path = self.path_finder.find(start, goal)
        entity.path = path

    def update(self, dt):
        self.handle_input()
        #call update method for all entities
        self.entities.update(dt)  
        
    def render(self):
        bg = self.objects["world"].image.copy()
        self.entities.draw(bg)
        SCREEN.surface.blit(bg, bg.get_rect(), self.camera.viewport)
        self.objects["player"].render(SCREEN.surface)
        self.console.draw(SCREEN.surface)
        pygame.display.update()

    def play(self):
        pygame.font.init()
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
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
