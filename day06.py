import numpy as np

from puzzle import Puzzle


class Day06(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 6, Part {part}")


class Part1(Day06):
    def __init__(self, n_steps, part=1):
        super().__init__(part)
        self.n_steps = n_steps

    def solve(self, input):
        school = School(8)
        for x in map(int, next(input).split(',')):
            school.add_fish(x)
        for _ in range(self.n_steps):
            school.step()
        return school.total_fish()


class School:
    def __init__(self, max_timer):
        self.fish_with_time = [0] * (1 + max_timer)
        self.times = tuple(range(1+max_timer))

    def add_fish(self, timer, n=1):
        self.fish_with_time[timer] += n

    def total_fish(self):
        return sum(self.fish_with_time)

    def step(self):
        updated_fish = []
        for t in self.times[:-1]:
            # decrease timer of all fish
            updated_fish.append(self.fish_with_time[t+1])
        # 0-timer fish spawn one new fish
        updated_fish.append(self.fish_with_time[0])
        # wrap 0-timer fish spawn
        updated_fish[6] += self.fish_with_time[0]
        self.fish_with_time = updated_fish


def main():
    Part1(0).check(EXAMPLE_INPUT, 5)
    Part1(18).check(EXAMPLE_INPUT, 26)
    Part1(80).check(EXAMPLE_INPUT, 5934)
    Part1(80).run("inputs/day06.txt")
    Part1(256, part=2).check(EXAMPLE_INPUT, 26984457539)
    Part1(256, part=2).run("inputs/day06.txt")


if __name__ == '__main__':
    EXAMPLE_INPUT = """3,4,3,1,2"""

    main()
