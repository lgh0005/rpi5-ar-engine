import numpy as np
from graphics.mesh import Mesh
from debug import Logger

class GeometryConverter:

    @staticmethod
    def convert_to_engine_mesh(program, t_mesh):
        # 1. 정점 분리
        # 게임 엔진에서는 큐브의 각 면이 독립된 노멀(Flat Shading)과 UV를 가지려면
        # 정점을 공유하면 안 됩니다. (8개 점 -> 24개 점으로 분리)
        # 이 함수가 기존의 잘못된 unmerge_faces 호출을 대체합니다.
        t_mesh.unmerge_vertices()

        # 2. 데이터 추출 (float32로 변환)
        # unmerge_vertices()를 했으므로 vertices 개수가 늘어난 상태입니다.
        vertices = t_mesh.vertices.astype('f4')
        
        # Normals 처리
        # trimesh가 자동으로 계산해주지만, 없을 경우를 대비해 계산 요청
        if t_mesh.vertex_normals is None:
            t_mesh.fix_normals()
        normals = t_mesh.vertex_normals.astype('f4')
        
        # 3. UV 데이터 확보
        # t_mesh.visual이 TextureVisuals가 아닐 수도 있으므로 안전하게 접근
        uvs = None
        if hasattr(t_mesh.visual, 'uv') and t_mesh.visual.uv is not None:
            # UV 개수가 정점 개수와 맞는지 확인
            if len(t_mesh.visual.uv) == len(vertices):
                uvs = t_mesh.visual.uv.astype('f4')
            else:
                Logger.warning(f"[Geometry] UV count mismatch. Verts:{len(vertices)}, UVs:{len(t_mesh.visual.uv)}")

        # UV가 없거나 개수가 안 맞으면 0으로 채움
        if uvs is None:
            uvs = np.zeros((len(vertices), 2), dtype='f4')

        # 4. 탄젠트(Tangent) 계산
        # Normal Map을 쓸 거면 필요합니다. 없으면 0으로 채움.
        tangents = None
        if hasattr(t_mesh, 'vertex_tangents') and t_mesh.vertex_tangents is not None:
             if len(t_mesh.vertex_tangents) == len(vertices):
                tangents = t_mesh.vertex_tangents.astype('f4')

        if tangents is None:
            tangents = np.zeros((len(vertices), 3), dtype='f4')

        # 5. 데이터 패킹 (Interleaved Layout: V, N, UV, T)
        # OpenGL 버퍼에 한 번에 넣기 위해 1차원 배열로 폅니다.
        # shape: (Vertex Count, 3+3+2+3) -> (Vertex Count, 11)
        packed_data = np.column_stack([vertices, normals, uvs, tangents]).flatten()
        
        # 6. 인덱스 추출
        indices = t_mesh.faces.flatten().astype('i4')

        # Mesh 객체 생성 및 반환
        return Mesh(program, packed_data, indices)