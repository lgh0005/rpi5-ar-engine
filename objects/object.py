from enum import IntEnum
import uuid

class Object:

    class ObjectState(IntEnum):
        INITIALIZING = 0
        PENDING_ADD = 1
        ACTIVE = 2
        PENDING_REMOVE = 3
        DESTROYED = 4

    def __init__(self):
        self.__active = True
        self.__uuid = uuid.uuid4()
        self.__state = Object.ObjectState.INITIALIZING

    def awake(self): pass
    def start(self): pass
    def update(self, dt): pass
    def late_update(self, dt): pass  
    def on_destroy(self): pass

    @property
    def active(self): return self.__active

    @active.setter
    def active(self, value): self.__active = value

    @property
    def uuid(self): return self.__uuid

    @property
    def state(self): return self.__state

    @state.setter
    def state(self, value): self.__state = value

