import pygame
import globals
import managers
from components import *
from debug import Logger

# 2. Engine Core Class
class EngineCore:
    def __init__(self):
        self.running = False

    def initialize(self):
        
        # 1. Pygame 초기화
        pygame.init()
        
        # 2. 매니저 초기화
        managers.create_managers()
        globals.WINDOW.initialize()
        globals.RENDER.initialize()
        globals.RESOURCE.initialize() 
        globals.SCENE.initialize()
        globals.UI.initialize()
        globals.OBJECT.initialize()
        globals.TIME.initialize()
        globals.INPUT.initialize()
        globals.CAMERA.initialize()
        globals.VISION.initialize()
        self.running = True

    def run(self):
        while self.running:
            # 1. Delta Time 계산
            globals.TIME.update()
            dt = globals.TIME.get_delta_time()

            # 2. 이벤트 처리 (Input)
            self.process_events()

            # 3. 업데이트 (Logic & Vision)
            self.update(dt)

            # 4. 렌더링 (Draw)
            self.render()

        self.cleanup()

    def process_events(self):
        # TODO : 필요한 pygame 이벤트 폴링 추가 필요
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                globals.WINDOW.handle_resize(event.w, event.h)

    def update(self, dt):
        globals.INPUT.update()
        globals.SCENE.update(dt)
        globals.UI.update(dt)

    def render(self):
        globals.RENDER.render()
        pygame.display.flip()

    def cleanup(self):

        # 매니저 종료
        globals.VISION.stop()
        globals.UI.stop()
        globals.OBJECT.stop()
        globals.SCENE.stop()
        globals.INPUT.stop()
        globals.CAMERA.stop()
        globals.RENDER.stop()
        globals.RESOURCE.stop()
        globals.TIME.stop()
        globals.WINDOW.stop()

        # Pygame 종료
        self.running = False
        pygame.quit()
        Logger.info("Engine Shutdown Complete.")

