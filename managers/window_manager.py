import pygame
import config.settings as settings
from core.singleton import SingletonMeta

class WindowManager(metaclass=SingletonMeta):
    def __init__(self):
        self.width = settings.SCREEN_WIDTH
        self.height = settings.SCREEN_HEIGHT
        self.screen = None

    def initialize(self):
        # Raspberry Pi 5 (GLES 3.0) 호환성 설정
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, settings.GL_MAJOR_VERSION)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, settings.GL_MINOR_VERSION)

        # 윈도우 생성
        self.screen = pygame.display.set_mode(
            (self.width, self.height), 
            pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
        )
        pygame.display.set_caption(settings.WINDOW_TITLE)

    def get_screen(self):
        return self.screen

    def handle_resize(self, width, height):
        self.width = width
        self.height = height
        pygame.display.set_mode(
            (self.width, self.height),
            pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
        )