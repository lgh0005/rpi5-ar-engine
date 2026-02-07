import os
import pygame
import cv2
import subprocess
import numpy as np
import mediapipe as mp

# 라즈베리 파이 모니터 출력 설정
# os.environ["DISPLAY"] = ":0"

# 1. 설정 및 MediaPipe 포즈 초기화
W, H = 640, 480
FRAME_SIZE = int(W * H * 1.5)

mp_pose = mp.solutions.pose
# model_complexity를 1로 설정하여 라즈베리 파이에서 성능과 정확도의 균형을 맞춥니다.
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# 2. Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("RPi5 AR Engine - Pose Detection")
clock = pygame.time.Clock()

# 3. 카메라 프로세스 시작
cmd = ["rpicam-vid", "-t", "0", "--width", str(W), "--height", str(H), 
       "--codec", "yuv420", "--nopreview", "-o", "-"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=FRAME_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 4. 카메라 데이터 획득 및 변환
    raw_data = process.stdout.read(FRAME_SIZE)
    if len(raw_data) != FRAME_SIZE:
        continue

    yuv = np.frombuffer(raw_data, dtype=np.uint8).reshape((int(H * 1.5), W))
    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    
    # 5. 포즈 추적 실행
    results = pose.process(rgb)

    # 6. 결과 시각화
    if results.pose_landmarks:
        # 관절과 연결선을 이미지 위에 직접 그립니다.
        mp_drawing.draw_landmarks(
            rgb, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        )

    # 7. Pygame 렌더링
    surface_data = np.transpose(rgb, (1, 0, 2))
    surface = pygame.surfarray.make_surface(surface_data)
    
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    
    clock.tick(30)

# 8. 자원 해제
process.terminate()
pygame.quit()