import numpy as np

from puzzle import Puzzle


class Day09(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 9, Part {part}")

    def load_array(self, input):
        return np.array(list(list(x) for x in input)).astype(int)


class Part1(Day09):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        data = self.load_array(input)
        return (data[minima(data)] + 1).sum()


def minima(data):
    padded = np.pad(data, 1, constant_values=99)
    d0, d1 = gradient(padded)
    is_minimum = (
        (d0[1:, 1:-1] > 0)
        & (d0[:-1, 1:-1] < 0)
        & (d1[1:-1, 1:] > 0)
        & (d1[1:-1, :-1] < 0)
    )
    return is_minimum


def gradient(data):
    d0 = data[1:, :] - data[:-1, :]
    d1 = data[:, 1:] - data[:, :-1]
    return d0, d1


class Part2(Day09):
    def __init__(self, part=2):
        super().__init__(part)

    def solve(self, input):
        data = self.load_array(input)
        seeds = list(zip(*np.where(minima(data))))

        basin_sizes = []
        for seed in seeds:
            basin = find_basin(seed, data)
            basin_sizes.append(basin.sum())

        basin_sizes = sorted(basin_sizes)
        return np.prod(basin_sizes[-3:])


def find_basin(seed, data):
    rows, cols = data.shape
    basin = np.zeros_like(data)
    queue = [seed]
    while queue:
        pos = queue.pop()
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= rows or pos[1] >= cols:
            continue
        if basin[pos]:
            continue
        if data[pos] >= 9:
            continue
        basin[pos] = True
        queue.append((pos[0] - 1, pos[1]))
        queue.append((pos[0] + 1, pos[1]))
        queue.append((pos[0], pos[1] - 1))
        queue.append((pos[0], pos[1] + 1))
    return basin


def main():
    Part1().check(EXAMPLE_INPUT, 15)
    Part1().run("inputs/day09.txt")
    Part2().check(EXAMPLE_INPUT, 1134)
    Part2().run("inputs/day09.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678"""

    main()
