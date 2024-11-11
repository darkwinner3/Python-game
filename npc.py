import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_image, size):
        super().__init__()
        self.sprite = pygame.image.load(sprite_image)
        self.sprite = pygame.transform.scale(self.sprite, size)
        self.rect = self.sprite.get_rect(topleft=(x, y))
    
    def draw(self, canvas, camera):
        canvas.blit(self.sprite, self.rect.move(camera))
    
    