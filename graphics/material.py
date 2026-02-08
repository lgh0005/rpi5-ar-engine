from graphics.texture import Texture
from config.opengl import (MATERIAL_TEXTURE_BINDINGS, 
    TEX_ALBEDO, TEX_SPECULAR, TEX_NORMAL, TEX_HEIGHT, TEX_EMISSION)
#from managers import RENDER

class Material:
    def __init__(self, 
        albedo=None, specular=None, normal=None, height=None, emission=None
    ):
        self.__textures = {
            TEX_ALBEDO: albedo,
            TEX_SPECULAR: specular,
            TEX_NORMAL: normal,
            TEX_HEIGHT: height,
            TEX_EMISSION: emission
        }
        self.height_scale = 0.05
        self.shininess = 32.0
        self.emission_intensity = 1.0

    def set_texture(self, map_type: str, texture: Texture):
        if map_type in self.__textures:
            self.__textures[map_type] = texture

    ## TODO : 유니폼 변수 선언 정책을 정해야 한다.
    def bind(self, program):

        # 1. 프로그램 사용
        program.use()

        # 2. 텍스처 유닛 바인딩 (순서 고정)
        # 0: Albedo, 1: Specular, 2: Normal, 3: Height, 4: Emission
        for i, slot in enumerate(MATERIAL_TEXTURE_BINDINGS):
            tex = self.__textures[slot]

            # TODO : 해당 슬롯에 텍스쳐가 None인 경우
            # 기본 텍스쳐를 넘겨줘야 할 필요가 있음
            # if tex is None:
            #     tex = RENDER.get_default_texture(slot)

            tex.use(location=i)
            program.set_uniform_int(f"u_material.{slot}_map", i)

        # 3. 추가 파라미터 전달
        program.set_uniform_float("u_material.shininess", self.shininess)
        program.set_uniform_float("u_material.emission_intensity", self.emission_intensity)
        program.set_uniform_float("u_material.height_scale", self.height_scale)
