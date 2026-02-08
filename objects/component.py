from objects import Object

class Component(Object):
    def __init__(self):
        super().__init__()
        self.entity = None
        self.enabled = True

    def on_enable(self): pass
    def on_disable(self): pass

    @property
    def enabled(self): return self._enabled

    @enabled.setter
    def enabled(self, value):
        if self._enabled != value:
            self._enabled = value
            if value: self.on_enable()
            else: self.on_disable()

    @property
    def entity(self): return self._entity

    @entity.setter
    def entity(self, value): self._entity = value
