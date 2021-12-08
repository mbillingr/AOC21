from puzzle import Puzzle


class Day08(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 8, Part {part}")

    def parse_line(self, line):
        patterns, outputs = line.split(" | ")
        return patterns.split(), outputs.split()


class Part1(Day08):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        lines = map(self.parse_line, input)
        outputs = flatten(map(lambda x: x[1], lines))
        simple_digits = filter(lambda pat: len(pat) in (2, 3, 4, 7), outputs)
        count = sum(1 for _ in simple_digits)
        return count


class Part2(Day08):
    def __init__(self, part=2):
        super().__init__(part)

    def solve(self, input):
        lines = list(map(self.parse_line, input))
        patterns = map(lambda x: normalize_patterns(x[0]), lines)
        outputs = map(lambda x: normalize_patterns(x[1]), lines)

        mappings = map(self.fit_code, patterns)

        decoded = map(
            lambda x: (str(self.decode(x[0], o)) for o in x[1]), zip(mappings, outputs)
        )
        str_decoded = map(lambda x: "".join(x), decoded)
        int_decoded = map(int, str_decoded)
        return sum(int_decoded)

    def decode(self, mapping, pattern):
        return DIGIT_PATTERNS.index(self.activations(mapping, pattern))

    def fit_code(self, patterns):
        solutions = list(self.backtrack("", patterns))
        assert len(solutions) == 1
        return solutions[0]

    def backtrack(self, partial_mapping, patterns):
        if self.reject(partial_mapping, patterns):
            return
        if self.accept(partial_mapping, patterns):
            yield partial_mapping
        for s in self.extensions(partial_mapping):
            yield from self.backtrack(s, patterns)

    def reject(self, partial_mapping, patterns):
        if not partial_mapping:
            return False
        # make sure the last added mapping has the right number
        # of activations for this position
        x = partial_mapping[-1]
        n = ACTIVATION_COUNTS[len(partial_mapping) - 1]
        c = sum(x in p for p in patterns)
        return c != n

    def accept(self, mapping, patterns):
        if len(mapping) < 7:
            return False
        for p in patterns:
            if self.activations(mapping, p) not in DIGIT_PATTERNS:
                return False
        return True

    def extensions(self, partial_mapping):
        unmapped = WIRES.difference(partial_mapping)
        for x in unmapped:
            yield partial_mapping + x

    def activations(self, mapping, pattern):
        return "".join("1" if x in pattern else "0" for x in mapping)


WIRES = set("abcdefg")


DIGIT_PATTERNS = [
    "1110111",  # 0
    "0010010",  # 1
    "1011101",  # 2
    "1011011",  # 3
    "0111010",  # 4
    "1101011",  # 5
    "1101111",  # 6
    "1010010",  # 7
    "1111111",  # 8
    "1111011",  # 9
    # counts
    # 8687497
]

ACTIVATION_COUNTS = [8, 6, 8, 7, 4, 9, 7]


def flatten(it):
    for x in it:
        yield from x


def normalize_patterns(seq):
    return ["".join(sorted(x)) for x in seq]


def main():
    Part1().check(EXAMPLE_INPUT, 26)
    Part1().run("inputs/day08.txt")
    Part2().check(EXAMPLE_INPUT, 61229)
    Part2().run("inputs/day08.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

    main()
