
class Puzzle:
    def __init__(self, name):
        self.name = name

    def check(self, input, expected):
        result = self.solve(iter(input.splitlines()))
        if result == expected:
            print(f"OK  {result}")
        else:
            raise AssertionError(f"expected {expected}, got {result}")

    def run(self, filename, wrong=()):
        with open(filename, "rt") as f:
            lines = (l.strip('\n') for l in f)
            result = self.solve(lines)

        if result in wrong:
            raise AssertionError(f"wrong result: {result}")

        print(f"{self.name}: {result}")

