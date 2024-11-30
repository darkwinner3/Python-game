import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, world_x, world_y, size, is_Spawned, animation_data = None):
        super().__init__()
        # self.sprite = pygame.image.load(sprite_image)
        # self.sprite = pygame.transform.scale(self.sprite, size)
        # self.rect = self.sprite.get_rect(topleft=(world_x, world_y))
        # self.direction = pygame.math.Vector2(0, 0)
        
        self.sprite_size = size
        self.sprite = pygame.Surface(size)
        self.rect = self.sprite.get_rect(topleft=(world_x, world_y))
        
        self.health = 1000
        
        self.dash_length = 50
        self.is_dashed = False
        self.dash_cooldown = 0
        self.dash_timer = 0
        self.dash_duration = 20
        self.dash_increment = 0
        
        self.speed = 10
        
        self.gravity = 0.5
        self.jump_speed = 15
        self.max_jumps = 2
        self.jumpCounter = 0
        self.on_ground = False
        self.jumping = False
        
        self.x = x
        self.y = y
        self.world_x = world_x
        self.world_y = world_y
        
        self.direction = pygame.Vector2(0, 0)
        self.animation_frames = []
        self.current_frame = 0
        self.animation_rate = 1
        self.animtaion_counter = 0
        self.animation_mode = "Loop"
        
        if animation_data:
            self.load_animation(animation_data)
        
        self.is_Spawned = is_Spawned
    
    def load_animation(self, animation_data):
        self.animation_frames = []
        tileset = pygame.image.load(animation_data["tileset_path"]).convert_alpha()
        
        for frame in animation_data["frames"]:
            x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
            frame_surface = pygame.Surface((w, h), pygame.SRCALPHA)
            frame_surface.blit(tileset, (0, 0), (x, y, w, h))
            self.animation_frames.append(frame_surface)
            
        self.animation_rate = animation_data["rate"]
        self.animation_mode = animation_data["mode"]
        
        self.animation_frames = [
            pygame.transform.scale(frame, self.sprite_size) for frame in self.animation_frames
        ]
        
        if self.animation_frames:
            self.sprite = self.animation_frames[0]
    
    def update_animation(self):
        if self.animation_frames:
            self.animtaion_counter += 1
            if self.animtaion_counter >= self.animation_rate:
                self.animtaion_counter = 0
                self.current_frame += 1
                
                if self.current_frame >= len(self.animation_frames):
                    if self.animation_mode == "Loop":
                        self.current_frame = 0
                    else:
                        self.current_frame = len(self.animation_frames) - 1
                
                self.sprite = self.animation_frames[self.current_frame]
                
    # Movement
    def moveLeft(self):
        if self.dash_timer > 0:
            self.direction.x = -self.dash_increment
            self.dash_timer -= 1
        else:
            self.direction.x = -1
            if self.is_dashed and self.dash_cooldown <= 0:
                self.start_dash(-1)
        
    def moveRight(self):
        if self.dash_timer > 0:
            self.direction.x = self.dash_increment
            self.dash_timer -= 1
        else:
            self.direction.x = 1
            if self.is_dashed and self.dash_cooldown <= 0:
                self.start_dash(1)
    
    def start_dash(self, direction):
        self.dash_timer = self.dash_duration
        self.dash_increment = self.dash_length / self.dash_duration
        self.direction.x = direction * self.dash_increment
        print(self.is_dashed)
        self.is_dashed = False
        self.dash_cooldown = 80
       
    def jump(self):
        if self.on_ground:
            self.direction.y = -self.jump_speed
            self.jumpCounter = 1
            self.on_ground = False
            self.jumping = True
        elif self.jumpCounter < self.max_jumps:
            self.direction.y = -self.jump_speed
            self.jumpCounter += 1
            self.jumping = True
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.moveRight()
        elif keys[pygame.K_LEFT]:
            self.moveLeft()
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not self.jumping:
                self.jump()
        elif not keys[pygame.K_SPACE] and not keys[pygame.K_UP]:
            self.jumping = False
        
        if keys[pygame.K_LSHIFT]:
            self.is_dashed = True
        elif not keys[pygame.K_LSHIFT]:
            self.is_dashed = False
        
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        
    def vertical_movement_collision(self, tiles):
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:  # Moving down
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                    self.jumpCounter = 0
                elif self.direction.y < 0:  # Moving up
                    self.rect.top = tile.rect.bottom
                self.direction.y = 0
            if self.on_ground and self.direction.y > 1 or self.direction.y < 0:
                self.on_ground = False
        
    
    def horizontal_movement_collision(self, tiles):
        self.rect.x += self.direction.x * self.speed
        
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left
                elif self.direction.x < 0:
                    self.rect.left = tile.rect.right
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def update(self):
        self.handle_input()
        self.update_animation()
    
    def draw(self, canvas, camera):
        canvas.blit(self.sprite, self.rect.move(camera))
    
    