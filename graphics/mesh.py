import numpy as np
import globals
import moderngl
import config

class Mesh:
    def __init__(self, program, vertices, indices, primitive=moderngl.TRIANGLES):
        self.__primitive = primitive
        self.__vbo = globals.RENDER.ctx.buffer(np.array(vertices, dtype='f4').tobytes())
        self.__ibo = globals.RENDER.ctx.buffer(np.array(indices, dtype='i4').tobytes())
        vertex = [
            (
                self.__vbo, 
                '3f 3f 2f 3f', 
                config.VAR_POSITION, 
                config.VAR_NORMAL, 
                config.VAR_TEXCOORD, 
                config.VAR_TANGENT
            )
        ]
        self.__vao = globals.RENDER.ctx.vertex_array(
            program.mgl_program, 
            vertex, 
            self.__ibo
        )

    def draw(self):
        self.__vao.render(self.__primitive)

    def release(self):
        if self.__vbo: self.__vbo.release()
        if self.__ibo: self.__ibo.release()
        if self.__vao: self.__vao.release()