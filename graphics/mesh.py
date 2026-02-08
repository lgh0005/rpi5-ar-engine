import numpy as np
from managers import RENDER
from config.opengl import VAR_POSITION, VAR_NORMAL, VAR_TEXCOORD, VAR_TANGENT

class Mesh:
    def __init__(self, program, vertices, indices, primitive):
        self.__primitive = primitive
        self.__vao = RENDER.ctx.vertex_array(
            program.mgl_program, 
            [
                self.__vbo,
                '3f 3f 2f 3f',
                VAR_POSITION, VAR_NORMAL, VAR_TEXCOORD, VAR_TANGENT
            ], 
            self.__ibo
        )
        self.__vbo = RENDER.ctx.buffer(np.array(vertices, dtype='f4').tobytes())
        self.__ibo = RENDER.ctx.buffer(np.array(indices, dtype='i4').tobytes())

    def draw(self):
        self.__vao.render(self.__primitive)

    def release(self):
        if self.__vbo: self.__vbo.release()
        if self.__ibo: self.__ibo.release()
        if self.__vao: self.__vao.release()