import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, pixel_pos, src, tileset_image, tile_size, type=None, variant=None):
        super().__init__()
        self.type = type
        self.variant = variant
        self.pixel_pos = pixel_pos
        self.pos = pos
        self.src = src
        self.tile_size = tile_size
        
        self.image = tileset_image.subsurface((src[0], src[1], tile_size, tile_size))
        
        self.rect = self.image.get_rect(topleft = pos)
        self.x, self.y = self.rect.x, self.rect.y
        
    def draw(self, display, camera):
        display.blit(self.image, (self.pos[0] + camera[0], self.pos[1] + camera[1]))