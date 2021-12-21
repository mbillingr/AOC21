from dataclasses import dataclass

from puzzle import Puzzle

N_ROLLS_PER_MOVE = 3
TRACK_LENGTH = 10
WINNING_SCORE_PART1 = 1000
WINNING_SCORE_PART2 = 21


class Day21(Puzzle):
    def __init__(self, positions, part):
        super().__init__(f"Day 21, Part {part}")
        self.positions = tuple(positions)


class Part1(Day21):
    def __init__(self, positions, part=1):
        super().__init__(positions, part)
        self.die = DeterministicDie()

    def solve(self, _):
        game = Game(WINNING_SCORE_PART1, self.positions)

        while not game.ends():
            forward = sum(self.die.roll() for _ in range(N_ROLLS_PER_MOVE))
            game = game.move(forward)

        return game.current_score * self.die.last_roll


class Part2(Day21):
    def __init__(self, positions, part=2):
        super().__init__(positions, part)
        self.known_games = {}

        self.roll_combinations = []
        for a in range(1, 4):
            for b in range(1, 4):
                for c in range(1, 4):
                    self.roll_combinations.append(a + b + c)

    def solve(self, _):
        initial_state = Game(WINNING_SCORE_PART2, self.positions)
        wins = self.compute_recursive_wins(initial_state)
        return max(wins)

    def compute_recursive_wins(self, game):
        if game.ends():
            wins = [0, 0]
            wins[game.winning_player] = 1
            return wins

        try:
            return self.known_games[game]
        except KeyError:
            pass

        wins = [0, 0]
        for fw in self.roll_combinations:
            after_move = game.move(fw)
            branch_wins = self.compute_recursive_wins(after_move)
            wins = list_add(wins, branch_wins)

        self.known_games[game] = wins
        return wins


@dataclass(frozen=True)
class Game:
    winning_score: int
    positions: "tuple"
    scores: "tuple" = (0, 0)
    current_player: int = 0

    def ends(self):
        return any(s >= self.winning_score for s in self.scores)

    def move(self, forward):
        pos = self.positions[self.current_player]

        pos += forward
        pos = 1 + (pos - 1) % TRACK_LENGTH

        positions = tuple_set(self.positions, self.current_player, pos)
        scores = tuple_inc(self.scores, self.current_player, pos)
        current_player = 1 - self.current_player

        return Game(self.winning_score, positions, scores, current_player)

    @property
    def current_score(self):
        return self.scores[self.current_player]

    @property
    def winning_player(self):
        return 1 - self.current_player


class DeterministicDie:
    def __init__(self):
        self.last_roll = 0

    def roll(self):
        self.last_roll += 1
        return self.last_roll


def list_add(a, b):
    return [x + y for x, y in zip(a, b)]


def tuple_set(tup, idx, val):
    return tup[:idx] + (val,) + tup[idx+1:]


def tuple_inc(tup, idx, val):
    return tup[:idx] + (tup[idx] + val,) + tup[idx+1:]


def main():
    Part1(EXAMPLE_INPUT).check("", 739785)
    Part1(ACTUAL_INPUT).run()

    Part2(EXAMPLE_INPUT).check("", 444356092776315)
    Part2(ACTUAL_INPUT).run()


if __name__ == "__main__":
    EXAMPLE_INPUT = [4, 8]
    ACTUAL_INPUT = [9, 10]

    main()
