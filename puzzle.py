
class Puzzle:
    def __init__(self, name):
        self.name = name

    def check(self, input, expected):
        result = self.solve(input.splitlines())
        if result == expected:
            print(f"OK  {result}")
        else:
            raise AssertionError(f"expected {expected}, got {result}")

    def run(self, filename):
        with open(filename, "rt") as f:
            result = self.solve(f)
            print(f"{self.name}: {result}")
