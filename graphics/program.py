import OpenGL.GL as gl
import numpy as np
import glm
from debug import Logger
from graphics.shader import Shader

class Program:
    def __init__(self):
        self._program_id = 0

    def __del__(self):
        if self._program_id:
            gl.glDeleteProgram(self._program_id)
            self._program_id = 0

    def use(self):
        gl.glUseProgram(self._program_id)

    def __link(self, shaders):
        self._program_id = gl.glCreateProgram()

        # Attach
        for shader in shaders:
            gl.glAttachShader(self._program_id, shader.id)

        # Link
        gl.glLinkProgram(self._program_id)

        # Check Errors
        success = gl.glGetProgramiv(self._program_id, gl.GL_LINK_STATUS)
        if not success:
            info_log = gl.glGetProgramInfoLog(self._program_id)
            Logger.error(f"Failed to link program: {info_log.decode()}")
            return False

        for shader in shaders:
            gl.glDetachShader(self._program_id, shader.id)
            
        return True

    @property
    def id(self):
        return self._program_id

# region [Creation Methods (Static Factories)]
    @classmethod
    def create(cls, shaders: list[Shader]):
        program = cls()
        if not program.__link(shaders): return None
        return program

    @classmethod
    def create_from_files(cls, vert_path: str, frag_path: str):
        vs = Shader.create_from_file(vert_path, gl.GL_VERTEX_SHADER)
        fs = Shader.create_from_file(frag_path, gl.GL_FRAGMENT_SHADER)

        if not vs or not fs:
            return None
        
        return cls.create([vs, fs])
# endregion
    
# region [Uniform Setters]
    def set_uniform_bool(self, name: str, value: bool):
        loc = gl.glGetUniformLocation(self._program_id, name)
        gl.glUniform1i(loc, int(value))

    def set_uniform_int(self, name: str, value: int):
        loc = gl.glGetUniformLocation(self._program_id, name)
        gl.glUniform1i(loc, value)

    def set_uniform_float(self, name: str, value: float):
        loc = gl.glGetUniformLocation(self._program_id, name)
        gl.glUniform1f(loc, value)

    def set_uniform_vec2(self, name: str, value: glm.vec2):
        loc = gl.glGetUniformLocation(self._program_id, name)
        gl.glUniform2fv(loc, 1, glm.value_ptr(value))

    def set_uniform_vec3(self, name: str, value: glm.vec3):
        loc = gl.glGetUniformLocation(self._program_id, name)
        gl.glUniform3fv(loc, 1, glm.value_ptr(value))

    def set_uniform_vec4(self, name: str, value: glm.vec4):
        loc = gl.glGetUniformLocation(self._program_id, name)
        gl.glUniform4fv(loc, 1, glm.value_ptr(value))

    def set_uniform_mat4(self, name: str, value: glm.mat4):
        loc = gl.glGetUniformLocation(self._program_id, name)
        gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, glm.value_ptr(value))
# endregion

# region [Array Uniforms]
    def set_uniform_int_array(self, name: str, values: list[int]):
        loc = gl.glGetUniformLocation(self._program_id, name)
        data = np.array(values, dtype=np.int32)
        gl.glUniform1iv(loc, len(values), data)

    def set_uniform_vec3_array(self, name: str, values: list[glm.vec3]):
        loc = gl.glGetUniformLocation(self._program_id, name)
        data = np.array(values, dtype=np.float32)
        gl.glUniform3fv(loc, len(values), data)

    def set_uniform_mat4_array(self, name: str, values: list[glm.mat4]):
        loc = gl.glGetUniformLocation(self._program_id, name)
        data = np.array(values, dtype=np.float32)
        gl.glUniformMatrix4fv(loc, len(values), gl.GL_FALSE, data)
# endregion