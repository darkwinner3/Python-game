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
    
    @classmethod
    def load_from_layer(cls, tile_layer, autoTile_layer, tileset_image, autoTile_image, world_offset):
        tiles = pygame.sprite.Group()
        tile_size = tile_layer['__gridSize']
        
        for tile_data in tile_layer.get('gridTiles', []):
            tile_px_x, tile_px_y = tile_data["px"]
            
            tile_world_x = tile_px_x + world_offset[0]
            tile_world_y = tile_px_y + world_offset[1]
            
            src = tile_data['src']
            
            tile = cls((tile_world_x, tile_world_y), src, tileset_image, tile_size)
            
            tiles.add(tile)
            
        for tile_data in autoTile_layer.get('autoLayerTiles', []):
            tile_px_x, tile_px_y = tile_data["px"]
            
            tile_world_x = tile_px_x + world_offset[0]
            tile_world_y = tile_px_y + world_offset[1]
            
            src = tile_data['src']
            
            tile = cls((tile_world_x, tile_world_y), src, autoTile_image, tile_size)
            
            tiles.add(tile)
        return tiles