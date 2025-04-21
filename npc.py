import pygame
from physicsEntity import PhysicsEntity

class NPC(PhysicsEntity, pygame.sprite.Sprite):
    def __init__(self, game, local_pos, world_pos, size):
        super().__init__(game, 'npc', world_pos, size, local_pos)
        pygame.sprite.Sprite.__init__(self)
    
    # def update(self, tilemap):
    #     super().update(tilemap)
        
    #     self.set_action('idle')
    
    def render(self, surf, camera):
        self.animation = pygame.transform.scale(self.animation, (64, 128))
        
        surf.blit(self.animation, (self.pos[0] + camera[0], self.pos[1] + camera[1]))
    
    