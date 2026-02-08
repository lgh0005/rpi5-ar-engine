from objects import Object, Entity
from typing import List

class Scene(Object):
    def __init__(self):
        super().__init__()
        self.entities : List['Entity'] = []

    def add_entity(self, entity):
        self.entities.append(entity)
        return entity

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def get_entity(self, index):
        if 0 <= index < len(self.entities):
            return self.entities[index]
        return None

    def awake(self):
        for entity in self.entities:
            entity.awake()

    def start(self):
        for entity in self.entities:
            entity.start()

    def update(self, dt : float):
        if not self.active: return
        for entity in self.entities:
            entity.update(dt)

    def late_update(self, dt : float):
        if not self.active: return
        for entity in self.entities:
            entity.late_update(dt)