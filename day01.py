from itertools import islice

from puzzle import Puzzle


class Part1(Puzzle):
    def __init__(self):
        super().__init__("Day 1, Part 1")

    def solve(self, input):
        numbers = (int(x) for x in input)
        pairs = window(numbers, 2)
        is_increment = (1 for a, b in pairs if b > a)
        return sum(is_increment)


class Part2(Puzzle):
    def __init__(self):
        super().__init__("Day 1, Part 2")

    def solve(self, input):
        numbers = (int(x) for x in input)
        smoothed = (sum(x) for x in window(numbers, 3))
        pairs = window(smoothed, 2)
        is_increment = (1 for a, b in pairs if b > a)
        return sum(is_increment)


def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for item in it:
        result = result[1:] + (item,)
        yield result


def main():
    Part1().check(EXAMPLE_INPUT, 7)
    Part1().run("inputs/day01.txt")

    Part2().check(EXAMPLE_INPUT, 5)
    Part2().run("inputs/day01.txt")


if __name__ == '__main__':
    EXAMPLE_INPUT = """199
200
208
210
200
207
240
269
260
263"""

    main()
