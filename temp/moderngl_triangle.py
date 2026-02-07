import pygame
import moderngl
import numpy as np

''' 설명 작성 '''

# 1. Pygame 초기화
pygame.init()

# 2. OpenGL ES 설정 (라즈베리 파이 5 필수 설정)
# 이 부분이 없으면 기본적으로 데스크탑 OpenGL을 찾다가 실패합니다.
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

# 3. 윈도우 생성
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

# 4. ModernGL 컨텍스트 생성
# require=300은 OpenGL ES 3.0을 의미합니다.
ctx = moderngl.create_context(require=300)

# 셰이더 프로그램 (OpenGL ES 3.0 규격, #version 300 es 필수)
prog = ctx.program(
    vertex_shader='''
        #version 300 es
        in vec2 in_vert;
        in vec3 in_color;
        out vec3 v_color;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_color = in_color;
        }
    ''',
    fragment_shader='''
        #version 300 es
        precision highp float;
        in vec3 v_color;
        out vec4 f_color;
        void main() {
            f_color = vec4(v_color, 1.0);
        }
    ''',
)

# 데이터: 위치(x, y), 색상(r, g, b)
vertices = np.array([
    0.0,  0.5, 1.0, 0.0, 0.0,
   -0.5, -0.5, 0.0, 1.0, 0.0,
    0.5, -0.5, 0.0, 0.0, 1.0,
], dtype='f4')

vbo = ctx.buffer(vertices)
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    ctx.clear(0.1, 0.1, 0.1)
    vao.render()
    pygame.display.flip()

pygame.quit()