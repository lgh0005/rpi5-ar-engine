import trimesh
from .geometry_converter import GeometryConverter

class SimpleGeometry:

# region [Public Static Factories]
    @staticmethod
    def create_box(program, extents=(1.0, 1.0, 1.0)):
        t_mesh = trimesh.creation.box(extents=extents)
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)
    
    @staticmethod
    def create_icosphere(program, radius=1.0, subdivisions=3):
        t_mesh = trimesh.creation.icosphere(radius=radius, subdivisions=subdivisions)
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)
    
    @staticmethod
    def create_uv_sphere(program, radius=1.0, count=(32, 32)):
        t_mesh = trimesh.creation.uv_sphere(radius=radius, count=count)
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)
    
    @staticmethod
    def create_torus(program, major_radius=1.0, minor_radius=0.25, major_sections=32, minor_sections=16):
        t_mesh = trimesh.creation.torus(
            major_radius=major_radius, 
            minor_radius=minor_radius, 
            major_sections=major_sections, 
            minor_sections=minor_sections
        )
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)
    
    @staticmethod
    def create_cylinder(program, radius=1.0, height=2.0, sections=32):
        t_mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)
    
    @staticmethod
    def create_capsule(program, height=2.0, radius=1.0, count=(32, 32)):
        t_mesh = trimesh.creation.capsule(height=height, radius=radius, count=count)
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)
    
    @staticmethod
    def create_cone(program, radius=1.0, height=2.0, sections=32):
        t_mesh = trimesh.creation.cone(radius=radius, height=height, sections=sections)
        return GeometryConverter.convert_to_engine_mesh(program, t_mesh)
# endregion

