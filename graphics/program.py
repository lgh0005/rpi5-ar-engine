import moderngl
import glm
import numpy as np
from managers import RENDER

class Program:
    def __init__(self, vert_path: str, frag_path: str):
        # 파일 읽기
        with open(vert_path, 'r', encoding='utf-8') as f: vs_source = f.read()
        with open(frag_path, 'r', encoding='utf-8') as f: fs_source = f.read()
        self._program = RENDER.ctx.program(vertex_shader=vs_source, fragment_shader=fs_source)

    @property
    def id(self):
        return self._program.glo if self._program else 0
    
    @property
    def mgl_program(self):
        return self._program
    
# region [Uniform Setters]
    def set_uniform_bool(self, name: str, value: bool):
        if name in self._program:
            self._program[name].value = value

    def set_uniform_int(self, name: str, value: int):
        if name in self._program:
            self._program[name].value = value

    def set_uniform_float(self, name: str, value: float):
        if name in self._program:
            self._program[name].value = value

    def set_uniform_vec3(self, name: str, value: glm.vec3):
        if name in self._program:
            self._program[name].value = tuple(value)

    def set_uniform_mat4(self, name: str, value: glm.mat4):
        if name in self._program:
            self._program[name].write(value)
# endregion

# region [Array Uniforms]
    def set_uniform_mat4_array(self, name: str, values: list[glm.mat4]):
        if name in self._program:
            data = np.array(values, dtype='f4').tobytes()
            self._program[name].write(data)
    # endregion