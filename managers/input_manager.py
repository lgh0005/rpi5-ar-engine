from core.singleton import SingletonMeta
import pygame
from debug import Logger

class InputManager(metaclass=SingletonMeta):
    def __init__(self):
        self.prev_keys = None
        self.curr_keys = None

        self.prev_mouse = (0, 0, 0)
        self.curr_mouse = (0, 0, 0)
        self.mouse_pos = (0, 0)

    def initialize(self):
        self.prev_keys = pygame.key.get_pressed()
        self.curr_keys = pygame.key.get_pressed()
        Logger.info("[Input] InputManager initialized.")
    
    def update(self):
        self.prev_keys = self.curr_keys
        self.curr_keys = pygame.key.get_pressed()
        
        self.prev_mouse = self.curr_mouse
        self.curr_mouse = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def get_key(self, key_code):
        return self.curr_keys[key_code]

    def get_key_down(self, key_code):
        return self.curr_keys[key_code] and not self.prev_keys[key_code]

    def get_key_up(self, key_code):
        return not self.curr_keys[key_code] and self.prev_keys[key_code]

    def get_mouse_button_down(self, button_index):
        return self.curr_mouse[button_index] and not self.prev_mouse[button_index]

    def stop(self):
        self.prev_keys = None
        self.curr_keys = None
        Logger.info("[Input] InputManager stopped.")