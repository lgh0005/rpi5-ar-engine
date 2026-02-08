class Asserter:
    @staticmethod
    def check(condition, message: str = "Assertion failed"):
        if __debug__: assert condition, message