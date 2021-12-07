import numpy as np

from puzzle import Puzzle


class Day07(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 7, Part {part}")


class Part1(Day07):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        numbers = np.array(list(map(int, next(input).split(','))))
        candidate_pos = np.median(numbers)
        return int(self.compute_fuel(numbers, candidate_pos))

    def compute_fuel(self, numbers, pos):
        return np.sum(np.abs(numbers - pos))


class Part2(Day07):
    def __init__(self, part=2):
        super().__init__(part)

    def solve(self, input):
        numbers = np.array(list(map(int, next(input).split(','))))
        candidate_pos = int(np.round(np.mean(numbers)))
        all_costs = []
        for p in range(candidate_pos-1, candidate_pos+1):
            fc = self.compute_fuel(numbers, p)
            all_costs.append(fc)
        return int(np.min(all_costs))

    def compute_fuel(self, numbers, pos):
        dist = np.abs(numbers - pos)
        cost = dist * (dist + 1) / 2
        return np.sum(cost)


def main():
    Part1().check(EXAMPLE_INPUT, 37)
    Part1().run("inputs/day07.txt")
    Part2().check(EXAMPLE_INPUT, 168)
    Part2().run("inputs/day07.txt")


if __name__ == '__main__':
    EXAMPLE_INPUT = """16,1,2,0,4,2,7,1,2,14"""

    main()
