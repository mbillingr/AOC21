import math

from puzzle import Puzzle


class Day22(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 22, Part {part}")

    def parse_input(self, line):
        state, rest = line.split()
        ranges = rest.split(",")
        ranges = (tuple(map(int, r[2:].split('..'))) for r in ranges)
        ranges = map(lambda mm: (mm[0], mm[1] + 1), ranges)
        return state, list(ranges)

    def compute_volume(self, steps):
        steps = list(steps)

        extent = 0
        for _, cube in steps:
            for lo, hi in cube:
                if lo < 0:
                    lo = -lo
                if hi < 0:
                    hi = -hi
                extent = max(extent, lo, hi)

        tree = BspTree((-extent, -extent, -extent), (extent, extent, extent), "off")

        for state, ranges in steps:
            lo = tuple(r[0] for r in ranges)
            hi = tuple(r[1] for r in ranges)
            tree.set_cube(lo, hi, state)
        return tree.compute_volume()


class Part1(Day22):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        steps = map(self.parse_input, input)
        steps = (s for s, _ in zip(steps, range(PART1_LINES)))  # only use first N lines
        return self.compute_volume(steps)


class Part2(Day22):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        steps = list(map(self.parse_input, input))
        return self.compute_volume(steps)


class BspTree:
    def __init__(self, min, max, leaf):
        self.min = min
        self.max = max
        self.leaf = leaf
        self.children = None

    def compute_volume(self):
        if self.leaf == "on":
            volume = 1
            for lo, hi in zip(self.min, self.max):
                volume *= hi - lo
            return volume
        if self.leaf == "off":
            return 0
        return sum(child.compute_volume() for child in self.children)

    def set_cube(self, min, max, state):
        if self.completely_covered(min, max):
            self.leaf = state
            self.children = None
            return

        if self.completely_outside(min, max):
            return

        if self.is_leaf():
            self.split(*self.find_split(min, max))

        for child in self.children:
            child.set_cube(min, max, state)

    def is_leaf(self):
        return self.leaf and self.children is None

    def split(self, axis, center):
        assert self.is_leaf()

        lo = self.min[axis]
        hi = self.max[axis]

        assert lo < center < hi

        self.children = [
            BspTree(self.min, self.max[:axis] + (center,) + self.max[1 + axis:], self.leaf),
            BspTree(self.min[:axis] + (center,) + self.min[1 + axis:], self.max, self.leaf),
        ]

        self.leaf = False

    def find_split(self, min_, max_):
        """split along the largest axis, where the split does not go through the cube"""
        for axis in range(3):
            lo = self.min[axis]
            hi = self.max[axis]
            a, b = min_[axis], max_[axis]

            if hi <= a or lo >= b:
                continue

            if lo < a:
                return axis, a

            if hi > b:
                return axis, b

    def completely_within(self, min, max):
        return all(m >= l for m, l in zip(min, self.min)) and all(m <= u for m, u in zip(max, self.max))

    def completely_outside(self, min, max):
        return any(m >= u for m, u in zip(min, self.max)) or any(m <= l for m, l in zip(max, self.min))

    def completely_covered(self, min, max):
        return all(m <= l for m, l in zip(min, self.min)) and all(m >= u for m, u in zip(max, self.max))


PART1_LINES = 20


def main():
    Part1().check(EXAMPLE1, 39)
    Part1().check(EXAMPLE2, 590784)
    Part1().run("inputs/day22.txt")

    Part2().check(EXAMPLE0, 100000*100001*100000)

    Part2().check(EXAMPLE2, 2758514936282235)
    Part2().run("inputs/day22.txt")


if __name__ == "__main__":
    EXAMPLE0 = """on x=-1..1,y=-1..1,z=-1..1
on x=-100000..-1,y=-50000..50000,z=-100000..-1"""

    EXAMPLE1 = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

    EXAMPLE2 = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""

    main()
