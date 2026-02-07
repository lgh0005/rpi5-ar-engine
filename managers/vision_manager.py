from core.singleton import SingletonMeta
from debug import Logger

class VisionManager(metaclass=SingletonMeta):
    def __init__(self):
        # Vision Manager 초기화 코드 작성
        pass

    def initialize(self):
        Logger.info("[Vision] VisionManager initialized.")

    def process_vision(self, frame):
        # 비전 처리 로직 작성
        pass

    def stop(self):
        Logger.info("[Vision] VisionManager stopped.")