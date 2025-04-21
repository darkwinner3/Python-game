import pygame
from tilemap import Tilemap
from player import Player
from npc import NPC

class World:
    def __init__(self, game, screen, display, level_data):
        self.level_data = level_data
        self.levels = self.level_data['levels']
        self.player = pygame.sprite.GroupSingle()
        self.npc = pygame.sprite.GroupSingle()
        self.game = game
        
        
        
        self.loaded_levels = []
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
        
    
    def run(self):
        self.display.fill(self.SKYCOLOR)
        
        self.player_world_rect = self.player.sprite.rect()
        
        map_left, map_right, map_top, map_bottom = self.calculate_map_boundaries()
        
        if self.player:
            camera = self.upate_camera(map_left, map_right, map_top, map_bottom)
            
            self.player.sprite.update(self.tilemap, (self.player.sprite.movement[1] - self.player.sprite.movement[0], 0))
            
        # print(self.player.sprite.movement[1])
        
        # self.npc.sprite.update(self.tilemap)
        
        self.load_nearby_levels(self.player_world_rect.x, self.player_world_rect.y, self.display)
        
        self.tilemap.render(self.display, camera)
        
        if self.npc:
            self.npc.sprite.render(self.display, camera)
        
        self.player.sprite.render(self.display, camera)
        
        # for level in self.loaded_levels:
        #     level_id = level['identifier']
        #     print(f"Loaded level: {level_id}")
        
        # Draw NPCs if they exist
        
            
        self.draw(self.screen)
        
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
    
    def upate_camera(self, map_left, map_right, map_top, map_bottom):
        self.scroll = [0, 0]
        
        target_scroll_x = (-self.player.sprite.rect().centerx + self.display.get_width() / 2)
        target_scroll_y = (-self.player.sprite.rect().centery + self.display.get_height() / 2)
        
        if self.player.sprite.rect().centerx < map_left + self.display.get_width() / 2:
            target_scroll_x = -map_left
        elif self.player.sprite.rect().centerx > map_right - self.display.get_width() / 2:
            target_scroll_x = -(map_right - self.display.get_width())

        if self.player.sprite.rect().centery < map_top + self.display.get_height() / 2:
            target_scroll_y = -map_top
        elif self.player.sprite.rect().centery > map_bottom - self.display.get_height() / 2:
            target_scroll_y = -(map_bottom - self.display.get_height())
        
        render_scroll = (int(target_scroll_x), int(target_scroll_y))
                
        return (render_scroll)
    
    # NEEDS TO BE FIXED
    def load_nearby_levels(self, player_x, player_y, display, range_x = 10000, range_y = 10000):
        # unlaod levels based on player position
        self.loaded_levels = [level for level in self.loaded_levels if self.is_within_range(self.get_level_boundaries(level), player_x, player_y, range_x, range_y)]
        
        for level in self.levels:
            level_id = level['identifier']
            current_level_id = self.current_level['identifier']
            
            level_boundaries = self.get_level_boundaries(level)
            
            # Load nearby levels that are not already loaded
            if self.is_within_range(level_boundaries, player_x, player_y, range_x, range_y) and level not in self.loaded_levels:
                self.load_level(level, display)
            if level_boundaries['minX'] <= player_x <= level_boundaries['maxX'] and level_boundaries['minY'] <= player_y <= level_boundaries['maxY']:
                self.current_level = level # Update the current level based on the player's position
                # print(self.current_level['identifier'])
                self.tilemap.load_tilemap(current_level_id)
                
        # Now, unload levels that are no longer within range
        for level_id, level_tiles in list(self.tilemap.tiles_by_level.items()):
            level = self.get_level_by_id(level_id)
            level_boundaries = self.get_level_boundaries(level)
            
            if not self.is_within_range(level_boundaries, player_x, player_y, range_x, range_y) and level_id != current_level_id:
                level_tiles.empty()  # Unload tiles by emptying the sprite group
                del self.tilemap.tiles_by_level[level_id]
                
    def get_level_boundaries(self, level):
            return {
                'minX': level['worldX'],
                'maxX': level['worldX'] + level['pxWid'],
                'minY': level['worldY'],
                'maxY': level['worldY'] + level['pxHei']
            }
    def get_level_by_id(self, level_id):
        return next((level for level in self.levels if level['identifier'] == level_id), None)
    # NEEDS TO BE FIXED
    def is_within_range(self, level_boundaries, player_x, player_y, range_x, range_y):
        within_horizontal_range = (level_boundaries['minX'] - range_x <= player_x <= level_boundaries['maxX'] + range_x)
        within_vertical_range = (level_boundaries['minY'] - range_y <= player_y <= level_boundaries['maxY'] + range_y)
        return within_horizontal_range and within_vertical_range
    
    def get_initial_level(self, display):
        current_level = next((level for level in self.levels if level['identifier'] == "Level_2"), None)
        
        self.current_level = current_level
        
        self.tilemap = Tilemap(self.game)
        
        self.load_level(self.current_level, display)
        
    def setup_level(self, display):
        level_id = self.level['identifier']
        
        if level_id not in self.tilemap.tiles_by_level:
         
            self.tilemap.load_from_layer(self.level, level_id)
            
            self.load_entities()
        else:
            self.load_entities()
        if level_id == self.current_level['identifier']:
            self.tilemap.load_tilemap(self.current_level['identifier'])
        

        self.SKYCOLOR = (135, 206, 235)
        
        
    def load_level(self, level, display):
        print(f"Current level fddfd after change: {self.current_level['identifier']}")
        self.level = level
        self.setup_level(display)
        
        print(f"Player initial world position: ({self.player_initial_world_x}, {self.player_initial_world_y})")
        print(f"Player rect after creation: {self.player.sprite.rect}")
        if level not in self.loaded_levels:
            self.loaded_levels.append(level)
        
        for level in self.loaded_levels:
            print(level['identifier'])
    
    def load_entities(self):
        
        if self.player_data == None:
            for entity in self.current_level["layerInstances"][1]["entityInstances"]:
                if entity["__identifier"] == "Player":
                    for field in entity["fieldInstances"]:
                        if field["__identifier"] == "Is_Spawned":
                            if field["__value"] == False:
                                self.player_data = entity
                                self.Is_Spawned = True
                elif entity["__identifier"] == "Npc":
                    self.npc_data = entity
                elif entity["__identifier"] == "Player_animation":
                    self.player_animation_entity = entity
                    
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
                self.npc_initial_world_x = self.current_level['worldX'] + self.npc_initial_x
                self.npc_initial_world_y = self.current_level['worldY'] + self.npc_initial_y
                self.npc_width = self.npc_data.get("width", 0)
                self.npc_height = self.npc_data.get("height", 0)
                self.npc_size = (self.npc_width, self.npc_height)
            else:
                self.npc_initial_x, self.npc_initial_y = 0, 0
                self.size = (0, 0)
        
        if self.player.sprite:
        # Use the current world position of the player
            world_x = self.player_world_rect.x
            world_y = self.player_world_rect.y
        else:
            # Default to the initial spawn position
            world_x = self.player_initial_world_x
            world_y = self.player_initial_world_y
        
        local_x = world_x - self.current_level['worldX']
        local_y = world_y - self.current_level['worldY']
        
        if not self.player.sprite:  # Only create a new player if one doesn't already exist
            player = Player(self.game, (local_x, local_y), (world_x, world_y), self.player_size, self.Is_Spawned)
            self.player.add(player)
            
        if not self.npc.sprite:
            npc = NPC(self.game, (local_x, local_y), (self.npc_initial_world_x,  self.npc_initial_world_y), self.npc_size)
            self.npc.add(npc)
            
    def draw(self, screen):
        screen.blit(self.display, (0, 0))

    def update_resolution(self, width, height, screen):
        self.screen = screen
        self.display = pygame.Surface((width, height), pygame.SRCALPHA)
        
    