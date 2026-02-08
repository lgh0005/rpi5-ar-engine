import os

# 1. 파일 시스템 경로 (Path Settings)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. 주요 엔진 경로
## TODO : 이후에 적절한 경로 추가 필요. 현재 코드는 예시 경로
INTERNAL_RES_DIR = os.path.join(BASE_DIR, "internal")
SHADER_DIR = os.path.join(INTERNAL_RES_DIR, "shaders")