from core.singleton import SingletonMeta
import config.camera as camera
import subprocess
import threading
import cv2
import numpy as np
from debug import Logger, Asserter

class CameraManager(metaclass=SingletonMeta):
    def __init__(self):
        self.rapicam_vid_proc = None
        self.current_frame = None # [주의] 공유 자원
        self.is_running = False
        self.thread = None
        self.lock = threading.Lock()

        self.frame_size = 0
        self.width = 0
        self.height = 0

    def initialize(self):
        # 1. Config에서 설정 로드
        self.width = camera.CAMERA_WIDTH
        self.height = camera.CAMERA_HEIGHT

        # YUV420 프레임 크기 계산: Width * Height * 1.5 바이트
        self.frame_size = int(self.width * self.height * 1.5)
        Logger.info(f"Initializing RPi5 CSI Camera via rpicam-vid CLI ({self.width}x{self.height})...")

        # 2. 명령어 가져오기 및 rpicam-vid 프로세스 시작
        cmd = camera.RPICAM_VID_ENTRY_CMD

        self.rapicam_vid_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, # 불필요한 로그 숨김
                bufsize=self.frame_size * 2, # 버퍼 크기 설정
            )
        Asserter.check(self.rapicam_vid_proc is not None, "Failed to start rpicam-vid process.")
    
        Logger.info("Camera subprocess started successfully.")
        Logger.info("[Camera] CameraManager initialized.")
        self.start()

    def start(self):
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        Logger.info("Camera capture thread started.")

    def _update(self):
        proc = self.rapicam_vid_proc
        f_size = self.frame_size
        while self.is_running and self.rapicam_vid_proc:

            # 1. 파이프에서 정확히 프레임 크기만큼 바이트 읽기 (Blocking)
            raw_data = proc.stdout.read(f_size)

            # 2. 데이터 무결성 검증
            if not raw_data or len(raw_data) != f_size:
                if proc.poll() is not None: # 프로세스가 종료되었는지 확인
                    Logger.warn("Camera process terminated unexpectedly.")
                    break
                continue

            # 3. 바이트 -> Numpy 배열 변환 : YUV420은 높이가 1.5배인 단일 채널 이미지로 간주됨
            yuv = np.frombuffer(raw_data, dtype=np.uint8).reshape((int(self.height * 1.5), self.width))
            bgr_frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

            # 5. 좌우 반전 옵션
            if camera.FLIP_HORIZONTAL:
                bgr_frame = cv2.flip(bgr_frame, 1)

            # 6. 최신 프레임 업데이트 (Thread-Safe)
            with self.lock:
                self.current_frame = bgr_frame

    def get_frame(self):
        with self.lock:
            if self.current_frame is None:
                return None
            return self.current_frame.copy()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        
        if self.rapicam_vid_proc:
            self.rapicam_vid_proc.terminate()
            self.rapicam_vid_proc.wait()
            self.rapicam_vid_proc = None

        Logger.info("[Camera] CameraManager stopped.")