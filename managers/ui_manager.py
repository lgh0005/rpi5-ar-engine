from core.singleton import SingletonMeta
from debug import Logger

class UIManager(metaclass=SingletonMeta):
    def __init__(self):
        # UI Manager 초기화 코드 작성
        pass

    def initialize(self):
        Logger.info("[UI] UIManager initialized.")

    def update(self, dt):
        pass

    def stop(self):
        Logger.info("[UI] UIManager stopped.")