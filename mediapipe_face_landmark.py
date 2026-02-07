import os
import pygame
import cv2
import subprocess
import numpy as np
import mediapipe as mp

# 라즈베리 파이 모니터 출력 설정
# os.environ["DISPLAY"] = ":0"

# 1. 설정 및 MediaPipe 초기화
W, H = 640, 480
FRAME_SIZE = int(W * H * 1.5)

mp_face_mesh = mp.solutions.face_mesh
# refine_landmarks=True는 눈동자, 입술 디테일을 살려줍니다.
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

# 2. Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("RPi5 AR Engine - Face Mesh")
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
    
    # MediaPipe는 RGB 이미지를 사용합니다.
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    
    # 5. 얼굴 랜드마크 추적
    results = face_mesh.process(rgb)

    # 6. 결과 그리기 (성공적으로 찾았을 경우)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 얼굴 전체에 테셀레이션(그물망) 그리기
            mp_drawing.draw_landmarks(
                image=rgb,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_spec
            )

    # 7. Pygame 렌더링
    # 이미 rgb 변환 상태이므로 transpose만 수행
    surface_data = np.transpose(rgb, (1, 0, 2))
    surface = pygame.surfarray.make_surface(surface_data)
    
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    
    clock.tick(30)

# 8. 종료
process.terminate()
pygame.quit()