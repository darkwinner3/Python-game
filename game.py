import pygame, sys, json, os
from pygame.locals import*
from menu.menu import Menu
from world import World
from tile import *
os.environ['SDL_VIDEO_CENTERED'] = '1'


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
        self.level = World(self.screen, self.display, self.level_data)
        
        # menu
        self.menu = Menu(DISPLAY_W, DISPLAY_H, self.screen, self.display, self, self.level)
    
    def change_screen_size(self, width, height):
        # Update screen and display
        self.DISPLAY_W, self.DISPLAY_H = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.display = pygame.Surface((width, height), pygame.SRCALPHA)

        # Notify other components
        self.menu.update_resolution(width, height, self.screen)
        self.level.update_resolution(width, height, self.screen)   
            
    def run(self):
        while True:
            
            if self.menu.game_paused:
                self.menu.run(self.screen)
            else:
                self.level.run()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.menu.menu_state = "main"
                    self.menu.game_paused = not self.menu.game_paused
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0 and self.menu.scroll_offset > 0:
                        self.menu.scroll_offset -= self.menu.scroll_step
                    elif event.y < 0 and self.menu.scroll_offset < len(self.menu.menus["levels"]) - self.menu.max_visible_buttons:
                        self.menu.scroll_offset += self.menu.scroll_step
                if event.type == pygame.VIDEORESIZE:
                    new_width, new_height = event.w, event.h
                    self.change_screen_size(new_width, new_height)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
            
                
                
            pygame.display.update()
                
            # fps control
            self.fpsClock.tick(self.FPS)


Game().run()
 