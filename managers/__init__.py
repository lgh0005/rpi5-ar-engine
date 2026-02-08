from .window_manager import WindowManager
from .resource_manager import ResourceManager
from .time_manager import TimeManager
from .camera_manager import CameraManager
from .render_manager import RenderManager
from .vision_manager import VisionManager
from .input_manager import InputManager
from .scene_manager import SceneManager
from .ui_manager import UIManager
from .object_manager import ObjectManager

WINDOW = WindowManager()
RESOURCE = ResourceManager()
TIME = TimeManager()
CAMERA = CameraManager()
RENDER = RenderManager()
VISION = VisionManager()
INPUT = InputManager()
SCENE = SceneManager()
UI = UIManager()
OBJECT = ObjectManager()

__all__ = [
    "WINDOW", 
    "RESOURCE", 
    "TIME", 
    "CAMERA", 
    "RENDER", 
    "VISION", 
    "INPUT", 
    "SCENE", 
    "UI",
    "OBJECT"
]
