# 3. 카메라 설정 (Camera Settings)
CAMERA_ID = 0           # 보통 0번이 기본 카메라
CAMERA_WIDTH = 640      # 카메라 하드웨어 해상도
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
FLIP_HORIZONTAL = True  # 거울 모드
RPICAM_VID_ENTRY_CMD = [
    "rpicam-vid",
    "-t", "0",
    "--width", str(CAMERA_WIDTH),
    "--height", str(CAMERA_HEIGHT),
    "--framerate", str(CAMERA_FPS),
    "--codec", "yuv420",
    "--nopreview",
    "-o", "-"
]