from puzzle import Puzzle


class Day25(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 25, Part {part}")


class Part1(Day25):
    def __init__(self, part=1):
        super().__init__(part)
        self.east_herd = None
        self.south_herd = None
        self.n_rows = None
        self.n_columns = None

    def parse_input(self, input):
        self.east_herd = set()
        self.south_herd = set()
        for row, line in enumerate(input):
            for col, ch in enumerate(line):
                match ch:
                    case '.': pass
                    case 'v': self.south_herd.add((row, col))
                    case '>': self.east_herd.add((row, col))
                    case _: raise ValueError(f'Unexpected character: {ch}')
        self.n_rows = row + 1
        self.n_columns = col + 1

    def solve(self, input):
        self.parse_input(input)
        n = 1
        while self.step():
            n += 1
        return n

    def step(self):
        any_moved = False
        for herd, move in [(self.east_herd, self.move_east), (self.south_herd, self.move_south)]:
            movers = [cucumber for cucumber in herd if self.is_free(move(cucumber))]
            any_moved = any_moved or bool(movers)
            for cucumber in movers:
                herd.remove(cucumber)
                herd.add(move(cucumber))
        return any_moved

    def is_free(self, pos):
        return pos not in self.east_herd and pos not in self.south_herd

    def move_east(self, pos):
        row, col = pos
        return row, (col + 1) % self.n_columns

    def move_south(self, pos):
        row, col = pos
        return (row + 1) % self.n_rows, col


def main():
    Part1().check(EXAMPLE, 58)
    Part1().run("inputs/day25.txt")


if __name__ == "__main__":
    EXAMPLE = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

    main()
