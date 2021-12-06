
from puzzle import Puzzle


class Part1(Puzzle):
    def __init__(self):
        super().__init__("Day 3, Part 1")

    def solve(self, input):
        numbers = list(input)

        most_commons = []
        for i in range(0, 99):
            try:
                most_commons.append(most_common_bit(x[i] for x in numbers))
            except IndexError:
                break

        gamma_rate = int(''.join(most_commons), 2)
        epsilon_rate = int(''.join(map(strinv, most_commons)), 2)
        return gamma_rate * epsilon_rate


class Part2(Puzzle):
    def __init__(self):
        super().__init__("Day 3, Part 2")

    def solve(self, input):
        numbers = list(input)
        oxy = self.compute(numbers, self.oxy_criterion)
        co2 = self.compute(numbers, self.co2_criterion)
        return oxy * co2

    def oxy_criterion(self, bits):
        return most_common_bit(bits)

    def co2_criterion(self, bits):
        return strinv(most_common_bit(bits))

    def compute(self, numbers, compute_criterion):
        current_bit = 0
        while len(numbers) > 1:
            keep_bit = compute_criterion(x[current_bit] for x in numbers)
            numbers = list(filter(lambda x: x[current_bit] == keep_bit, numbers))
            current_bit += 1
        return int(numbers[0], 2)


def most_common_bit(bits):
    one_count = 0
    zero_count = 0
    for x in bits:
        if x == '1':
            one_count += 1
        else:
            zero_count += 1
    return '1' if one_count >= zero_count else '0'


def strinv(bit):
    match bit:
        case '1': return '0'
        case '0': return '1'
        case _: raise ValueError(f"invalid bit: {bit}")


def main():
    Part1().check(EXAMPLE_INPUT, 198)
    Part1().run("inputs/day03.txt", wrong=(130,))

    Part2().check(EXAMPLE_INPUT, 230)
    Part2().run("inputs/day03.txt", wrong=())


if __name__ == '__main__':
    EXAMPLE_INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

    main()
