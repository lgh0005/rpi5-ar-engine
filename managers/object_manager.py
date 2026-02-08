from debug import Logger
from core.singleton import SingletonMeta
from objects.object import Object
from objects.component import Component

class ObjectManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__pending_add_queue = []
        self.__pending_destroy_queue = []
        self.__entity_queue = []
        self.__component_registry = {}

    def initialize(self):
        # import components
        all_types = self._get_all_subclasses(Component)
        for cls in all_types:
            self.__component_registry[cls] = []
        Logger.info(f"[Object] ObjectManager initialized. : {len(self.__component_registry)}")

    def _get_all_subclasses(self, cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(self._get_all_subclasses(subclass))
        return list(set(all_subclasses))

    def add_entity(self, entity):
        if entity.state != Object.ObjectState.PENDING_ADD:
            entity.state = Object.ObjectState.PENDING_ADD
            self.__pending_add_queue.append(entity)

    def destroy_entity(self, entity):
        if entity.state != Object.ObjectState.PENDING_REMOVE:
            entity.state = Object.ObjectState.PENDING_REMOVE
            self.__pending_destroy_queue.append(entity)
    
    def flush(self): 
        self._process_pending_destroy_queue()
        self._process_pending_add_queue()

    def _process_pending_destroy_queue(self):
        while self.__pending_destroy_queue:
            target_entity = self.__pending_destroy_queue.pop(0)
            
            # 레지스트리에서 해당 엔티티의 모든 컴포넌트 제거
            for comp in target_entity.components.values():
                cls = type(comp)
                if cls in self.__component_registry:
                    self.__component_registry[cls].remove(comp)
                comp.on_destroy()
                comp.state = Object.ObjectState.DESTROYED

            # 활성 큐에서 제거
            if target_entity in self.__entity_queue:
                self.__entity_queue.remove(target_entity)
            target_entity.on_destroy()
            target_entity.state = Object.ObjectState.DESTROYED

    def _process_pending_add_queue(self):
        while self.__pending_add_queue:
            new_entity = self.__pending_add_queue.pop(0)

            # Entity가 오버라이드한 awake() 호출
            new_entity.awake()

            # 컴포넌트들을 전역 레지스트리에 등록
            for comp in new_entity.components.values():
                cls = type(comp)
                if cls in self.__component_registry:
                    self.__component_registry[cls].append(comp)
                comp.state = Object.ObjectState.ACTIVE

            new_entity.start()

            new_entity.state = Object.ObjectState.ACTIVE
            self.__entity_queue.append(new_entity)

    def get_components(self, component_cls):
        return self.__component_registry[component_cls]
    
    def update(self, dt):
        # 1. update 호출
        for entity in self.__entity_queue:
            if not entity.active: continue
            entity.update(dt)
        
        # 2. late_udpate 호출
        for entity in self.__entity_queue:
            if not entity.active: continue
            entity.late_update(dt)

    def stop(self):
        self.__pending_add_queue.clear()
        self.__pending_destroy_queue.clear()
        self.__entity_queue.clear()
        self.__component_registry.clear()
        Logger.info("[Object] ObjectManager stopped.")