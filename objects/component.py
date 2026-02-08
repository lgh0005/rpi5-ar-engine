from objects import Object

class Component(Object):
    def __init__(self):
        super().__init__()
        self.entity = None
        self.enabled : bool = True
        self._initialized : bool = False

    def initialize(self):
        self._initialized = True

    @property
    def enabled(self): return self._enabled

    @enabled.setter
    def enabled(self, value : bool): self._enabled = value

    @property
    def entity(self): return self._entity

    @entity.setter
    def entity(self, value): self._entity = value