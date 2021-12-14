from itertools import product

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

        self.all_letters = set(rules.values())
        self.all_letters |= set(x[0] for x in rules.keys())
        self.all_letters |= set(x[1] for x in rules.keys())

        self.all_pairs = {a + b: 0 for a, b in product(self.all_letters, self.all_letters)}

        return template

    def solve(self, input):
        template = self.load(input)

        # optimized based on the observation that the actual locations of the letters in the string does not matter.
        # what matters is just the number of letter-pairs, which produce new letters...

        pair_graph = self.compute_pair_graph()
        pair_counts = count(map(lambda p: p[0] + p[1], zip(template, template[1:])), self.all_pairs)
        letter_counts = count(template, self.all_letters)

        for _ in range(self.n_steps):
            pair_increments = {}
            for pair, n in pair_counts.items():
                if n == 0:
                    continue

                a, c, b = pair_graph[pair]
                left, right = a + c, c + b

                # for every pair in the current string ...

                # ... insert a new letter in the middle ...
                letter_counts[c] += n

                # ... creating two new pairs ...
                pair_increments[left] = pair_increments.get(left, 0) + n
                pair_increments[right] = pair_increments.get(right, 0) + n

                # ... and destroying the original pair
                pair_increments[pair] = pair_increments.get(pair, 0) - n

            for p, i in pair_increments.items():
                pair_counts[p] += i

        counts = [x for x in letter_counts.values() if x > 0]
        return max(counts) - min(counts)

    def compute_pair_graph(self):
        rule_graph = {}
        for a, b in product(self.all_letters, self.all_letters):
            c = self.rules[a+b]
            rule_graph[a + b] = (a, c, b)
        return rule_graph


def count(within, all_items):
    counts = {x: 0 for x in all_items}
    for x in within:
        counts[x] += 1
    return counts


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
