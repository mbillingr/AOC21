from collections import deque
import heapq

from puzzle import Puzzle


class Day23(Puzzle):
    def __init__(self, input, part):
        super().__init__(f"Day 23, Part {part}")
        self.input = input

    def solve(self, _):
        world = World.parse(self.input)

        all_costs = {world: 0}
        visited = set()

        minimum_cost = float("inf")
        queue = [(0, world)]
        heapq.heapify(queue)
        while queue:
            total_cost, world = heapq.heappop(queue)

            if world in visited:
                continue
            visited.add(world)

            if world.done():
                minimum_cost = min(minimum_cost, total_cost)
                return minimum_cost

            for cost, after_move in world.all_moves():
                nc = total_cost + cost
                if after_move not in all_costs or nc < all_costs[after_move]:
                    all_costs[after_move] = nc
                    heapq.heappush(queue, (nc, after_move))
        return minimum_cost


class Part1(Day23):
    def __init__(self, input, part=1):
        super().__init__(input, part)


class Part2(Day23):
    def __init__(self, input, part=1):
        super().__init__(input, part)


class World:
    def __init__(self, hallway, rooms, room_size):
        self.hallway = hallway
        self.rooms = rooms
        self.room_size = room_size

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return self.hallway == other.hallway and self.rooms == other.rooms

    def __hash__(self):
        return hash(self.hallway) ^ hash(self.rooms)

    @staticmethod
    def parse(input):
        return World(INITIAL_HALLWAY, tuple(input), room_size=len(input[0]))

    def done(self):
        if not all(x == "." for x in self.hallway):
            return False

        for kind, room in zip("ABCD", self.rooms):
            if not all(x == kind for x in room):
                return False

        return True

    def all_moves(self):
        for r, x in enumerate(ROOMS_X):
            yield from self.move_to_hallway(r, x)

        for i, h in enumerate(self.hallway):
            yield from self.move_from_hallway(i)

    def move_to_hallway(self, room, x):
        kind = "ABCD"[room]
        if not self.rooms[room]:
            return
        if all(k == kind for k in self.rooms[room]):
            return

        creature = self.rooms[room][-1]
        rooms = tuple(ro[:-1] if i == room else ro for i, ro in enumerate(self.rooms))

        def to_hallway(rng):
            for p in rng:
                if self.hallway[p] != ".":
                    break
                if p not in ROOMS_X:
                    hallway = self.set_hallway(p, creature)
                    distance = self.distance(p, room)
                    yield distance * MOVE_COSTS[creature], World(
                        hallway, rooms, self.room_size
                    )

        yield from to_hallway(range(x, -1, -1))
        yield from to_hallway(range(x, 11))

    def move_from_hallway(self, p):
        creature = self.hallway[p]
        if creature == ".":
            return

        room = {"A": 0, "B": 1, "C": 2, "D": 3}[creature]
        if any(k != creature for k in self.rooms[room]):
            return

        a = min(p + 1, ROOMS_X[room])
        b = max(p - 1, ROOMS_X[room]) + 1
        if any(k != "." for k in self.hallway[a:b]):
            return

        rooms = tuple(
            ro + (creature,) if i == room else ro for i, ro in enumerate(self.rooms)
        )
        hallway = self.set_hallway(p, ".")
        distance = self.distance(p, room) - 1
        yield distance * MOVE_COSTS[creature], World(hallway, rooms, self.room_size)

    def distance(self, hallway_pos, room_idx):
        return (
            1
            + abs(hallway_pos - ROOMS_X[room_idx])
            + self.room_size
            - len(self.rooms[room_idx])
        )

    def set_hallway(self, p, item):
        return self.hallway[:p] + item + self.hallway[p + 1 :]

    def __str__(self):
        return self.hallway + "\n" + "  | | | |  " + "\n" + str(self.rooms)


MOVE_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOMS_X = (2, 4, 6, 8)
INITIAL_HALLWAY = "..........."


def main():
    Part1(EXAMPLE_INPUT).check("", 12521)
    Part1(ACTUAL_INPUT).run()

    Part2(EXAMPLE_INPUT2).check("", 44169)
    Part2(ACTUAL_INPUT2).run()


if __name__ == "__main__":
    EXAMPLE_INPUT = [("A", "B"), ("D", "C"), ("C", "B"), ("A", "D")]
    ACTUAL_INPUT = [("B", "D"), ("C", "A"), ("B", "C"), ("A", "D")]

    EXAMPLE_INPUT2 = [
        ("A", "D", "D", "B"),
        ("D", "B", "C", "C"),
        ("C", "A", "B", "B"),
        ("A", "C", "A", "D"),
    ]
    ACTUAL_INPUT2 = [
        ("B", "D", "D", "D"),
        ("C", "B", "C", "A"),
        ("B", "A", "B", "C"),
        ("A", "C", "A", "D"),
    ]

    main()
