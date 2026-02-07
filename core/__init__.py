import os
import sys

# 1. 환경 변수 설정
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# 2. 엔진 기본 정보 설정
__version__ = "0.1.0"
__author__ = "ForPhysicalComputingSubject"

# 3. 시스템 경로 추가
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 이 메시지는 엔진이 로드될 때 딱 한 번 출력
print(f"[CORE] RPi5 AR Engine v{__version__} Initializing...")