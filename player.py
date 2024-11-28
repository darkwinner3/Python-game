import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, world_x, world_y, sprite_image, size, is_Spawned):
        super().__init__()
        self.sprite = pygame.image.load(sprite_image)
        self.sprite = pygame.transform.scale(self.sprite, size)
        self.rect = self.sprite.get_rect(topleft=(world_x, world_y))
        self.direction = pygame.math.Vector2(0, 0)
        
        self.health = 1000
        
        self.speed = 8
        self.gravity = 0.5
        self.jump_speed = 15
        self.max_jumps = 2
        self.jumpCounter = 0
        self.x = x
        self.y = y
        self.world_x = world_x
        self.world_y = world_y
        self.on_ground = False
        self.jumping = False
        self.is_Spawned = is_Spawned
    
    # Movement
    def moveLeft(self):
        self.direction.x = -1
        
    def moveRight(self):
        self.direction.x = 1
       
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
        if not keys[pygame.K_SPACE] and not keys[pygame.K_UP]:
            self.jumping = False
            
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
    
    def draw(self, canvas, camera):
        canvas.blit(self.sprite, self.rect.move(camera))
    
    