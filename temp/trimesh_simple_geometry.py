import os
import pygame
import moderngl
import numpy as np
import trimesh

os.environ["DISPLAY"] = ":0"

def perspective(fovy, aspect, near, far):
    f = 1.0 / np.tan(fovy / 2.0)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2.0 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype='f4')

def rotate_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype='f4')

def rotate_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype='f4')

pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

screen_size = (800, 600)
pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context(require=300)

# 셰이더 수정: model 행렬 추가 및 법선 변환
prog = ctx.program(
    vertex_shader='''
        #version 300 es
        uniform mat4 mvp;
        uniform mat4 model;
        in vec3 in_vert;
        in vec3 in_normal;
        out vec3 v_normal;
        void main() {
            gl_Position = mvp * vec4(in_vert, 1.0);
            // 법선을 월드 공간으로 변환 (회전 적용)
            v_normal = mat3(model) * in_normal;
        }
    ''',
    fragment_shader='''
        #version 300 es
        precision highp float;
        in vec3 v_normal;
        out vec4 f_color;
        void main() {
            // 고정된 광원 방향 (위쪽, 오른쪽, 앞쪽에서 오는 빛)
            vec3 lightDir = normalize(vec3(0.5, 1.0, 0.5));
            float light = dot(normalize(v_normal), lightDir);
            light = clamp(light, 0.2, 1.0);
            f_color = vec4(vec3(1.0, 0.5, 0.2) * light, 1.0);
        }
    ''',
)

# 다양한 기본 기하학 도형들
# 옵션 1: 큐브 (정육면체)
mesh = trimesh.creation.box(extents=(1.5, 1.5, 1.5))

# 옵션 2: 구 (Icosphere - 정삼각형 기반의 고른 밀도)
# mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)

# 옵션 3: 구 (UV Sphere - 경도/위도 방식의 구)
# mesh = trimesh.creation.uv_sphere(radius=1.0, count=[32, 32])

# 옵션 4: 토러스 (도넛 모양)
# mesh = trimesh.creation.torus(major_radius=1.0, minor_radius=0.4)

# 옵션 5: 실린더 (원기둥)
# mesh = trimesh.creation.cylinder(radius=0.8, height=2.0)

# 옵션 6: 캡슐 (알약 모양)
# mesh = trimesh.creation.capsule(radius=0.5, height=1.5)

# 옵션 7: 원뿔 (Cone)
# mesh = trimesh.creation.cone(radius=1.0, height=2.0)


vertices = mesh.vertices[mesh.faces].reshape(-1, 3).astype('f4')
normals = mesh.vertex_normals[mesh.faces].reshape(-1, 3).astype('f4')
model_data = np.hstack([vertices, normals])

vbo = ctx.buffer(model_data)
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_normal')

proj = perspective(np.radians(45.0), screen_size[0] / screen_size[1], 0.1, 100.0)
view = np.eye(4, dtype='f4')
view[2, 3] = -4.0

angle = 0
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.1, 0.1, 0.1)
    ctx.enable(moderngl.DEPTH_TEST)

    angle += 0.02
    model_mat = rotate_y(angle) @ rotate_x(angle * 0.5)
    mvp = proj @ view @ model_mat
    
    # 셰이더에 model 행렬과 mvp 행렬 모두 전달
    prog['model'].write(model_mat.T.tobytes())
    prog['mvp'].write(mvp.T.tobytes())

    vao.render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()