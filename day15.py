from more_itertools import peekable
import numpy as np
from collections import deque
import heapq

from tqdm import tqdm

from puzzle import Puzzle


class Day15(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 15, Part {part}")

    def load_array(self, input):
        return np.array(list(map(list, input))).astype(int)

    def path_search(self, grid, start=(0, 0)):
        # dijkstra
        n, m = grid.shape
        goal = n-1, m-1

        min_path_costs = np.inf + np.zeros_like(grid)
        min_path_costs[start] = 0

        queue = [(0, start)]
        heapq.heapify(queue)

        while queue:
            cost, current = heapq.heappop(queue)

            if current == goal:
                return cost

            for npos in neighbors(current, grid.shape):
                tentative_gscore = min_path_costs[current] + grid[npos]
                if tentative_gscore < min_path_costs[npos]:
                    min_path_costs[npos] = tentative_gscore
                    heapq.heappush(queue, (min_path_costs[npos], npos))
        return min_path_costs[goal]


class Part1(Day15):
    def __init__(self, part=1):
        super().__init__(part)
        self.total_flashes = 0

    def solve(self, input):
        grid = self.load_array(input)
        return int(self.path_search(grid))


class Part2(Day15):
    def __init__(self, part=1):
        super().__init__(part)
        self.total_flashes = 0

    def solve(self, input):
        grid = self.load_array(input)

        top_row = np.concatenate([grid+i for i in range(5)], axis=1)
        big_grid = np.concatenate([top_row+i for i in range(5)], axis=0)
        grid = wrap_grid_numbers(big_grid)

        return int(self.path_search(grid))


def wrap_grid_numbers(grid):
    return (grid - 1) % 9 + 1


def neighbors(pos, size):
    x, y = pos

    if x < size[0] - 1:
        yield (x+1, y)

    if y < size[1] - 1:
        yield (x, y+1)

    if x > 0:
        yield (x-1, y)

    if y > 0:
        yield (x, y-1)


def main():
    Part1().check(EXAMPLE_INPUT, 40)
    Part1().run("inputs/day15.txt")
    Part2().check(EXAMPLE_INPUT, 315)
    Part2().run("inputs/day15.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

    main()
