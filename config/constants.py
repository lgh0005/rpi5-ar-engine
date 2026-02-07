from managers.window_manager import WindowManager
from managers.resource_manager import ResourceManager
from managers.time_manager import TimeManager
from managers.camera_manager import CameraManager
from managers.render_manager import RenderManager
from managers.vision_manager import VisionManager
from managers.audio_manager import AudioManager
from managers.input_manager import InputManager
from managers.scene_manager import SceneManager
from managers.ui_manager import UIManager

# Instantiate global manager objects
WINDOW = WindowManager()
INPUT = InputManager()
TIME = TimeManager()
SCENE = SceneManager()
RENDER = RenderManager()
CAMERA = CameraManager()
VISION = VisionManager()
AUDIO = AudioManager()
RESOURCE = ResourceManager()
UI = UIManager()

# static gloabla variables
