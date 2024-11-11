import pygame, json
from tile import Tile
from player import Player
from npc import NPC

with open("level1-map.json") as f:
            level_data = json.load(f)
f.close()

class Level1:
    def __init__(self, screen, display):
        self.levels = level_data['levels']
        # self.level = self.get_level()
        
        self.loaded_levels = []
        self.level = None
        
        self.get_initial_level(display)
        
        self.setup_level(display)
        self.display = display
        self.screen = screen
        
        
        self.current_level_index = 0
        
        self.x_shift = 0
        self.y_shift = 0
            
    def vertical_movement_collision(self):
        player = self.player.sprite
        
        if player:
            player.apply_gravity()
        
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                        player.jumpCounter = 0
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
            if player.on_ground and player.direction.y > 1 or player.direction.y < 0:
                player.on_ground = False
        
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        if player:
            player.rect.x += player.direction.x * player.speed
        
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                    elif player.direction.x < 0:
                        player.rect.left = sprite.rect.right
        
    
    def calculate_map_boundaries(self):
        map_left = 0
        map_right = 0
        map_top = 0 
        map_bottom = 0  
        
        for level in self.loaded_levels:
            level_width = level['pxWid'] 
            level_height = level['pxHei']
            
            map_right += level_width 
            map_bottom += level_height

        map_right /= 2
        map_bottom /= 2
            
        return map_left, map_right, map_top, map_bottom
    
    def run(self):
        self.display.fill(self.SKYCOLOR)
        
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        
        
        
        self.tiles.update(self.x_shift, self.y_shift)
        self.player.update()
        self.npc.update()
        
        player_world_x, player_world_y = self.get_player_world_position()
        
        self.load_nearby_levels(player_world_x, player_world_y, self.display)
        
        # map_left = 0
        # # map_right = 200000
        # map_right = self.level_width
        # map_top = 0
        # # map_bottom = 200000
        # map_bottom = self.level_height
        
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
        else:
            # Fallback camera if no player exists (e.g., top-left corner of the map)
            camera = (0, 0)
            
        self.load_map(camera)
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
            if self.is_within_range(level, player_x, player_y, range_x, range_y) and level not in self.loaded_levels:
                self.load_level(level, display)
            
    def is_within_range(self, level, player_x, player_y, range_x, range_y):
        level_x, level_y = level['worldX'], level['worldY']
        return abs(level_x - player_x) <= range_x and abs(level_y - player_y) <= range_y
    
    def get_initial_level(self, display):
        current_level = next((level for level in self.levels if level['identifier'] == "Level_2"), None)
        
        self.level = current_level
        
        self.load_level(self.level, display)
    
    def load_level(self, level, display): 
        # self.level = level
        self.setup_level(display)
        self.loaded_levels.append(level)    
        
    def get_player_world_position(self):
        return self.player_initial_world_x, self.player_initial_world_y
    
    def load_entities(self):
        self.player = pygame.sprite.GroupSingle()
        self.npc = pygame.sprite.GroupSingle()
        
        self.player_data = None
        self.npc_data = None
        for entity in self.level["layerInstances"][1]["entityInstances"]:
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
            self.player_initial_world_x = self.level['worldX'] + self.player_initial_x
            self.player_initial_world_y = self.level['worldY'] + self.player_initial_y
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
        
        if self.player_data:
            player = Player(self.player_initial_x, self.player_initial_y, self.player_initial_world_x, self.player_initial_world_y, character_spritesheet_path, self.player_size, self.Is_Spawned)
            self.player.add(player)
            
        if self.npc_data:
            npc = NPC(self.npc_initial_x, self.npc_initial_y, character_spritesheet_path, self.npc_size)
            self.npc.add(npc)
            
    def setup_level(self, display):
        self.tiles = pygame.sprite.Group()
        self.load_entities()
        # self.load_nearby_levels(self.player.sprite.rect.x, self.player.sprite.rect.y, display)
        self.load_tiles()
        
        self.level_width, self.level_height = self.level['pxWid'], self.level['pxHei']
        display = pygame.Surface((self.level_width, self.level_height), pygame.SRCALPHA)
        display.set_colorkey((135, 206, 235))

        self.SKYCOLOR = (135, 206, 235)
        
        
    
    
    def draw(self, screen):
        screen.blit(self.display, (0, 0))
        
    def load_map(self, camera):
        for tile in self.tiles:
            tile.draw(self.display, camera)
        
    def read_gridMap(self):
        return level_data["levels"][0]["layerInstances"][2]["intGridCsv"]

    def load_tiles(self):
        # Extract the tile layer and load the tileset image
        self.tile_layer = next(layer for layer in self.level['layerInstances'] if layer['__identifier'] == 'Tiles')
        self.autoTile_layer = next(layer for layer in self.level['layerInstances'] if layer['__identifier'] == 'IntGrid')
        self.tileset_image = pygame.image.load(self.tile_layer['__tilesetRelPath']).convert_alpha()
        self.autoTileset_image = pygame.image.load(self.autoTile_layer['__tilesetRelPath']).convert_alpha()
        
        # Loop through gridTiles and create Tile objects
        for tile_data in self.tile_layer['gridTiles']:
            self.tile_size = self.tile_layer['__gridSize']
            pos = tile_data['px']  # Position (x, y)
            src = tile_data['src']
            tile_sprite = Tile(pos, src, self.tileset_image, self.tile_size)  # Create Tile sprite
            self.tiles.add(tile_sprite)
        for tile_data in self.autoTile_layer['autoLayerTiles']:
            self.autoTile_size = self.autoTile_layer['__gridSize']
            pos = tile_data['px']
            src = tile_data['src']
            tile_sprite = Tile(pos, src, self.autoTileset_image, self.autoTile_size)
            self.tiles.add(tile_sprite)
        
    