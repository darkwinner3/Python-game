import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, src, tileset_image, tile_size):
        super().__init__()
        
        self.image = tileset_image.subsurface((src[0], src[1], tile_size, tile_size))
        
        self.rect = self.image.get_rect(topleft = pos)
        self.x, self.y = self.rect.x, self.rect.y
        
    def update(self, x_shift, y_shift):
        self.x += x_shift
        self.y -= y_shift
        self.rect.topleft = round(self.x), round(self.y)
        
    def draw(self, display, camera):
        display.blit(self.image, self.rect.move(camera))