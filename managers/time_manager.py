import config
from core.singleton import SingletonMeta
import pygame
from debug import Logger

class TimeManager(metaclass=SingletonMeta):
    def __init__(self):
        self.clock = None
        self.target_fps = 60
        self.delta_time = 0.0

    def initialize(self):
        self.clock = pygame.time.Clock()
        self.target_fps = config.TARGET_FPS
        Logger.info("[Time] TimeManager initialized.")

    def update(self):
        milliseconds = self.clock.tick(self.target_fps)
        self.delta_time = milliseconds / 1000.0

    def get_delta_time(self):
        return self.delta_time
    
    def get_fps(self):
        return self.clock.get_fps()

    def stop(self):
        self.clock = None
        Logger.info("[Time] TimeManager stopped.")