from objects import Object
from typing import override

class Entity(Object):
    def __init__(self):
        super().__init__()
        self.__parent = None
        self.__components = {}

    def add_component(self, component_cls):
        instance = component_cls()
        instance.entity = self
        self.__components[component_cls] = instance
        return instance

    def get_component(self, component_cls):
        return self.__components.get(component_cls)

# region [Default object overrides]
    @override
    def awake(self):
        for comp in self.__components.values():
            comp.awake()

    @override
    def start(self):
        for comp in self.__components.values():
            if comp.enabled:
                comp.start()

    @override
    def update(self, dt):
        for comp in self.__components.values():
            if comp.enabled:
                comp.update(dt)

    @override
    def late_update(self, dt):
        for comp in self.__components.values():
            if comp.enabled:
                comp.late_update(dt)
# endregion

# region [Default Entity getters & setters]
    @property
    def parent(self) : return self.__parent

    @parent.setter
    def parent(self, value) : self.__parent = value

    @property
    def components(self) : return self.__components
# endregion