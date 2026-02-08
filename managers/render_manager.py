import moderngl
from core.singleton import SingletonMeta
from debug import Logger
from config.opengl import MGL_GL_CONTEXT_VERSION

class RenderManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__ctx = None

    def initialize(self):
        self.__ctx = moderngl.create_context(require=MGL_GL_CONTEXT_VERSION)
        self.__ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.__get_mgl_context_info()

    def render(self):
        if self.__ctx:
            self.__ctx.clear(0.1, 0.1, 0.1, 1.0)

    def stop(self):
        Logger.info("[Render] RenderManager stopped.")

# region [OpenGL context getter]
    @property
    def ctx(self):
        if self.__ctx is None:
            Logger.error("[Render] Context is NOT initialized! Call initialize() first.")
            return None
        return self.__ctx
# endregion
    
# region [Debug method]
    def __get_mgl_context_info(self):
        if __debug__:
            vendor = self.__ctx.info.get('GL_VENDOR', 'Unknown')
            renderer = self.__ctx.info.get('GL_RENDERER', 'Unknown')
            Logger.info(f"[Render] RenderManager initialized. GPU: {vendor} {renderer}")
# endregion
