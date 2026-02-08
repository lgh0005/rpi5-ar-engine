from debug import Logger
from core.singleton import SingletonMeta
from objects import Component

class ObjectManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__registry = {}
        self.__pending_add  = []
        self.__pending_remove = []
        self.__components_by_type = {}

    def initialize(self):
        import components
        all_types = self._get_all_subclasses(Component)

        for cls in all_types:
            self.__components_by_type[cls] = {}
        Logger.info(f"[Object] {len(all_types)} types registered successfully.")
        Logger.info("[Object] ObjectManager initialized.")

    def _get_all_subclasses(self, cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(self._get_all_subclasses(subclass))
        return list(set(all_subclasses))
    
    def get(self, uuid):
        return self.__registry.get(uuid)
    
    def flush(self):
        pass

    def stop(self):
        Logger.info("[Object] ObjectManager stopped.")