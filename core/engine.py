import pygame
from managers import *
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
        WINDOW.initialize()
        RESOURCE.initialize()
        RENDER.initialize()
        SCENE.initialize()
        UI.initialize()
        OBJECT.initialize()
        TIME.initialize()
        INPUT.initialize()
        CAMERA.initialize()
        VISION.initialize()

        self.running = True

    def run(self):
        while self.running:
            # 1. Delta Time 계산
            TIME.update()
            dt = TIME.get_delta_time()

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
                WINDOW.handle_resize(event.w, event.h)

    def update(self, dt):
        INPUT.update()
        SCENE.update(dt)
        UI.update(dt)

    def render(self):
        RENDER.render()
        pygame.display.flip()

    def cleanup(self):

        # 매니저 종료
        VISION.stop()
        UI.stop()
        OBJECT.stop()
        SCENE.stop()
        INPUT.stop()
        CAMERA.stop()
        RENDER.stop()
        RESOURCE.stop()
        TIME.stop()
        WINDOW.stop()

        # Pygame 종료
        self.running = False
        pygame.quit()
        Logger.info("Engine Shutdown Complete.")

