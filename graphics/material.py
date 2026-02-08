from graphics.program import Program
from graphics.texture import Texture
from config.opengl import TEX_ALBEDO, TEX_SPECULAR, TEX_NORMAL, TEX_HEIGHT, TEX_EMISSION

class Material:
    def __init__(self, program: Program):
        self.program = program

        self.textures = {
            TEX_ALBEDO : None,
            TEX_SPECULAR : None,
            TEX_NORMAL : None,
            TEX_HEIGHT : None,
            TEX_EMISSION : None
        }

        self.height_scale = 1.0
        self.shininess = 32.0
        self.emission_intensity = 1.0

    def set_texture(self, map_type: str, texture: Texture):
        if map_type in self.textures:
            self.textures[map_type] = texture

    ## TODO : 유니폼 변수 정책을 정해야 한다.
    def bind(self):

        # 1. 프로그램 사용
        self.program.use()

        # 2. 텍스처 유닛 바인딩 (순서 고정)
        # 0: Albedo, 1: Specular, 2: Normal, 3: Height, 4: Emission
        mat_tex_slots = ['albedo', 'specular', 'normal', 'height', 'emission']
        for i, slot in enumerate(mat_tex_slots):
            tex = self.textures[slot]

            ## TODO : 이후에 셰이더 안에서 머티리얼 구조체 블록으로 감싼
            ## 유니폼 변수 선언이 필요함

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
