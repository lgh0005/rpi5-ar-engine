from graphics.program import Program
from graphics.texture import Texture
from config.opengl import MATERIAL_TEXTURE_BINDINGS

class Material:
    def __init__(self, program: Program):
        self.program = program
        self.__textures = { slot: None for slot in MATERIAL_TEXTURE_BINDINGS }
        self.height_scale = 1.0
        self.shininess = 32.0
        self.emission_intensity = 1.0

    def set_texture(self, map_type: str, texture: Texture):
        if map_type in self.__textures:
            self.__textures[map_type] = texture

    ## TODO : 유니폼 변수 선언 정책을 정해야 한다.
    def bind(self):

        # 1. 프로그램 사용
        self.program.use()

        # 2. 텍스처 유닛 바인딩 (순서 고정)
        # 0: Albedo, 1: Specular, 2: Normal, 3: Height, 4: Emission
        mat_tex_slots = MATERIAL_TEXTURE_BINDINGS
        for i, slot in enumerate(mat_tex_slots):
            tex = self.__textures[slot]

            if tex:
                tex.use(location=i)
                self.program.set_uniform_int(f"u_{slot}_map", i)
                self.program.set_uniform_bool(f"u_has_{slot}_map", True)
            else:
                self.program.set_uniform_bool(f"u_has_{slot}_map", False)

        # 3. 추가 파라미터 전달
        self.program.set_uniform_float("u_shininess", self.shininess)
        self.program.set_uniform_float("u_emission_intensity", self.emission_intensity)
        self.program.set_uniform_float("u_height_scale", self.height_scale)
