from core.singleton import SingletonMeta
import pygame
import config.settings as settings

class TimeManager(metaclass=SingletonMeta):
    def __init__(self):
        self.clock = None
        self.target_fps = 60
        self.delta_time = 0.0

    def initialize(self):
        self.clock = pygame.time.Clock()
        self.target_fps = getattr(settings, 'TARGET_FPS', 60)

    def update(self):
        milliseconds = self.clock.tick(self.target_fps)
        self.delta_time = milliseconds / 1000.0

    def get_delta_time(self):
        return self.delta_time
    
    def get_fps(self):
        return self.clock.get_fps()