import numpy as np
import trimesh
from graphics.mesh import Mesh

class GeometryConverter:

    @staticmethod
    def convert_to_engine_mesh(program, t_mesh):
        # 1. UV 데이터 생성 및 정점 분리
        # Primitives는 기본적으로 정점을 공유하므로, 면마다 독립된 UV를 갖도록 분리함
        if not hasattr(t_mesh.visual, 'uv') or t_mesh.visual.uv is None:
            t_mesh = trimesh.visual.texture.unmerge_faces(t_mesh)

        # 2. 데이터 추출 (float32)
        vertices = t_mesh.vertices.astype('f4')
        normals = t_mesh.vertex_normals.astype('f4')
        
        # UV 데이터 확보 (없을 경우 0으로 채움)
        has_uv = hasattr(t_mesh.visual, 'uv') and t_mesh.visual.uv is not None
        uvs = t_mesh.visual.uv.astype('f4') if has_uv else np.zeros((len(vertices), 2), dtype='f4')

        # 3. 탄젠트 계산
        # trimesh 객체에 탄젠트 정보가 있으면 가져오고, 없으면 0으로 채움
        has_tangents = hasattr(t_mesh, 'vertex_tangents') and t_mesh.vertex_tangents is not None
        tangents = t_mesh.vertex_tangents.astype('f4') if has_tangents else np.zeros((len(vertices), 3), dtype='f4')

        # 4. 데이터 패킹 및 인덱스 추출
        packed_data = np.column_stack([vertices, normals, uvs, tangents]).flatten()
        indices = t_mesh.faces.flatten().astype('i4')

        return Mesh(program, packed_data, indices)