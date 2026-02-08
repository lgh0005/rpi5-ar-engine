import pygame
import moderngl
from managers import RENDER

class Texture:
    def __init__(self, path: str, components=4):

        # 1. Pygame을 이용한 이미지 로드 (상하 반전)
        surface = pygame.image.load(path)
        surface = pygame.transform.flip(surface, False, True)

        # 2. 이미지 데이터를 바이트 형태로 변환
        format_str = "RGBA" if components == 4 else "RGB"
        image_data = pygame.image.tostring(surface, format_str)
        width, height = surface.get_size()

        # 3. ModernGL 텍스처 생성
        self.__texture = RENDER.ctx.texture(
            size=(width, height),
            components=components,
            data=image_data
        )

       # 4. 기본 설정 적용 (Mipmap 및 Wrap)
        self.set_mipmap()
        self.set_wrap()

    def set_wrap(self, s=True, t=True):
        self.__texture.repeat_x = s
        self.__texture.repeat_y = t

    def set_mipmap(self, enable=True):
        if enable:
            self.__texture.build_mipmaps()
            self.__texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        else:
            self.__texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

    def use(self, location: int = 0):
        self.__texture.use(location=location)

    def release(self):
        if self.__texture:
            self.__texture.release()

    @property
    def id(self):
        return self.__texture.glo

    @property
    def size(self):
        return self.__texture.size