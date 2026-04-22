from os.path import join
import os
import pygame

class Animation(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        self.frames = self.load_frames()
        self.current_state = 'move'
        self.direction = 'right'
        self.current_index = 0
        self.timer = 0
        self.animation_speed = 0.15

    def load_frames(self):
        frames = {'move': {'left': [], 'right': []}, 'attack': {'left': [], 'right': []}}
        base_path = join("sprites", self.name)

        for state in ['move', 'attack']:
            for direction in ['left', 'right']:
                folder = join(base_path, state, direction)
                if os.path.exists(folder):
                    files = sorted([f for f in os.listdir(folder) if f.endswith('.PNG')])
                    for f in files:
                        img = pygame.image.load(join(folder, f)).convert_alpha()
                        frames[state][direction].append(img)
        return frames


    def update(self, dt, is_moving, is_attacking):
        self.timer += dt
        
        if is_attacking: self.current_state = 'attack'
        else: self.current_state = 'move'

        if self.timer >= self.animation_speed:
            self.timer = 0
            frame_list = self.frames[self.current_state][self.direction]
            if is_moving or is_attacking:
                self.current_index = (self.current_index + 1) % len(frame_list)
            else:
                self.current_index = 0 

    def draw(self, screen, x, y, tint=None):
        frame_list = self.frames[self.current_state][self.direction] 
        
        idx = self.current_index % len(frame_list)
        img = frame_list[idx].copy()
        
        if tint:
            tint_surf = pygame.Surface(img.get_size(), pygame.SRCALPHA)
            tint_surf.fill(tint)
            img.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        screen.blit(img, (x, y))

