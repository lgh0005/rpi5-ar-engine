import sys

class Logger:

    # 터미널 색상 코드
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def info(message, tag="INFO"):
        if __debug__:
            print(f"{Logger.OKGREEN}[{tag}]{Logger.ENDC} {message}")

    @staticmethod
    def warn(message, tag="WARN"):
        if __debug__:
            print(f"{Logger.WARNING}[{tag}]{Logger.ENDC} {message}")

    @staticmethod
    def error(message, tag="ERROR"):
        print(f"{Logger.FAIL}[{tag}]{Logger.ENDC} {message}", file=sys.stderr)

    @staticmethod
    def debug(message, tag="DEBUG"):
        if __debug__:
            print(f"{Logger.OKBLUE}[{tag}]{Logger.ENDC} {message}")