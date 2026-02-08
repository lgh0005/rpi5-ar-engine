import moderngl
from core.singleton import SingletonMeta
from debug import Logger
from config.opengl import MGL_GL_CONTEXT_VERSION

class RenderManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__ctx = None

    def initialize(self):
        # 1. 기존에 생성된 윈도우의 OpenGL 컨텍스트 감지 및 생성
        self.__ctx = moderngl.create_context(require=MGL_GL_CONTEXT_VERSION)

        # 2. 필수 3D 렌더링 설정 활성화
        # DEPTH_TEST: 깊이 버퍼 사용 (앞의 물체가 뒤를 가림)
        # CULL_FACE: 뒷면(Back-face) 그리기 생략 (성능 최적화)
        self.__ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # GPU 정보 로깅
        if __debug__:
            vendor = self.__ctx.info.get('GL_VENDOR', 'Unknown')
            renderer = self.__ctx.info.get('GL_RENDERER', 'Unknown')
            Logger.info(f"[Render] RenderManager initialized. GPU: {vendor} {renderer}")

    def render(self):
        if self.__ctx:
            self.__ctx.clear(0.1, 0.1, 0.1, 1.0)

    @property
    def ctx(self):
        if self.__ctx is None:
            Logger.error("[Render] Context is NOT initialized! Call initialize() first.")
            return None
        return self.__ctx

    def stop(self):
        Logger.info("[Render] RenderManager stopped.")