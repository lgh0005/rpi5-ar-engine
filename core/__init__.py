import os
import sys

# 1. 시스템 경로 추가 (Bootstrapping)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# 2. 환경 변수 설정
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# 3. 엔진 기본 정보 설정
__version__ = "0.1.0"
__author__ = "ForPhysicalComputingSubject"

# 4. 전역 설정 가져오기
from config import *

# 5. [디버그] 디버그 모듈 전부 가져오기
from debug import *

# 이 메시지는 엔진이 로드될 때 딱 한 번 출력
Logger.info(f"[CORE] RPi5 AR Engine v{__version__} Initializing...")
Logger.info(f"[CORE] Project Root: {BASE_DIR}")