import glm
from objects import Component

class Transform(Component):
    def __init__(self):
        super().__init__()

        # 1. 기본 공간 데이터 (pyglm 타입)
        self.__position = glm.vec3(0.0, 0.0, 0.0)
        self.__scale = glm.vec3(1.0, 1.0, 1.0)
        self.__rotation = glm.quat(1.0, 0.0, 0.0, 0.0)

        # 2. 계층 구조
        self.__parent = None
        self.__children = []

        # 3. 더티 플래그 및 행렬 캐싱
        self.__local_matrix = glm.mat4(1.0)
        self.__world_matrix = glm.mat4(1.0)
        self.__is_transform_dirty = True

    def set_dirty(self):
        stack = [self]

        while stack:
            current = stack.pop()
            if current.__is_transform_dirty:
                continue
            current.__is_transform_dirty = True
            for child in current.children:
                stack.append(child)

# --- [Properties: Position, Scale, Rotation] ---
    @property
    def position(self): return self.__position

    @position.setter
    def position(self, value):
        self.__position = glm.vec3(value)
        self.set_dirty()
    
    @property
    def scale(self): return self.__scale

    @scale.setter
    def scale(self, value):
        self.__scale = glm.vec3(value)
        self.set_dirty()

    @property
    def rotation(self):
        euler_rad = glm.eulerAngles(self.__rotation)
        return glm.vec3(glm.degrees(euler_rad.x), 
                         glm.degrees(euler_rad.y), 
                         glm.degrees(euler_rad.z))

    @rotation.setter
    def rotation(self, value):
        rad = glm.vec3(glm.radians(value[0]), 
                       glm.radians(value[1]), 
                       glm.radians(value[2]))
        self.__rotation = glm.quat(rad)
        self.set_dirty()

# --- [Hierarchy Management] ---
    @property
    def parent(self): return self.__parent

    @parent.setter
    def parent(self, value):
        if self.__parent == value: return
        
        # 기존 부모에서 제거
        if self.__parent and self in self.__parent.children:
            self.__parent.children.remove(self)
        
        self.__parent = value
        
        # 새 부모에 추가
        if self.__parent:
            self.__parent.children.append(self)
        
        self.set_dirty()

    @property
    def children(self): return self.__children

# --- [Matrix Calculation: Lazy Evaluation] ---
    def __update_matrices(self):
        # Local Matrix = T * R * S
        t_mat = glm.translate(glm.mat4(1.0), self.__position)
        r_mat = glm.mat4_cast(self.__rotation)
        s_mat = glm.scale(glm.mat4(1.0), self.__scale)
        
        self.__local_matrix = t_mat * r_mat * s_mat

        # World Matrix = ParentWorld * Local
        if self.__parent:
            self.__world_matrix = self.__parent.world_matrix * self.__local_matrix
        else:
            self.__world_matrix = self.__local_matrix
            
        self.__is_transform_dirty = False

    @property
    def local_matrix(self):
        if self.__is_transform_dirty:
            self.__update_matrices()
        return self.__local_matrix
    
    @property
    def world_matrix(self):
        if self.__is_transform_dirty:
            self.__update_matrices()
        return self.__world_matrix
