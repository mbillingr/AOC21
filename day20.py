import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from puzzle import Puzzle


POWERS_OF_TWO = 2**np.arange(9)[::-1]


class Day20(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 18, Part {part}")

    def load(self, input):
        self.lookup = np.array([{'.': 0, '#': 1}[ch] for ch in next(input)])
        _ = next(input)
        self.initial_grid = np.array([[{'.': 0, '#': 1}[ch] for ch in row] for row in input])

    def compute_neighborhood_code(self, grid, inf_val=0):
        grid = np.pad(grid, 2, constant_values=inf_val)

        n, m = grid.shape

        view = sliding_window_view(grid, (3, 3)).reshape(n-2, m-2, 9)
        indices = np.sum(view * [POWERS_OF_TWO], axis=-1)

        return self.lookup[indices]

    def crop(self, grid, inf_val):
        if np.all(grid[0, :] == inf_val): grid = grid[1:, :]
        if np.all(grid[-1, :] == inf_val): grid = grid[:-1, :]
        if np.all(grid[:, 0] == inf_val): grid = grid[:, 1:]
        if np.all(grid[:, -1] == inf_val): grid = grid[:, :-1]
        return grid


class Part1(Day20):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        self.load(input)
        inf_val = 0
        step1 = self.compute_neighborhood_code(self.initial_grid, inf_val=inf_val)

        inf_val = self.lookup[inf_val*511]
        step2 = self.compute_neighborhood_code(step1, inf_val=inf_val)
        return np.sum(step2)


class Part2(Day20):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        self.load(input)

        grid = self.initial_grid
        inf_val = 0

        for _ in range(50):
            grid = self.compute_neighborhood_code(grid, inf_val=inf_val)
            inf_val = self.lookup[inf_val*511]
            grid = self.crop(grid, inf_val)
        return np.sum(grid)


def main():
    Part1().check(EXAMPLE_INPUT, 35)
    Part1().run("inputs/day20.txt")

    Part2().check(EXAMPLE_INPUT, 3351)
    Part2().run("inputs/day20.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

    main()
