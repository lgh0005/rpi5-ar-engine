import OpenGL.GL as gl
from debug import Logger

class Shader:
    def __init__(self):
        self._shader_id = 0

    def __del__(self):
        if self._shader_id:
            gl.glDeleteShader(self._shader_id)
            self._shader_id = 0

    @property
    def id(self):
        return self._shader_id
    
    @classmethod
    def create_from_file(cls, filename, shader_type):
        shader = cls()
        if not shader.load_file(filename, shader_type):
            return None
        return shader
    
    def load_file(self, filename, shader_type):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            Logger.error(f"Failed to open shader file: {filename}")
            return False

        # 1. 셰이더 생성 및 소스 입력
        self._shader_id = gl.glCreateShader(shader_type)
        gl.glShaderSource(self._shader_id, code)
        
        # 2. 컴파일
        gl.glCompileShader(self._shader_id)

        # 3. 에러 체크
        success = gl.glGetShaderiv(self._shader_id, gl.GL_COMPILE_STATUS)
        if not success:
            info_log = gl.glGetShaderInfoLog(self._shader_id)
            Logger.error(f"Failed to compile shader: \"{filename}\"")
            Logger.error(f"Reason: {info_log.decode()}")
            return False
            
        return True