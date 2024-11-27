import pygame, sys, json
from pygame.locals import*
from player import Player
from world import World
from tile import *

class Game():
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        pygame.display.set_caption('Game')
        DISPLAY_W, DISPLAY_H = 1920, 1080

        with open("level1-map.json") as f:
            self.level_data = json.load(f)
        f.close()
        
        self.screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.display = pygame.Surface((DISPLAY_W, DISPLAY_H), pygame.SRCALPHA)
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()

        # level init
        self.level = World(self.screen, self.display)
        
            
    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.level.run()
                
                
            pygame.display.update()
                
            # fps control
            self.fpsClock.tick(self.FPS)


Game().run()
 