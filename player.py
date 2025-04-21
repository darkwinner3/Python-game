import pygame
from physicsEntity import PhysicsEntity

class Player(PhysicsEntity, pygame.sprite.Sprite):
    def __init__(self, game, local_pos, world_pos, size, is_Spawned):
        super().__init__(game, 'player', world_pos, size, local_pos)
        pygame.sprite.Sprite.__init__(self)
        
        self.speed_increment = 2
        self.air_time = 0
        self.doubleJump = True
        self.jumping = False
        self.current_jumps = 0
        self.max_jumps = 2
        self.jump_speed = 5.5
        self.dashing = 0
        self.grounded_timer = 0
        
        self.movement = [False, False]
        
        self.health = 1000
        
        self.x, self.y = local_pos
        self.world_x, self.world_y = world_pos
        
        self.is_Spawned = is_Spawned
                
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -100
            else:
                self.dashing = 100
    
    def jump(self):
        
        if self.grounded_timer > 3 and self.current_jumps == 0:  # Assume 3 frames of being in the air means a fall
            self.doubleJump = False
            self.current_jumps = 1
        
        if not self.doubleJump and self.current_jumps < self.max_jumps:
            self.current_jumps += 1
            self.velocity.y = -self.jump_speed
            self.air_time = 5.5
            self.jumping = True
            print(self.current_jumps)
        elif self.doubleJump and self.current_jumps < self.max_jumps:  # Player is airborne
            self.current_jumps += 1
            self.velocity.y = -self.jump_speed
            self.air_time = 5.5
            self.jumping = True
            print(self.current_jumps)
            
        
            
            
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            if not self.movement[1]:  # Start moving right
                self.movement[1] = True
            self.velocity.x = self.speed_increment  # Set positive velocity for right movement
        elif not keys[pygame.K_RIGHT] and self.movement[1]:  # Stop moving right
            self.movement[1] = False
            self.velocity.x = 0
            
        if keys[pygame.K_LEFT]:
            if not self.movement[0]:  # Start moving left
                self.movement[0] = True
            self.velocity.x = -self.speed_increment  # Set negative velocity for left movement
        elif not keys[pygame.K_LEFT] and self.movement[0]:  # Stop moving left
            self.movement[0] = False
            self.velocity.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not self.jumping:
                self.jump()
        elif not keys[pygame.K_SPACE] and not keys[pygame.K_UP]:
            self.jumping = False
        
        if keys[pygame.K_LSHIFT]:
            self.dash()
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        
        if not self.collisions['down']:
            self.grounded_timer += 1
        else:
            self.grounded_timer = 0  # Reset timer if grounded
        
        
        if self.collisions['down']:
            self.air_time = 0
            self.current_jumps = 0
            self.doubleJump = True
            
            
        self.handle_input()
        
        self.set_action('idle')
        
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity.x = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity.x *= 0.1
                
        if self.velocity.x > 0:
            self.velocity.x = max(self.velocity.x - 0.1, 0)
        else:
            self.velocity.x = min(self.velocity.x + 0.1, 0)
    
    def render(self, surf, camera):
        if abs(self.dashing) <= 50:
            super().render(surf, camera)
    
    