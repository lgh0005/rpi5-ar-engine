from core.singleton import SingletonMeta
from debug import Logger

class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def initialize(self):
        Logger.info("[Scene] SceneManager initialized.")

    def load_scene(self, scene_name):
        Logger.info(f"[Scene] Loading scene: {scene_name}")

    def update(self, dt):
        pass

    def stop(self):
        Logger.info("[Scene] SceneManager stopped.")