import os
import globals
import config
from core.singleton import SingletonMeta
from debug import Logger
from graphics import *
from geometries.simple_geometry import SimpleGeometry

## TODO : 하드코딩된 부분들을 조금 수정할 필요가 있음
class ResourceManager(metaclass=SingletonMeta):
    def __init__(self):
        self.__programs = {}
        self.__textures = {}
        self.__meshes = {}
        self.__materials = {}

    def initialize(self):
        self.__load_default_program()
        self.__load_default_textures()
        self.__load_default_meshes()
        self.__load_default_materials()
        Logger.info(f"[Resource] ResourceManager initialized. (Prog:{len(self.__programs)}, Tex:{len(self.__textures)}, Mesh:{len(self.__meshes)}, Mat:{len(self.__materials)})")

    def stop(self):
        self.__textures.clear()
        self.__meshes.clear()
        self.__materials.clear()
        self.__programs.clear()
        Logger.info("[Resource] ResourceManager stopped.")

# region [resource getters & setters]
    def get_texture(self, name: str): return self.__textures.get(name)
    def get_mesh(self, name: str): return self.__meshes.get(name)
    def get_material(self, name: str): return self.__materials.get(name)
    def get_program(self, name: str): return self.__programs.get(name)

    def add_texture(self): pass
    def add_mesh(self): pass
    def add_material(self): pass
    def add_program(self): pass
# endregion

# region [load built-in resources]
    def __load_default_program(self):
        vert_path = os.path.join(config.SHADER_DIR, "simple.vert")
        frag_path = os.path.join(config.SHADER_DIR, "simple.frag")
        if os.path.exists(vert_path) and os.path.exists(frag_path):
            self.__programs['default'] = Program(vert_path, frag_path)
        else:
            Logger.error(f"[Resource] Default shader not found at {vert_path}, {frag_path}")

    def __load_default_textures(self):
        ctx = globals.RENDER.ctx
        self.__textures['default_white'] = ctx.texture((1, 1), 4, data=b'\xff\xff\xff\xff')
        self.__textures['default_black'] = ctx.texture((1, 1), 4, data=b'\x00\x00\x00\xff')
        self.__textures['default_normal'] = ctx.texture((1, 1), 3, data=b'\x80\x80\xff')

    def __load_default_meshes(self):
        program = self.get_program('default')
        if program is None:
            Logger.error("[Resource] Failed to load default meshes: 'default' program is missing.")
            return
        
        self.__meshes['cube'] = SimpleGeometry.create_box(program)
        self.__meshes['icosphere'] = SimpleGeometry.create_icosphere(program)
        self.__meshes['sphere'] = SimpleGeometry.create_uv_sphere(program)
        self.__meshes['torus'] = SimpleGeometry.create_torus(program)
        self.__meshes['cylinder'] = SimpleGeometry.create_cylinder(program)
        self.__meshes['capsule'] = SimpleGeometry.create_capsule(program)
        self.__meshes['cone'] = SimpleGeometry.create_cone(program)

    def __load_default_materials(self):
        default_mat = Material(
            albedo=self.get_texture('default_white'),
            specular=self.get_texture('default_white'),
            normal=self.get_texture('default_normal'),
            height=self.get_texture('default_black'),
            emission=self.get_texture('default_black')
        )

        # 기본 속성 설정
        default_mat.shininess = 32.0
        default_mat.height_scale = 0.0  # 기본은 평평하게
        default_mat.emission_intensity = 0.0

        self.__materials['default'] = default_mat
# endregion