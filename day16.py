from operator import mul
from functools import reduce
from puzzle import Puzzle


class Day16(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 16, Part {part}")


class Part1(Day16):
    def __init__(self, part=1):
        super().__init__(part)
        self.total_flashes = 0

    def solve(self, input):
        reader = BITSParser(next(input))
        expr = reader.parse_packet()
        return self.sum_versions(expr)

    def sum_versions(self, expr):
        match expr:
            case (('lit', v), _): return v
            case ((_, v), *args): return v + sum(map(self.sum_versions, args))


class Part2(Day16):
    def __init__(self, part=1):
        super().__init__(part)
        self.total_flashes = 0

    def solve(self, input):
        reader = BITSParser(next(input))
        expr = reader.parse_packet()
        return evaluate(expr)


def evaluate(expr):
    match expr:
        case (('lit', _), x): return x
        case (('+', _), *args): return sum(map(evaluate, args))
        case (('*', _), *args): return prod(map(evaluate, args))
        case (('min', _), *args): return min(map(evaluate, args))
        case (('max', _), *args): return max(map(evaluate, args))
        case (('<', _), a, b): return evaluate(a) < evaluate(b)
        case (('>', _), a, b): return evaluate(a) > evaluate(b)
        case (('=', _), a, b): return evaluate(a) == evaluate(b)
        case _: raise SyntaxError(f"unknown expression: {expr}")


def prod(args):
    return reduce(mul, args)


class BITSParser:
    """Parse BITS code into S-expressions.

    S-expressions are tuples of the form ((operator, version), *args).
    """
    def __init__(self, input):
        if isinstance(input, str):
            self.bit_reader = BitReader(input)
        else:
            raise NotImplementedError()

        self.type_id_parsers = {
            4: self.parse_literal,
            0: lambda: self.parse_operator("+"),
            1: lambda: self.parse_operator("*"),
            2: lambda: self.parse_operator("min"),
            3: lambda: self.parse_operator("max"),
            5: lambda: self.parse_operator(">"),
            6: lambda: self.parse_operator("<"),
            7: lambda: self.parse_operator("="),
        }

    def parse_packet(self):
        version = self.bit_reader.read_int(3)
        type_id = self.bit_reader.read_int(3)
        payload = self.parse_payload(type_id)

        operator = payload[0]
        args = payload[1:]

        return ((operator, version),) + args

    def parse_payload(self, type_id):
        try:
            return self.type_id_parsers[type_id]()
        except KeyError:
            pass
        return self.parse_operator(type_id)

    def parse_literal(self):
        number = 0
        continued = True
        while continued:
            continued = self.bit_reader.read_bool()
            half_byte = self.bit_reader.read_int(4)
            number = (number << 4) + half_byte
        return 'lit', number

    def parse_operator(self, op):
        length_type_id = self.bit_reader.read_bool()
        if length_type_id:
            n_sub_packets = self.bit_reader.read_int(11)
            return (op,) + self.parse_n_packets(n_sub_packets)
        else:
            n_bits_total_sub_packets = self.bit_reader.read_int(15)
            return (op,) + self.parse_packets_by_bits(n_bits_total_sub_packets)

    def parse_n_packets(self, n):
        return tuple(self.parse_packet() for _ in range(n))

    def parse_packets_by_bits(self, total_size):
        limit = self.bit_reader.bits_remaining - total_size
        packets = []
        while self.bit_reader.bits_remaining > limit:
            packets.append(self.parse_packet())
        return tuple(packets)


class BitReader:
    def __init__(self, hexstring):
        self.bits = self.hexstring_to_bitstring(hexstring)

    @property
    def bits_remaining(self):
        return len(self.bits)

    def hexstring_to_bitstring(self, hexstring):
        bitlist = []
        for ch in hexstring:
            decimal = int(ch, 16)
            binary = format(decimal, "04b")
            bitlist.append(binary)
        return ''.join(bitlist)

    def read_int(self, n_bits):
        return int(self.read_bitstring(n_bits), 2)

    def read_bool(self):
        return self.read_bitstring(1) == '1'

    def read_bitstring(self, n_bits):
        s = self.bits[:n_bits]
        self.bits = self.bits[n_bits:]
        return s


def main():
    Part1().check("8A004A801A8002F478", 16)
    Part1().check("620080001611562C8802118E34", 12)
    Part1().check("C0015000016115A2E0802F182340", 23)
    Part1().check("A0016C880162017C3686B18A3D4780", 31)
    Part1().run("inputs/day16.txt")

    Part2().check("C200B40A82", 3)
    Part2().check("04005AC33890", 54)
    Part2().check("880086C3E88112", 7)
    Part2().check("CE00C43D881120", 9)
    Part2().check("D8005AC2A8F0", 1)
    Part2().check("F600BC2D8F", 0)
    Part2().check("9C005AC2F8F0", 0)
    Part2().check("9C0141080250320F1802104A08", 1)
    Part2().run("inputs/day16.txt")


if __name__ == "__main__":
    EXAMPLE_INPUT = """8A004A801A8002F478"""

    main()
