import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.volume = 0.5  
        self.tracks = {
            "INTRO": "sounds/intro_theme.mp3",
            "MENU": "sounds/menu_theme.mp3",
            "PLAYING": "sounds/forest_ambient.mp3",
            "END": "sounds/game_over.mp3"
        }
        self.current_state = None

    def play_state_music(self, state):
        if state == self.current_state:
            return
            
        track_path = self.tracks.get(state)
        if track_path and os.path.exists(track_path):
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.current_state = state
        else:
            pygame.mixer.music.stop()
            self.current_state = state

    def set_volume(self, new_volume):
        self.volume = max(0.0, min(1.0, new_volume))
        pygame.mixer.music.set_volume(self.volume)