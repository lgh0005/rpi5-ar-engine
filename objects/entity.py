from objects import Object
from typing import override

class Entity(Object):
    def __init__(self):
        super().__init__()
        self.components = []
        self.parent = None
        self.__state : int = 0

    def add_component(self, component):
        component.entity = self
        self.components.append(component)
        return component

    def get_component(self, component_type):
        for comp in self.components:
            if isinstance(comp, component_type):
                return comp
        return None

    @override
    def awake(self):
        for comp in self.components:
            comp.awake()
    
    @override
    def start(self):
        for comp in self.components:
            comp.start()
    
    @override
    def update(self, dt : float):
        if not self.active: return
        for comp in self.components: comp.update(dt)
        for child in self.children: child.update(dt)

    @override
    def late_update(self, dt : float):
        if not self.active: return
        for comp in self.components: comp.late_update(dt)
        for child in self.children: child.late_update(dt)

    @property
    def state(self): return self.__state
    
    @state.setter
    def state(self, value : int): self.__state = value