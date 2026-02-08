import uuid

class Object:
    def __init__(self):
        self.__active : bool = True
        self.__uuid : uuid.UUID = uuid.uuid4()

    def awake(self): pass
    def start(self): pass
    def update(self, dt : float): pass
    def late_update(self, dt : float): pass  

    @property
    def active(self): return self.__active

    @active.setter
    def active(self, value : bool): self.__active = value

    @property
    def uuid(self): return self.__uuid
