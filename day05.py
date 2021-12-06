import numpy as np

from puzzle import Puzzle


class Day05(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 5, Part {part}")

    def parse_line(self, line):
        nums = ','.join(line.split(' -> '))
        xa, ya, xb, yb = map(int, nums.split(','))
        return xa, ya, xb, yb


class Part1(Day05):
    def __init__(self):
        super().__init__(1)

    def solve(self, input):
        field = np.zeros((999, 999), dtype=int)
        maxx, maxy = 0, 0
        for line in input:
            x1, y1, x2, y2 = self.parse_line(line)
            maxx = max(maxx, x1, x2)
            maxy = max(maxy, y1, y2)
            if x1 == x2:
                y1, y2 = sorted([y1, y2])
                field[x1, y1:y2+1] += 1
            if y1 == y2:
                x1, x2 = sorted([x1, x2])
                field[x1:x2+1, y1] += 1
        field = field[:maxx+1, :maxy+1]

        return np.sum(field > 1)


class Part2(Day05):
    def __init__(self):
        super().__init__(2)

    def solve(self, input):
        field = np.zeros((999, 999), dtype=int)
        maxx, maxy = 0, 0
        for line in input:
            x1, y1, x2, y2 = self.parse_line(line)
            maxx = max(maxx, x1, x2)
            maxy = max(maxy, y1, y2)
            dx = np.sign(x2 - x1)
            dy = np.sign(y2 - y1)
            while x1 != x2 or y1 != y2:
                field[x1, y1] += 1
                x1 += dx
                y1 += dy
            field[x2, y2] += 1
        field = field[:maxx+1, :maxy+1]

        return np.sum(field > 1)


def main():
    Part1().check(EXAMPLE_INPUT, 5)
    Part1().run("inputs/day05.txt")

    Part2().check(EXAMPLE_INPUT, 12)
    Part2().run("inputs/day05.txt")


if __name__ == '__main__':
    EXAMPLE_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

    main()
