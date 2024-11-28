import pygame, sys, json
from pygame.locals import*
from menu.menu import Menu
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
        
        self.game_paused = False
        self.menu_state = "main"
        
        self.screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.display = pygame.Surface((DISPLAY_W, DISPLAY_H), pygame.SRCALPHA)
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()

        # menu
        self.menu = Menu(DISPLAY_W, DISPLAY_H)
        
        # level init
        self.level = World(self.screen, self.display, self.level_data)
        
            
    def run(self):
        while True:
            
            if self.game_paused == True:
                if self.menu_state == "main":
                    self.screen.fill((0, 0, 0))
                    if self.menu.resume_button.draw(self.screen):
                        self.game_paused = False
                    if self.menu.options_button.draw(self.screen):
                        self.menu_state = "options"
                    if self.menu.quit_button.draw(self.screen):
                        pygame.quit()
                        sys.exit()
                if self.menu_state == "options":
                    self.screen.fill((0, 0, 0))
                    if self.menu.video_button.draw(self.screen):
                        print("nothing")
                    if self.menu.audio_button.draw(self.screen):
                        print("nothing")
                    if self.menu.keys_button.draw(self.screen):
                        print("nothing")
                    if self.menu.back_button.draw(self.screen):
                        self.menu_state = "main"
            else:
                self.level.run()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_paused = True
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
            
                
                
            pygame.display.update()
                
            # fps control
            self.fpsClock.tick(self.FPS)


Game().run()
 