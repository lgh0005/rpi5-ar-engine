import os
import trimesh
from debug import Logger
from .geometry_converter import GeometryConverter

class ModelLoader:

    @staticmethod
    def load(program, file_path: str, normalize: bool = False):

        # 1. 파일 존재 여부 확인
        if not os.path.exists(file_path):
            Logger.error(f"[ModelLoader] File not found: {file_path}")
            return None
        
        # 2. trimesh로 로드
        data = trimesh.load(file_path)

        # 3. Scene 객체일 경우 단일 Mesh로 병합
        if isinstance(data, trimesh.Scene):
            t_mesh = trimesh.util.concatenate(data.dump())
        else:
            t_mesh = data

        # 4. 위치 및 크기 정규화
        if normalize:
            t_mesh.apply_translation(-t_mesh.centroid) # 원점으로 이동
            scale = 2.0 / t_mesh.extents.max()         # 가장 긴 축을 2.0에 맞춤
            t_mesh.apply_scale(scale)
        
        # 5. 엔진 포맷으로 변환
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)