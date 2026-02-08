from graphics.texture import Texture
import config
import globals

class Material:
    def __init__(self, 
        albedo=None, specular=None, normal=None, height=None, emission=None
    ):
        self.__textures = {
            config.TEX_ALBEDO: albedo,
            config.TEX_SPECULAR: specular,
            config.TEX_NORMAL: normal,
            config.TEX_HEIGHT: height,
            config.TEX_EMISSION: emission
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
        for i, slot in enumerate(config.MATERIAL_TEXTURE_BINDINGS):
            tex = self.__textures[slot]

            # 텍스처가 None인 경우 RESOURCE에서 기본 텍스처를 가져옴
            if tex is None:
                if slot == config.TEX_NORMAL:
                    # 노멀맵은 평평한 푸른색 텍스처
                    tex = globals.RESOURCE.get_texture('default_normal')
                elif slot == config.TEX_HEIGHT or slot == config.TEX_EMISSION:
                    # 높이맵과 에미션은 검은색 텍스처 (영향 없음)
                    tex = globals.RESOURCE.get_texture('default_black')
                else:
                    # 알베도, 스펙큘러 등 나머지는 흰색 텍스처
                    tex = globals.RESOURCE.get_texture('default_white')

            tex.use(location=i)
            program.set_uniform_int(f"u_material.{slot}_map", i)

        # 3. 추가 파라미터 전달
        program.set_uniform_float("u_material.shininess", self.shininess)
        program.set_uniform_float("u_material.emission_intensity", self.emission_intensity)
        program.set_uniform_float("u_material.height_scale", self.height_scale)
