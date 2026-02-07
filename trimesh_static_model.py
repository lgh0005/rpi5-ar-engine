import os
import pygame
import moderngl
import numpy as np
import trimesh

''' used model : https://free3d.com/3d-model/low-poly-tree-449895.html '''

# 라즈베리 파이 디스플레이 설정
# os.environ["DISPLAY"] = ":0"

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

# 1. FBX 파일 로드 함수
def load_fbx_model(file_path):
    # FBX 파일을 로드합니다. (보통 Scene 객체로 반환됨)
    scene = trimesh.load(file_path)
    
    # Scene에 포함된 모든 메쉬를 하나의 메쉬로 합칩니다.
    # dump()는 계층 구조의 모든 변환을 적용한 메쉬 리스트를 반환합니다.
    mesh = trimesh.util.concatenate(scene.dump())
    
    # 모델을 원점으로 이동시키고 크기를 정규화합니다.
    mesh.apply_translation(-mesh.centroid)
    scale = 2.0 / mesh.extents.max()
    mesh.apply_scale(scale)
    
    return mesh

# 2. 초기화
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

screen_size = (800, 600)
pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context(require=300)

# 3. 셰이더 프로그램
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
            v_normal = mat3(model) * in_normal;
        }
    ''',
    fragment_shader='''
        #version 300 es
        precision highp float;
        in vec3 v_normal;
        out vec4 f_color;
        void main() {
            vec3 lightDir = normalize(vec3(0.5, 1.0, 0.5));
            float light = dot(normalize(v_normal), lightDir);
            light = clamp(light, 0.3, 1.0);
            f_color = vec4(vec3(0.4, 0.7, 0.3) * light, 1.0);
        }
    ''',
)

# 4. 실제 FBX 모델 데이터 처리
# 'tree.fbx' 파일이 해당 경로에 있어야 합니다.
fbx_path = 'tree.glb'
mesh = load_fbx_model(fbx_path)

# 정점 및 법선 데이터 평탄화
vertices = mesh.vertices[mesh.faces].reshape(-1, 3).astype('f4')
normals = mesh.vertex_normals[mesh.faces].reshape(-1, 3).astype('f4')
model_data = np.hstack([vertices, normals])

vbo = ctx.buffer(model_data)
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_normal')

# 5. 렌더링 루프
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

    angle += 0.01
    model_mat = rotate_y(angle)
    mvp = proj @ view @ model_mat
    
    prog['model'].write(model_mat.T.tobytes())
    prog['mvp'].write(mvp.T.tobytes())

    vao.render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()