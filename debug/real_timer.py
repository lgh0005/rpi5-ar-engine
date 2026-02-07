import time

class RealTimer:
    def __init__(self, label: str = "Block"):
        if __debug__:
            self.label = label
            self.start_time = 0

    def __enter__(self):
        if __debug__:
            self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args):
        if __debug__:
            elapsed = (time.perf_counter() - self.start_time) * 1000.0

            # 한 프레임 내부에 동작이 완료될 때
            color = '\033[94m'

            # 16.6ms 초과 시 경고 색상 변경
            if elapsed > 16.6: color = '\033[93m'

            print(f"{color}[TIMER] {self.label}: {elapsed:.4f} ms\033[0m")
