from core.singleton import SingletonMeta
from debug import Logger

class ResourceManager(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def initialize(self):
        Logger.info("[Resource] ResourceManager initialized.")

    def stop(self):
        Logger.info("[Resource] ResourceManager stopped.")