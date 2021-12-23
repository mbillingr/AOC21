from dataclasses import dataclass

from puzzle import Puzzle


class Day23(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 23, Part {part}")


class Part1(Day23):
    def __init__(self, part=1):
        super().__init__(part)

    def solve(self, input):
        world = World(input)
        print(world.possible_moves(0))


class World:
    def __init__(self, input):
        self.walls = set()
        self.creatures = []
        for row, line in enumerate(input):
            for col, ch in enumerate(line):
                if ch in "ABCD":
                    self.creatures.append((ch, (row, col)))
                if ch == "#":
                    self.walls.add((row, col))

    def possible_moves(self, creature_idx):
        kind, start_pos = self.creatures[creature_idx]
        started_in_hallway = start_pos == 1

        final_positions = []

        queue = [(0, start_pos)]
        visited = set()
        while queue:
            cost, pos = queue.pop()

            if pos in visited:
                continue

            visited.add(pos)

            if pos in self.walls:
                continue

            if pos != start_pos and self.occupied(pos):
                continue

            if self.may_stop(kind, pos, started_in_hallway):
                final_positions.append((cost, pos))

            for npos in neighbors(pos):
                queue.append((MOVE_COSTS[kind], npos))

        return final_positions

    def occupied(self, pos):
        for kind, p in self.creatures:
            if p == pos:
                return kind
        return None

    def may_stop(self, kind, pos, started_in_hallway):
        if pos[0] == 1:
            if started_in_hallway:
                # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.
                return False

            if pos in DOORWAY:
                # Amphipods will never stop on the space immediately outside any room.
                return False

        elif pos[0] > 1:
            if pos not in TARGETS[kind]:
                # only move into the designated room
                return False

            if pos[0] == 2:
                other = self.occupied((3, pos[1]))
                if not other:
                    # no point in blocking the door... must move to the end of the room
                    return False

                if other != kind:
                    # still occupied by the wrong kind
                    return False

        return True


def neighbors(pos):
    y, x = pos
    yield y, x + 1
    yield y, x - 1
    yield y + 1, x
    yield y - 1, x


MOVE_COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
TARGETS = {'A': ((2, 3), (3, 3)), 'B': ((2, 5), (3, 5)), 'C': ((2, 7), (3, 7)), 'D': ((2, 9), (3, 9))}
DOORWAY = [(1, 3), (1, 5), (1, 6), (1, 7)]


def main():
    Part1().check(EXAMPLE_INPUT, 12521)
    Part1().run(ACTUAL_INPUT)


if __name__ == "__main__":
    EXAMPLE_INPUT = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

    ACTUAL_INPUT = """#############
#...........#
###D#A#C#D###
  #B#C#B#A#
  #########"""

    main()
