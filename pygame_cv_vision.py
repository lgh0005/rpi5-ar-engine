import os
import pygame
import cv2
import subprocess
import numpy as np

# 라즈베리 파이 연결 모니터 출력을 위한 설정
os.environ["DISPLAY"] = ":0"

# 1. 설정
W, H = 640, 480
FRAME_SIZE = int(W * H * 1.5)

# 2. 초기화
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("RPi5 AR Engine - Camera Preview")
clock = pygame.time.Clock()

# 3. rpicam-vid 실행
cmd = ["rpicam-vid", "-t", "0", "--width", str(W), "--height", str(H), 
       "--codec", "yuv420", "--nopreview", "-o", "-"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=FRAME_SIZE)

running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 4. 데이터 읽기
    raw_data = process.stdout.read(FRAME_SIZE)
    if len(raw_data) != FRAME_SIZE:
        continue

    # 5. 데이터 변환 (YUV -> BGR -> RGB)
    yuv = np.frombuffer(raw_data, dtype=np.uint8).reshape((int(H * 1.5), W))
    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # 6. Pygame Surface로 변환 (축 교환 필수)
    # numpy 배열의 [H, W, C]를 Pygame의 [W, H, C]로 맞춥니다.
    rgb_surface = np.transpose(rgb, (1, 0, 2))
    surface = pygame.surfarray.make_surface(rgb_surface)

    # 7. 화면 출력
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    # 프레임 제한 (CPU 점유율 관리)
    clock.tick(60)

# 자원 해제
process.terminate()
pygame.quit()