from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from managers.window_manager import WindowManager
    from managers.resource_manager import ResourceManager
    from managers.time_manager import TimeManager
    from managers.camera_manager import CameraManager
    from managers.render_manager import RenderManager
    from managers.vision_manager import VisionManager
    from managers.input_manager import InputManager
    from managers.scene_manager import SceneManager
    from managers.ui_manager import UIManager
    from managers.object_manager import ObjectManager

# 실제 인스턴스가 저장될 변수
WINDOW: Optional['WindowManager'] = None
RESOURCE: Optional['ResourceManager'] = None
TIME: Optional['TimeManager'] = None
CAMERA: Optional['CameraManager'] = None
RENDER: Optional['RenderManager'] = None
VISION: Optional['VisionManager'] = None
INPUT: Optional['InputManager'] = None
SCENE: Optional['SceneManager'] = None
UI: Optional['UIManager'] = None
OBJECT: Optional['ObjectManager'] = None