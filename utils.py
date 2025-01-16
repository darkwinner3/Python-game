import os

import pygame

BASE_IMG_PATH = 'data/pictures/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def load_tileset_images(path, data):
    animation_frames = []
    tileset = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    
    animation_path = next(
                    (tileset.get("relPath") for tileset in data.get("defs", {}).get("tilesets", []) if tileset.get("identifier") == "Animation"),
                    None
                )
    
    animation_data = extract_animation_data(animation_path, data)
        
    for frame in animation_data["frames"]:
        x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
        frame_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        frame_surface.blit(tileset, (0, 0), (x, y, w, h))
        animation_frames.append(frame_surface)
    
    animation_frames = [
            pygame.transform.scale(frame, animation_data["player_size"]) for frame in animation_frames
        ]
    
    return animation_frames

def extract_animation_data(tileset_path, data):
    player_animation_entity = None
    for entity in data["levels"][2]["layerInstances"][1]["entityInstances"]:
        if entity["__identifier"] == "Player_animation":
            player_animation_entity = entity
        
    frames = []
    for frame_data in player_animation_entity["fieldInstances"][0]["__value"]:
        frames.append({
            "x": frame_data["x"],
            "y": frame_data["y"],
            "w": frame_data["w"],
            "h": frame_data["h"],
        })
        
    rate = next((field["__value"] for field in player_animation_entity["fieldInstances"] if field["__identifier"] == "animation_rate"), 1)
    mode = next((field["__value"] for field in player_animation_entity["fieldInstances"] if field["__identifier"] == "animationMode"), "Loop")  
    
    player_width = player_animation_entity.get("width", 0)
    player_height = player_animation_entity.get("height", 0)
    player_size = (player_width, player_height) 
    
    return {
        "tileset_path": tileset_path,
        "frames": frames,
        "rate": rate,
        "mode": mode,
        "player_size": player_size,
    }
        


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
        
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 0.2) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]