from objects import Object
from managers import OBJECT

class Scene(Object):
    def __init__(self):
        super().__init__()

    def load(self):
        # 1. json파일을 로드 (함수 인자에 json파일 경로를 받아올 수 있음)

        # 2. 적절히 파싱해서 컴포넌트 생성, add_entity를 호출한다.
        pass

    ## TODO : load에 필요한 몇 가지 private 메서드들을 호출한다.
    def _add_entity(self, entity):
        OBJECT.add_entity(entity)
        return entity

    def _remove_entity(self, entity):
        if entity in self.entities:
            OBJECT.destroy_entity(entity)
