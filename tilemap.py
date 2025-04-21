import pygame, math
from tile import Tile

PHYSICS_TILES = {'solid', 'stone'}

character_width = 63
character_height = 125
tile_width = 64
tile_height = 64

half_width_in_tiles = math.ceil(character_width / 2 / tile_width)
half_height_in_tiles = math.ceil(character_height / 2 / tile_height)

NEIGHBOR_OFFSETS = []
for dy in range(-half_height_in_tiles, half_height_in_tiles + 2):
    for dx in range(-half_width_in_tiles, half_width_in_tiles + 1):
        NEIGHBOR_OFFSETS.append((dx, dy))
        
# [(-1, -1), (0, -1), (1, -1),
#  (-1,  0), (0,  0), (1,  0),
#  (-1,  1), (0,  1), (1,  1),
#  (-1,  2), (0,  2), (1,  2)]

class Tilemap(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        
        self.tiles_by_level = {}
        self.tilemap = {}
        
        self.game = game
        self.tile_size = 0
        
    def render(self, display, camera):
        for level_id, level_tiles in self.tiles_by_level.items():
            for tile in level_tiles:
                tile.draw(display, camera)
        
    
    def load_tiles(self, tile_layer, autoTile_layer, tileset_image, autoTile_image, world_offset):
        tiles = pygame.sprite.Group()
        self.tile_size = tile_layer['__gridSize']
        
        for tile_data in tile_layer.get('gridTiles', []):
            tile_px_x, tile_px_y = tile_data["px"]
            
            tile_world_x = tile_px_x + world_offset[0]
            tile_world_y = tile_px_y + world_offset[1]
            
            src = tile_data['src']
            
            tile = Tile((tile_world_x, tile_world_y), (tile_px_x, tile_px_y), src, tileset_image, self.tile_size)
            
            tiles.add(tile)
            
        for tile_data in autoTile_layer.get('autoLayerTiles', []):
            tile_px_x, tile_px_y = tile_data["px"]
            
            tile_world_x = tile_px_x + world_offset[0]
            tile_world_y = tile_px_y + world_offset[1]
            
            src = tile_data['src']
            
            tile = Tile((tile_world_x, tile_world_y), (tile_px_x, tile_px_y), src, autoTile_image, self.tile_size)
            
            tiles.add(tile)
        
        return tiles
    
    def load_tilemap(self, current_level):
        self.tilemap = {}
        for tile in self.tiles_by_level[current_level]:
            self.tilemap[(tile.pos[0] // self.tile_size, tile.pos[1] // self.tile_size)] = tile
    
    def load_from_layer(self, level, level_id):
        tile_layer = next(layer for layer in level['layerInstances'] if layer['__identifier'] == 'Tiles')
        autoTile_layer = next(layer for layer in level['layerInstances'] if layer['__identifier'] == 'IntGrid')
        tileset_image = pygame.image.load(tile_layer['__tilesetRelPath']).convert_alpha()
        autoTileset_image = pygame.image.load(autoTile_layer['__tilesetRelPath']).convert_alpha()
        
        self.world_offset = (level['worldX'], level['worldY'])
        
        tiles = self.load_tiles(tile_layer, autoTile_layer, tileset_image, autoTileset_image, self.world_offset)
        
        self.tiles_by_level[level_id] = tiles
    
    
    def extract(self, tiles, id_pairs, keep=False):
        matches = []
        for tile in tiles.sprites():
            if (tile.type, tile.variant) in id_pairs:
                matches.append(tile)
                if not keep:
                    tiles.remove(tile)
        return matches
    
    def solid_check(self, pos):
        # Check if a position intersects with a solid tile
        tile_loc = (int(pos[0]), int(pos[1]))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc].type in PHYSICS_TILES:
                return self.tilemap[tile_loc]
            return self.tilemap[tile_loc]
        return None
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            neighbor_pos = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
            tile = self.tilemap.get(neighbor_pos)
            if tile:
                # print(tile.pos)
                tiles.append(tile)
        return tiles
        
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.type in PHYSICS_TILES:
                rects.append(tile.rect)
            rects.append(tile.rect)
        return rects