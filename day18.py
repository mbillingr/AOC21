import json
from puzzle import Puzzle


class Day18(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 18, Part {part}")


class Part1(Day18):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        numbers = [parse_pair(line) for line in input]
        total = numbers[0]
        for n in numbers[1:]:
            total = add_pairs(total, n)
            total = reduce_pair(total)
        return magnitude(total)


class Part2(Day18):
    def __init__(self, part=2):
        super().__init__(part)

    def solve(self, input):
        numbers = [parse_pair(line) for line in input]
        max_mag = 0
        for a in numbers:
            for b in numbers:
                c = add_pairs(a, b)
                d = reduce_pair(c)
                m = magnitude(d)
                if m > max_mag:
                    max_mag = m
        return max_mag


def parse_pair(line: str):
    s = json.loads(line)
    return s


def magnitude(number):
    match number:
        case int(): return number
        case [l, r]: return 3*magnitude(l) + 2*magnitude(r)


def recsum(number):
    match number:
        case int(): return number
        case [l, r]: return recsum(l) + recsum(r)


def add_pairs(a, b):
    if a == 0: return b
    if b == 0: return a
    return [a, b]


def reduce_pair(number):
    number = number
    while True:
        n = explode_left(number)
        if n is not number:
            number = n
            continue

        n = split_left(number)
        if n is not number:
            number = n
            continue

        return number


def split_left(number):
    match number:
        case int(x) if x >= 10:
            l = x // 2
            r = x - l
            return [l, r]
        case int(): return number
        case [l, r]:
            l1 = split_left(l)
            if l1 is not l:
                return [l1, r]

            r1 = split_left(r)
            if r1 is not r:
                return [l, r1]

            return number


def explode_left(pair):
    cmd, out = explode_left_aux(pair)
    return out


def explode_left_aux(pair, nesting_level=0):
    match pair:
        case int(): return (), pair

        case [[a, b], r] if nesting_level == 3:
            assert isinstance(a, int) and isinstance(b, int)
            r = add_left(b, r)
            return ('propagate-left', a), [0, r]

        case [l, [a, b]] if nesting_level == 3:
            assert isinstance(a, int) and isinstance(b, int)
            l = add_right(a, l)
            return ('propagate-right', b), [l, 0]

        case [l, r]:
            cmd, l1 = explode_left_aux(l, nesting_level+1)
            if l1 is not l:
                match cmd:
                    case ('propagate-right', x): return (), [l1, add_left(x, r)]
                    case _: return cmd, [l1, r]

            cmd, r1 = explode_left_aux(r, nesting_level+1)
            if r1 is not r:
                match cmd:
                    case ('propagate-left', x): return (), [add_right(x, l), r1]
                    case _: return cmd, [l, r1]

            return (), pair


def add_left(x, pair):
    match pair:
        case int(y): return x + y
        case [l, r]: return [add_left(x, l), r]


def add_right(x, pair):
    match pair:
        case int(y): return x + y
        case [l, r]: return [l, add_right(x, r)]


def main():
    assert explode_left([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
    assert explode_left([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
    assert explode_left([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
    assert explode_left([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    assert explode_left([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

    Part1().check(EXAMPLE_INPUT, 4140)
    Part1().run("inputs/day18.txt")

    Part2().check(EXAMPLE_INPUT, 3993)
    Part2().run("inputs/day18.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

    main()
