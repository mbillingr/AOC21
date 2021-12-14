from collections import Counter
from itertools import product

import numpy as np

from puzzle import Puzzle


class Day14(Puzzle):
    def __init__(self, part, n_steps):
        super().__init__(f"Day 14, Part {part}")
        self.n_steps = n_steps

    def load(self, input):
        template = next(input)
        next(input)
        rules = dict(tuple(line.split(' -> ')) for line in input)
        self.rules = rules

        self.all_letters = set(self.rules.values())
        self.all_letters |= set(x[0] for x in self.rules.keys())
        self.all_letters |= set(x[1] for x in self.rules.keys())

        return template

    def insertion_step(self, template):
        output = [template[0]]
        for a, b in zip(template, template[1:]):
            c = self.rules.get(a+b, '')
            output.append(c)
            output.append(b)
        return ''.join(output)

    def solve(self, input):
        template = self.load(input)

        for _ in range(self.n_steps):
            template = self.insertion_step(template)

        counts = Counter(template).most_common()
        return counts[0][1] - counts[-1][1]


def main():
    Day14(1, 0).check(EXAMPLE1, 1)
    Day14(1, 1).check(EXAMPLE1, 1)
    Day14(1, 2).check(EXAMPLE1, 5)
    Day14(1, 3).check(EXAMPLE1, 11 - 4)
    Day14(1, 10).check(EXAMPLE1, 1588)
    Day14(1, 10).run("inputs/day14.txt")
    Day14(2, 40).check(EXAMPLE1, 2188189693529)
    Day14(2, 40).run("inputs/day14.txt")


if __name__ == "__main__":
    EXAMPLE1 = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

    main()
