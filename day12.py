from collections import Counter

from puzzle import Puzzle


class Day12(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 12, Part {part}")

    def load_edges(self, input):
        node_pairs = map(lambda line: line.split("-"), input)
        edges = {}
        for a, b in node_pairs:
            edges.setdefault(a, []).append(b)
            edges.setdefault(b, []).append(a)
        return edges


class Part1(Day12):
    def __init__(self, part=1):
        super().__init__(part)
        self.total_paths = 0

    def solve(self, input):
        self.edges = self.load_edges(input)
        self.find_all_paths("start")
        return self.total_paths

    def find_all_paths(self, node, path=[]):
        if node == "end":
            self.total_paths += 1
            return
        path = path + [node]
        if not self.is_valid_path(path):
            return
        for neighbor in self.edges[node]:
            self.find_all_paths(neighbor, path)

    def is_valid_path(self, path):
        node = path[-1]
        return not (node.islower() and node in path[:-1])


class Part2(Part1):
    def __init__(self, part=2):
        super().__init__(part)

    def is_valid_path(self, path):
        if len(path) < 2:
            return True
        if path[-1] == "start":
            return False
        cave_counts = Counter(filter(str.islower, path))
        cc = Counter(cave_counts.values())
        if len(cc) < 2:
            return True
        return cc[2] == 1


def main():
    Part1().check(EXAMPLE1, 10)
    Part1().check(EXAMPLE2, 19)
    Part1().check(EXAMPLE3, 226)
    Part1().run("inputs/day12.txt")
    Part2().check(EXAMPLE1, 36)
    Part2().check(EXAMPLE2, 103)
    Part2().check(EXAMPLE3, 3509)
    Part2().run("inputs/day12.txt")


if __name__ == "__main__":
    EXAMPLE1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    EXAMPLE2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
    EXAMPLE3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

    main()
