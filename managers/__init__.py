from .window_manager import WindowManager
from .resource_manager import ResourceManager
from .time_manager import TimeManager
from .camera_manager import CameraManager
from .render_manager import RenderManager
from .vision_manager import VisionManager
from .audio_manager import AudioManager
from .input_manager import InputManager
from .scene_manager import SceneManager
from .ui_manager import UIManager

WINDOW = WindowManager()
RESOURCE = ResourceManager()
TIME = TimeManager()
CAMERA = CameraManager()
RENDER = RenderManager()
VISION = VisionManager()
AUDIO = AudioManager()
INPUT = InputManager()
SCENE = SceneManager()
UI = UIManager()

__all__ = [
    "WINDOW", 
    "RESOURCE", 
    "TIME", 
    "CAMERA", 
    "RENDER", 
    "VISION", 
    "AUDIO", 
    "INPUT", 
    "SCENE", 
    "UI"
]
