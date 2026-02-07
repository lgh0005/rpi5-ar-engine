from core.singleton import SingletonMeta
from debug import Logger

class RenderManager(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def initialize(self):
        Logger.info("[Render] RenderManager initialized.")

    def render(self):
        # 렌더링 로직 작성
        pass

    def stop(self):
        Logger.info("[Render] RenderManager stopped.")