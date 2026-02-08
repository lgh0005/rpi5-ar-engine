import glm
from objects import Component
from components import Transform

class Camera(Component):
    def __init__(self):
        super().__init__()

        # 1. 투영 설정 (기본값)
        self.__fov = 45.0
        self.__near = 0.1
        self.__far = 1000.0
        self.__aspect_ratio = 16.0 / 9.0 # TODO : window_manager와 소통 필요
                                         # 뷰포트 크기(윈도우 크기)가 바뀌면 바뀌어야 함

        # 2. 행렬 캐싱
        self.__projection_matrix = glm.mat4(1.0)
        self.__is_camera_dirty = True

# region [Properties]
    @property
    def fov(self): return self.__fov
    @fov.setter
    def fov(self, value):
        self.__fov = value
        self.__is_camera_dirty = True

    @property
    def near(self): return self.__near
    @near.setter
    def near(self, value):
        self.__near = value
        self.__is_camera_dirty = True

    @property
    def far(self): return self.__far
    @far.setter
    def far(self, value):
        self.__far = value
        self.__is_camera_dirty = True

    @property
    def aspect_ratio(self): return self.__aspect_ratio
    @aspect_ratio.setter
    def aspect_ratio(self, value):
        self.__aspect_ratio = value
        self.__is_camera_dirty = True
# endregion

# region [[Matrix Calculations]
    @property
    def projection_matrix(self):
        if self.__is_camera_dirty:
            self.__projection_matrix = glm.perspective(
                glm.radians(self.__fov), 
                self.__aspect_ratio, 
                self.__near, 
                self.__far
            )
            self.__is_camera_dirty = False
        return self.__projection_matrix

    @property
    def view_matrix(self):
        transform = self.entity.get_component(Transform)
        if not transform:
            return glm.mat4(1.0)
            
        return glm.inverse(transform.world_matrix)
# endregion
    