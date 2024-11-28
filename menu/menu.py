import pygame
from menu.button import Button


class Menu():
    def __init__(self, display_width, display_height):
        TEXT_COL = (255, 255, 255)

        self.font = pygame.font.Font("C:\WINDOWS\FONTS\ARIAL.TTF", 40)

        self.resume_img = pygame.image.load("data/pictures/resume.png").convert_alpha()
        self.options_img = pygame.image.load("data/pictures/options.png").convert_alpha()
        self.quit_img = pygame.image.load("data/pictures/quit.png").convert_alpha()
        self.video_img = pygame.image.load("data/pictures/video.png").convert_alpha()
        self.audio_img = pygame.image.load("data/pictures/audio.png").convert_alpha()
        self.keys_img = pygame.image.load("data/pictures/keys.png").convert_alpha()
        self.back_img = pygame.image.load("data/pictures/back.png").convert_alpha()

        button_width, button_height = self.resume_img.get_size()
        
        x = (display_width - button_width) // 2 + 30
        y = (display_height - button_height) // 2 - 100
        
        self.resume_button = Button(x, y - 150, self.resume_img, 1)
        self.options_button = Button(x, y, self.options_img, 1) 
        self.quit_button = Button(x, y + 150, self.quit_img, 1)
        self.video_button = Button(x, y - 150, self.video_img, 1)
        self.audio_button = Button(x, y, self.audio_img, 1) 
        self.keys_button = Button(x, y + 150, self.keys_img, 1)
        self.back_button = Button(x, y + 300, self.back_img, 1)

    def draw_text(text, font, text_col, x, y, screen):
        img = font.render(text, font, text_col, x, y)
        screen.blit(img, (x, y))
    
    