from itertools import islice

from puzzle import Puzzle


class Part1(Puzzle):
    def __init__(self):
        super().__init__("Day 1, Part 1")

    def solve(self, input):
        commands = (x.split() for x in input)
        hpos, depth = 0, 0
        for dir, dist in commands:
            match dir, int(dist):
                case ('forward', n): hpos += n
                case ('down', n): depth += n
                case ('up', n): depth -= n
                case other: raise ValueError(other)
        return hpos * depth


class Part2(Puzzle):
    def __init__(self):
        super().__init__("Day 1, Part 2")

    def solve(self, input):
        commands = (x.split() for x in input)
        hpos, depth, aim = 0, 0, 0
        for dir, dist in commands:
            match dir, int(dist):
                case ('forward', n):
                    hpos += n
                    depth += n * aim
                case ('down', n): aim += n
                case ('up', n): aim -= n
                case other: raise ValueError(other)
        return hpos * depth


def main():
    Part1().check(EXAMPLE_INPUT, 150)
    Part1().run("inputs/day02.txt")

    Part2().check(EXAMPLE_INPUT, 900)
    Part2().run("inputs/day02.txt")


if __name__ == '__main__':
    EXAMPLE_INPUT = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

    main()
