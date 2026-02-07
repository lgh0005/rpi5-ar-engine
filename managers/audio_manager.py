import os
import pygame
from core.singleton import SingletonMeta

class AudioManager(metaclass=SingletonMeta):
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.5

    def initialize(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def load_sound(self, name, path):
        if name not in self.sounds:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sfx_volume)
                self.sounds[name] = sound
            else:
                print(f"Sound not found: {path}")

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, path, loop=-1):
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()