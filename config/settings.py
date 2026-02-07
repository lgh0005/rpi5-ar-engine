import os

# 1. 파일 시스템 경로 (Path Settings)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. 디스플레이 & 윈도우 (Window Settings)
WINDOW_TITLE = "RPi5 AR Engine v0.1"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_FPS = 60
USE_FULLSCREEN = False

# 3. 카메라 설정 (Camera Settings)
CAMERA_ID = 0           # 보통 0번이 기본 카메라
CAMERA_WIDTH = 640      # 카메라 하드웨어 해상도
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
FLIP_HORIZONTAL = True  # 거울 모드

# 4. OpenGL & 렌더링 (Render Settings)
GL_MAJOR_VERSION = 3
GL_MINOR_VERSION = 0
DEPTH_SIZE = 24
NUM_SAMPLES = 4         # MSAA (계단현상 제거)

# 5. 디버그 설정 (Debug)
DEBUG = True