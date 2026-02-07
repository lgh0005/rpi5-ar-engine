from core.singleton import SingletonMeta
import config.settings as settings
import threading
import cv2

class CameraManager(metaclass=SingletonMeta):
    def __init__(self):
        self.cap = None
        self.current_frame = None
        self.is_running = False
        self.thread = None
        self.lock = None

        self.width = 640
        self.height = 480
        self.fps = 30
        self.camera_index = -1

    def initialize(self):
        self.lock = threading.Lock()
        self.width = settings.CAMERA_WIDTH
        self.height = settings.CAMERA_HEIGHT
        self.fps = settings.CAMERA_FPS

        # 사용 가능한 카메라 인덱스 찾기
        for index in range(10):
            temp_cap = cv2.VideoCapture(index)
            if temp_cap.isOpened():
                ret, frame = temp_cap.read()
                if ret:
                    self.camera_index = index
                    temp_cap.release()
                    break
                else:
                    temp_cap.release()

        if self.camera_index == -1: return

        # 실제 캡처 객체 초기화
        self.cap = cv2.VideoCapture(self.camera_index)

        # 해상도 및 FPS 설정
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

    def start(self):
        if self.cap is None or not self.cap.isOpened():
            return
        
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def update(self):
        pass

    def get_frame(self):
        with self.lock:
            if self.current_frame is None:
                return None
            return self.current_frame.copy()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        
        if self.cap:
            self.cap.release()