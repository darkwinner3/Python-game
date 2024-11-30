import pygame, sys
from menu.button import Button

class Menu():
    def __init__(self, display_width, display_height, screen, display, game, level):
        TEXT_COL = (255, 255, 255)

        self.level = level
        self.game = game
        self.screen = screen
        self.display = display
        self.display_width, self.display_height = (display_width, display_height)
        self.game_paused = False
        self.menu_state = "main"
        self.scroll_offset = 0
        self.max_visible_buttons = 5
        self.scroll_step = 1
        
        # self.menu_change_cooldown = 0
        
        
        self.font = pygame.font.Font("C:\WINDOWS\FONTS\ARIAL.TTF", 40)

        # main menu settings img
        self.resume_img = pygame.image.load("data/pictures/resume.png").convert_alpha()
        self.options_img = pygame.image.load("data/pictures/options.png").convert_alpha()
        self.quit_img = pygame.image.load("data/pictures/quit.png").convert_alpha()
        self.video_img = pygame.image.load("data/pictures/video.png").convert_alpha()
        self.audio_img = pygame.image.load("data/pictures/audio.png").convert_alpha()
        self.keys_img = pygame.image.load("data/pictures/keys.png").convert_alpha()
        self.back_img = pygame.image.load("data/pictures/back.png").convert_alpha()
        self.levels_img = pygame.image.load("data/pictures/Levels.png").convert_alpha()
        
        # resolutions img
        self.standardVGA_img = pygame.image.load("data/pictures/640x480.png").convert_alpha()
        self.standardSuperVGA_img = pygame.image.load("data/pictures/800x600.png").convert_alpha()
        self.hd_img = pygame.image.load("data/pictures/1280x720.png").convert_alpha()
        self.fullHD_img = pygame.image.load("data/pictures/1920x1080.png").convert_alpha()
        
        # levels img
        self.level1_img = pygame.image.load("data/pictures/level1.png").convert_alpha()
        self.level2_img = pygame.image.load("data/pictures/level2.png").convert_alpha()
        self.level3_img = pygame.image.load("data/pictures/level3.png").convert_alpha()
        self.level4_img = pygame.image.load("data/pictures/level4.png").convert_alpha()
        self.level5_img = pygame.image.load("data/pictures/level5.png").convert_alpha()
        self.level6_img = pygame.image.load("data/pictures/level6.png").convert_alpha()
        self.level7_img = pygame.image.load("data/pictures/level7.png").convert_alpha()
        self.level8_img = pygame.image.load("data/pictures/level8.png").convert_alpha()
        self.level9_img = pygame.image.load("data/pictures/level9.png").convert_alpha()
        self.level10_img = pygame.image.load("data/pictures/level10.png").convert_alpha()
        self.level11_img = pygame.image.load("data/pictures/level11.png").convert_alpha()
        self.level12_img = pygame.image.load("data/pictures/level12.png").convert_alpha()

        button_width, button_height = self.resume_img.get_size()
        
        # buttons location
        x = (self.display_width - button_width) // 2 + 30
        y = (self.display_height - button_height) // 2 - 100
        
        # menu buttons
        self.menus = {
            "main": {
                "resume": Button(x, y - 150, self.resume_img, 1),
                "levels": Button(x, y, self.levels_img, 1),
                "options": Button(x, y + 150, self.options_img, 1),
                "quit": Button(x, y + 450, self.quit_img, 1),
            },
            "options": {
                "video": Button(x, y - 150, self.video_img, 1),
                "audio": Button(x, y, self.audio_img, 1),
                "keys": Button(x, y + 150, self.keys_img, 1),
                "back": Button(x, y + 300, self.back_img, 1),
            },
            "video": {
                "standardVGA": Button(x, y - 150, self.standardVGA_img, 1),
                "standardSuperVGA": Button(x, y, self.standardSuperVGA_img, 1),
                "hd": Button(x, y + 150, self.hd_img, 1),
                "fullHD": Button(x, y + 300, self.fullHD_img, 1),
                "back": Button(x, y + 450, self.back_img, 1),
            },
            "levels": {
                "level1": Button(x, y, self.level1_img, 1),
                "level2": Button(x, y, self.level2_img, 1),
                "level3": Button(x, y, self.level3_img, 1),
                "level4": Button(x, y, self.level4_img, 1),
                "level5": Button(x, y, self.level5_img, 1),
                "level6": Button(x, y, self.level6_img, 1),
                "level7": Button(x, y, self.level7_img, 1),
                "level8": Button(x, y, self.level8_img, 1),
                "level9": Button(x, y, self.level9_img, 1),
                "level10": Button(x, y, self.level10_img, 1),
                "level11": Button(x, y, self.level11_img, 1),
                "level12": Button(x, y, self.level12_img, 1),
                
            }
        }
    
    def run(self, screen):
        if self.game_paused:
            screen.fill((0, 0, 0))  # Clear the screen at the start

            # if self.menu_change_cooldown > 0:
            #     self.menu_change_cooldown -= 1
            #     return
            
            if self.menu_state == "levels":
                self.handle_scroll_input()
                self.draw_levels_menu(screen)
            else:
                # Get the current menu's buttons dynamically
                current_menu_buttons = self.menus.get(self.menu_state, {})

                # Iterate over the buttons in the current menu
                for button_name, button in current_menu_buttons.items():
                    if button.draw(screen):
                        self.handle_button_click(button_name)
            

    def get_visible_buttons(self):
        start_index = self.scroll_offset
        end_index = start_index + self.max_visible_buttons
        
        visible_buttons = list(self.menus["levels"].items())[start_index:end_index]
        return visible_buttons

    def handle_scroll_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.scroll_offset > 0:
            self.scroll_offset -= self.scroll_step
        elif keys[pygame.K_DOWN] and self.scroll_offset < len(self.menus["levels"]) - self.max_visible_buttons:
            self.scroll_offset += self.scroll_step
            
    def draw_levels_menu(self, screen):
        visible_buttons = self.get_visible_buttons()
        
        x, y = (self.display_width // 2 - 150, 200)
        spacing = 150
        
        back_button = Button(x + 550, y + 700, self.back_img, 1)
        
        for button_name, button in visible_buttons:
            button.rect.topleft = (x, y)
            if button.draw(screen):
                self.handle_button_click(button_name)
            y += spacing
        
        if back_button.draw(screen):
                self.menu_state = "main"
    
    def update_resolution(self, width, height, screen):
        self.display_width = width
        self.display_height = height
        self.screen = screen
        
        button_width = 100  # Example button width
        button_height = 50  # Example button height

        # Recalculate positions for each menu
        for menu_name, buttons in self.menus.items():
            for button_name, button in buttons.items():
                # Calculate the new x and y positions
                if menu_name == "main":
                    base_y = (self.display_height - button_height) // 2 - 100
                    offsets = {
                        "resume": -150,
                        "levels": 0,
                        "options": 150,
                        "quit": 450,
                    }
                    y = base_y + offsets.get(button_name, 0)
                elif menu_name == "options":
                    base_y = (self.display_height - button_height) // 2 - 100
                    offsets = {
                        "video": -150,
                        "audio": 0,
                        "keys": 150,
                        "back": 300,
                    }
                    y = base_y + offsets.get(button_name, 0)
                elif menu_name == "video":
                    base_y = (self.display_height - button_height) // 2 - 100
                    offsets = {
                        "standardVGA": -150,
                        "standardSuperVGA": 0,
                        "hd": 150,
                        "fullHD": 300,
                        "back": 450,
                    }
                    y = base_y + offsets.get(button_name, 0)
                elif menu_name == "levels":
                    # Special case for scrolling menu
                    base_y = (self.display_height - button_height) // 2 - 100
                    y = base_y  # Default base Y for level buttons
                    # Add logic here if levels require unique positions

                # Calculate x position
                x = (self.display_width - button_width) // 2 + 30

                # Update the button position
                button.rect.topleft = (x, y)
                
    def get_clicked_level(self, levelID):
        chosen_level = self.level.get_level_by_id(levelID)
        
        self.level.current_level = chosen_level
        
        print(f"Current level after change: {self.level.current_level['identifier']}")
        print(f"Current level after change: {chosen_level['identifier']}")
        self.level.player_data = None
        
        self.level.player = pygame.sprite.GroupSingle()
        
        self.level.load_level(chosen_level, self.display)
        

    def handle_button_click(self, button_name):
        if self.menu_state == "main":
            if button_name == "resume":
                self.game_paused = False
            elif button_name == "levels":
                self.menu_state = "levels"
            elif button_name == "options":
                self.menu_state = "options"
            elif button_name == "quit":
                pygame.quit()
                sys.exit()

        elif self.menu_state == "options":
            if button_name == "video":
                self.menu_state = "video"
            elif button_name == "audio":
                print("Audio settings")
            elif button_name == "keys":
                print("Key bindings")
            elif button_name == "back":
                self.menu_state = "main"

        elif self.menu_state == "video":
            if button_name == "standardVGA":
                self.game.change_screen_size(640, 480)
            elif button_name == "standardSuperVGA":
                self.game.change_screen_size(800, 600)
            elif button_name == "hd":
                self.game.change_screen_size(1280, 720)
            elif button_name == "fullHD":
                self.game.change_screen_size(1920, 1080)
            elif button_name == "back":
                self.menu_state = "options"
        
        elif self.menu_state == "levels":
            if button_name == "level1":
                self.get_clicked_level("Level_1")
            elif button_name == "level2":
                self.get_clicked_level("Level_2")
            elif button_name == "level3":
                self.get_clicked_level("Level_3")
            elif button_name == "level4":
                self.get_clicked_level("Level_4")
            elif button_name == "level5":
                self.get_clicked_level("Level_5")
            elif button_name == "level6":
                self.get_clicked_level("Level_6")
            elif button_name == "level7":
                self.get_clicked_level("Level_7")
            elif button_name == "level8":
                self.get_clicked_level("Level_8")
            elif button_name == "level9":
                self.get_clicked_level("Level_9")
            elif button_name == "level10":
                self.get_clicked_level("Level_10")
            elif button_name == "level11":
                self.get_clicked_level("Level_11")
            elif button_name == "level12":
                self.get_clicked_level("Level_0")
            
                
        
        # self.menu_change_cooldown = 10
                    
    def draw_text(text, font, text_col, x, y, screen):
            img = font.render(text, font, text_col, x, y)
            screen.blit(img, (x, y))