from more_itertools import peekable
import numpy as np

from puzzle import Puzzle


class Day11(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 11, Part {part}")

    def load_array(self, input):
        return np.array(list(map(list, input))).astype(int)


class Part1(Day11):
    def __init__(self, part=1):
        super().__init__(part)
        self.total_flashes = 0

    def solve(self, input):
        grid = self.load_array(input)

        for _ in range(100):
            grid = self.compute_step(grid)
        return self.total_flashes

    def compute_step(self, grid):
        grid += 1

        flashed_this_step = set()

        while True:
            wanna_flash = np.where(grid > 9)
            will_flash = {xy for xy in zip(*wanna_flash) if xy not in flashed_this_step}

            if not will_flash:
                break

            grid = self.flash(grid, will_flash)
            flashed_this_step |= will_flash

        for x, y in flashed_this_step:
            grid[x, y] = 0

        self.total_flashes += len(flashed_this_step)

        return grid

    def flash(self, grid, will_flash):
        grid = np.pad(grid, 1, constant_values=99)
        for x, y in will_flash:
            grid[x : x + 3, y : y + 3] += 1
        return grid[1:-1, 1:-1]


class Part2(Part1):
    def __init__(self, part=2):
        super().__init__(part)

    def solve(self, input):
        grid = self.load_array(input)

        step = 0
        while True:
            step += 1
            grid = self.compute_step(grid)
            if np.all(grid == 0):
                return step


def main():
    Part1().check(EXAMPLE_INPUT, 1656)
    Part1().run("inputs/day11.txt")
    Part2().check(EXAMPLE_INPUT, 195)
    Part2().run("inputs/day11.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

    main()
