from core.singleton import SingletonMeta
from debug import Logger

class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def initialize(self):
        Logger.info("[Scene] SceneManager initialized.")

    def update(self, dt):
        pass

    def stop(self):
        Logger.info("[Scene] SceneManager stopped.")