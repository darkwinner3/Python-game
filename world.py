import pygame, json, sys
from tile import Tile
from player import Player
from npc import NPC

with open("level1-map.json") as f:
            level_data = json.load(f)
f.close()

class Level1:
    def __init__(self, screen, display):
        self.levels = level_data['levels']
        self.player = pygame.sprite.GroupSingle()
        
        self.loaded_levels = []
        self.tiles_by_level = {}
        self.current_level = None
        self.level = None
        self.player_data = None
        self.npc_data = None
        
        self.get_initial_level(display)
        
        self.display = display
        self.screen = screen
        
        
        self.current_level_index = 0
        
        self.x_shift = 0
        self.y_shift = 0
            
    def vertical_movement_collision(self):
        player = self.player.sprite
        
        if player:
            player.apply_gravity()
        
            for level_id, level_tiles in self.tiles_by_level.items():
                for sprite in level_tiles.sprites():
                    if sprite.rect.colliderect(player.rect):
                        if player.direction.y > 0:  # Moving down
                            player.rect.bottom = sprite.rect.top
                            player.direction.y = 0
                            player.on_ground = True
                            player.jumpCounter = 0
                        elif player.direction.y < 0:  # Moving up
                            player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                    if player.on_ground and player.direction.y > 1 or player.direction.y < 0:
                        player.on_ground = False
        
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        if player:
            player.rect.x += player.direction.x * player.speed
        
            for level_id, level_tiles in self.tiles_by_level.items():
                for sprite in level_tiles.sprites():
                    if sprite.rect.colliderect(player.rect):
                        if player.direction.x > 0:
                            player.rect.right = sprite.rect.left
                        elif player.direction.x < 0:
                            player.rect.left = sprite.rect.right
        
    
    def calculate_map_boundaries(self):
        map_left = float('inf')
        map_right = float('-inf')
        map_top = float('inf')
        map_bottom = float('-inf')
        
        for level in self.levels:
            level_x, level_y = level['worldX'], level['worldY']
            level_width, level_height = level['pxWid'], level['pxHei']
            
            map_left = min(map_left, level_x)
            map_top = min(map_top, level_y)
            map_right = max(map_right, level_x + level_width)
            map_bottom = max(map_bottom, level_y + level_height)
            
        return map_left, map_right, map_top, map_bottom
        
    
    def run(self):
        self.display.fill(self.SKYCOLOR)
        
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        
        
        for level_id, level_tiles in self.tiles_by_level.items():
                for sprite in level_tiles.sprites():
                    sprite.update(self.x_shift, self.y_shift)
        self.player.update()
        self.npc.update()
        
        self.load_nearby_levels(self.player.sprite.rect.x, self.player.sprite.rect.y, self.display)
        
        map_left, map_right, map_top, map_bottom = self.calculate_map_boundaries()
        if self.player:
            camera_x = -self.player.sprite.rect.centerx + self.display.get_rect().centerx
        
            if self.player.sprite.rect.centerx < map_left + self.display.get_rect().centerx:
                camera_x = -map_left
            if self.player.sprite.rect.centerx > map_right - self.display.get_rect().centerx:
                camera_x = -(map_right - self.display.get_rect().width)
                
            camera_y = -self.player.sprite.rect.centery + self.display.get_rect().centery
            
            if self.player.sprite.rect.centery < map_top + self.display.get_rect().centery:
                camera_y = -map_top
            if self.player.sprite.rect.centery > map_bottom - self.display.get_rect().centery:
                camera_y = -(map_bottom - self.display.get_rect().height)
                
            camera = (camera_x, camera_y)
            
        self.load_map(camera)
        
        print(self.tiles_by_level)
        
        # print(self.player.sprite.rect.x)
        
        # Draw player if present
        if self.player:
            self.player.sprite.draw(self.display, camera)

        # Draw NPCs if they exist
        if self.npc:
            self.npc.sprite.draw(self.display, camera)
            
        self.draw(self.screen)
        
    def load_nearby_levels(self, player_x, player_y, display, range_x = 24577, range_y = 12289):
        # unlaod levels based on player position
        self.loaded_levels = [level for level in self.loaded_levels if self.is_within_range(level, player_x, player_y, range_x, range_y)]
        
        for level in self.levels:
            level_id = level['identifier']
            current_level_id = self.current_level['identifier']
            # Load nearby levels that are not already loaded
            if self.is_within_range(level, player_x, player_y, range_x, range_y) and level not in self.loaded_levels:
                self.load_level(level, display)
            if player_x >= level['worldX'] and player_y >= level['worldY']:
                self.current_level = level 
        # Now, unload levels that are no longer within range
        for level_id, level_tiles in list(self.tiles_by_level.items()):
            if not self.is_within_range(self.get_level_by_id(level_id), player_x, player_y, range_x, range_y) and level_id != current_level_id:
                level_tiles.empty()  # Unload tiles by emptying the sprite group
                del self.tiles_by_level[level_id]

    def get_level_by_id(self, level_id):
        return next((level for level in self.levels if level['identifier'] == level_id), None)
    
    def is_within_range(self, level, player_x, player_y, range_x, range_y):
        level_x, level_y = level['worldX'], level['worldY']
        return abs(level_x - player_x) <= range_x and abs(level_y - player_y) <= range_y
    
    def get_initial_level(self, display):
        current_level = next((level for level in self.levels if level['identifier'] == "Level_2"), None)
        
        self.current_level = current_level
        
        self.load_level(self.current_level, display)
    
    def load_level(self, level, display): 
        self.level = level
        self.setup_level(display)
        self.loaded_levels.append(level)    

    
    def load_entities(self):
        
        self.npc = pygame.sprite.GroupSingle()
        
        if self.player_data == None:
            for entity in self.current_level["layerInstances"][1]["entityInstances"]:
                if entity["__identifier"] == "Player":
                    for field in entity["fieldInstances"]:
                        if field["__identifier"] == "Is_Spawned":
                            if field["__value"] == False:
                                self.player_data = entity
                                self.Is_Spawned = True
                if entity["__identifier"] == "Npc":
                    self.npc_data = entity
            if self.player_data:
                self.player_initial_x, self.player_initial_y = self.player_data["px"]
                self.player_initial_world_x = self.current_level['worldX'] + self.player_initial_x
                self.player_initial_world_y = self.current_level['worldY'] + self.player_initial_y
                self.player_width = self.player_data.get("width", 0)
                self.player_height = self.player_data.get("height", 0)
                self.player_size = (self.player_width, self.player_height)
            else:
                self.player_initial_x, self.player_initial_y = 0, 0
                self.size = (0, 0)
                
            if self.npc_data:
                self.npc_initial_x, self.npc_initial_y = self.npc_data["px"]
                self.npc_width = self.npc_data.get("width", 0)
                self.npc_height = self.npc_data.get("height", 0)
                self.npc_size = (self.npc_width, self.npc_height)
            else:
                self.npc_initial_x, self.npc_initial_y = 0, 0
                self.size = (0, 0)
        
        
            
        character_spritesheet_path = next(
            (tileset.get("relPath") for tileset in level_data.get("defs", {}).get("tilesets", []) if tileset.get("identifier") == "CharacterSprite"),
            None
        )
        
        if self.player.sprite:
        # Use the current world position of the player
            world_x = self.player.sprite.rect.x
            world_y = self.player.sprite.rect.y
        else:
            # Default to the initial spawn position
            world_x = self.player_initial_world_x
            world_y = self.player_initial_world_y
        
        local_x = world_x - self.current_level['worldX']
        local_y = world_y - self.current_level['worldY']
        
        if not self.player.sprite:  # Only create a new player if one doesn't already exist
            player = Player(local_x, local_y, world_x, world_y, character_spritesheet_path, self.player_size, self.Is_Spawned)
            self.player.add(player)
            
        if self.npc_data:
            npc = NPC(self.npc_initial_x, self.npc_initial_y, character_spritesheet_path, self.npc_size)
            self.npc.add(npc)
            
    def setup_level(self, display):
        level_id = self.level['identifier']
        
        if level_id not in self.tiles_by_level:
            tiles = pygame.sprite.Group()
            
            self.load_entities()
            self.load_tiles(tiles)
            self.tiles_by_level[level_id] = tiles

        self.SKYCOLOR = (135, 206, 235)
        
        
    
    
    def draw(self, screen):
        screen.blit(self.display, (0, 0))
        
    def load_map(self, camera):
        
        for level_id, level_tiles in self.tiles_by_level.items():
                for sprite in level_tiles.sprites():
                    sprite.draw(self.display, camera)

    def load_tiles(self, tiles):
        # Extract the tile layer and load the tileset image
        self.tile_layer = next(layer for layer in self.level['layerInstances'] if layer['__identifier'] == 'Tiles')
        self.autoTile_layer = next(layer for layer in self.level['layerInstances'] if layer['__identifier'] == 'IntGrid')
        self.tileset_image = pygame.image.load(self.tile_layer['__tilesetRelPath']).convert_alpha()
        self.autoTileset_image = pygame.image.load(self.autoTile_layer['__tilesetRelPath']).convert_alpha()
        
        # Loop through gridTiles and create Tile objects
        for tile_data in self.tile_layer['gridTiles']:
            self.tile_size = self.tile_layer['__gridSize']
            
            # pixel position
            tile_px_x, tile_px_y = tile_data["px"]
            
            # world position
            tile_world_x = tile_px_x + self.level['worldX']
            tile_world_y = tile_px_y + self.level['worldY']
            
            # image source
            src = tile_data['src']
            
            tile_sprite = Tile((tile_world_x, tile_world_y), src, self.tileset_image, self.tile_size)  # Create Tile sprite
            tiles.add(tile_sprite)
        
        for tile_data in self.autoTile_layer['autoLayerTiles']:
            self.autoTile_size = self.autoTile_layer['__gridSize']
            # pixel position
            tile_px_x, tile_px_y = tile_data["px"]
            
            # world position
            tile_world_x = tile_px_x + self.level['worldX']
            tile_world_y = tile_px_y + self.level['worldY']
            
            src = tile_data['src']
            tile_sprite = Tile((tile_world_x, tile_world_y), src, self.autoTileset_image, self.autoTile_size)
            tiles.add(tile_sprite)
        
    