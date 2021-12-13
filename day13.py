from collections import Counter

from puzzle import Puzzle


class Day13(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 13, Part {part}")

    def load(self, input):
        coordinates = []
        for line in input:
            if not line:
                break
            coordinates.append(tuple(map(int, line.split(","))))

        folds = []
        for line in input:
            line = line[len("fold along ") :]
            axis, pos = line.split("=")
            folds.append((axis, int(pos)))

        return coordinates, folds

    def fold(self, coords, fold):
        dim, pos = self.calc_index(fold)
        coords = map(lambda c: self.fold_axis(dim, pos, c), coords)
        return set(coords)

    def calc_index(self, fold):
        axis, pos = fold
        return {"x": 0, "y": 1}[axis], pos

    def fold_axis(self, dim, pos, coord):
        return tuple(
            pos * 2 - c if i == dim and c > pos else c for i, c in enumerate(coord)
        )


class Part1(Day13):
    def __init__(self, part=1):
        super().__init__(part)
        self.total_paths = 0

    def solve(self, input):
        coords, folds = self.load(input)
        coords = self.fold(coords, folds[0])
        return len(coords)


class Part2(Day13):
    def __init__(self, part=2):
        super().__init__(part)
        self.total_paths = 0

    def solve(self, input):
        coords, folds = self.load(input)

        for fold in folds:
            coords = self.fold(coords, fold)

        N_COLS, N_ROWS = 40, 7

        output = []
        for y in range(-1, N_ROWS):
            line = ("█" if (x, y) in coords else "░" for x in range(-1, N_COLS))
            output.append("".join(line))
        return "\n" + "\n".join(output)


def main():
    Part1().check(EXAMPLE1, 17)
    Part1().run("inputs/day13.txt", wrong=[802])
    Part2().run("inputs/day13.txt")


if __name__ == "__main__":
    EXAMPLE1 = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    main()
