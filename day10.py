from more_itertools import peekable
import numpy as np

from puzzle import Puzzle


class Day10(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 10, Part {part}")


class Part1(Day10):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        line_scores = map(score_syntax, input)
        return sum(line_scores)


def score_syntax(line):
    stack = []
    for ch in line:
        if ch in "([{<":
            stack.append(ch)
        if ch in ")]}>":
            top = stack.pop()
            if MATCHING_PAIRS[top] != ch:
                return CHECK_SCORES[ch]
    return 0


class Part2(Day10):
    def __init__(self, part=2):
        super().__init__(part)

    def solve(self, input):
        line_scores = list(map(score_completion, input))
        scores = filter(lambda x: x is not None, line_scores)
        scores = list(scores)
        return np.median(scores).astype('int64')


def score_completion(line):
    stack = []
    for ch in line:
        if ch in "([{<":
            stack.append(ch)
        if ch in ")]}>":
            top = stack.pop()
            if MATCHING_PAIRS[top] != ch:
                return None

    completion_chars = (MATCHING_PAIRS[ch] for ch in stack[::-1])
    points = (COMPLETION_SCORES[ch] for ch in completion_chars)
    total_score = 0
    for p in points:
        total_score *= 5
        total_score += p
    return total_score


MATCHING_PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}


CHECK_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


COMPLETION_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def main():
    Part1().check(EXAMPLE_INPUT, 26397)
    Part1().run("inputs/day10.txt")
    Part2().check(EXAMPLE_INPUT, 288957)
    Part2().run("inputs/day10.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

    main()
