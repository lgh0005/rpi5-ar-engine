import globals

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

def create_managers():
    _window = WindowManager()
    _resource = ResourceManager()
    _time = TimeManager()
    _camera = CameraManager()
    _render = RenderManager()
    _vision = VisionManager()
    _input = InputManager()
    _scene = SceneManager()
    _ui = UIManager()
    _object = ObjectManager()

    globals.WINDOW = _window
    globals.RESOURCE = _resource
    globals.TIME = _time
    globals.CAMERA = _camera
    globals.RENDER = _render
    globals.VISION = _vision
    globals.INPUT = _input
    globals.SCENE = _scene
    globals.UI = _ui
    globals.OBJECT = _object
    