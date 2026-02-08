import glm
from objects import Component

class MeshRenderer(Component):
    def __init__(self):
        super().__init__()
        self._mesh = None
        self._material = None
        self._color = glm.vec4(1.0)

    def render(self, program):
        if self._material:
            self._material.bind(program)

        if self._mesh:
            self._mesh.draw()

# region [MeshRenderer Getters & Setters]
    @property
    def mesh(self): return self._mesh

    @mesh.setter
    def mesh(self, value): self._mesh = value

    @property
    def material(self): return self._material

    @material.setter
    def material(self, value): self._material = value

    @property
    def color(self): return self._color

    @color.setter
    def color(self, value: glm.vec4): self._color = value
# endregion