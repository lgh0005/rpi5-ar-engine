import pygame
import config.constants as constants

# 2. Engine Core Class
class EngineCore:
    def __init__(self):
        self.running = False

    def initialize(self):
        
        # 1. Pygame 초기화
        pygame.init()
        
        # 2. 매니저 초기화
        constants.WINDOW.initialize()
        constants.RESOURCE.initialize()
        constants.RENDER.initialize()
        constants.SCENE.initialize()
        constants.UI.initialize()
        constants.TIME.initialize()
        constants.INPUT.initialize()
        constants.CAMERA.initialize()
        constants.VISION.initialize()

        self.running = True

    def run(self):
        if not self.running:
            self.initialize()

        while self.running:
            # 1. Delta Time 계산
            constants.TIME.update()
            dt = constants.TIME.get_delta_time()

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
                constants.WINDOW.handle_resize(event.w, event.h)

    def update(self, dt):
        constants.INPUT.update()
        constants.SCENE.update(dt)
        constants.UI.update(dt)

    def render(self):
        constants.RENDER.render()
        pygame.display.flip()

    def cleanup(self):
        # 매니저 정리 (순서 중요)
        # self.camera_manager.stop()

        self.running = False
        pygame.quit()

