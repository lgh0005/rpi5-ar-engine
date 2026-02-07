import sys

class Asserter:
    @staticmethod
    def check(condition: bool, message: str = "Assertion failed"):
        if __debug__:
            assert condition, message