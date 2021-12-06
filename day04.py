from math import isnan

from puzzle import Puzzle


class Day04(Puzzle):
    def __init__(self, part):
        super().__init__(f"Day 4, Part {part}")

    def load_boards(self, input):
        numbers = list(map(int, next(input).split(',')))
        next(input)  # skip blank line
        boards = []
        current_board = []
        for line in input:
            if not line:
                boards.append(Board(current_board))
                current_board = []
            else:
                current_board.append(list(map(int, line.split())))
        boards.append(Board(current_board))
        return numbers, boards


class Part1(Day04):
    def __init__(self):
        super().__init__(1)

    def solve(self, input):
        numbers, boards = self.load_boards(input)

        for n in numbers:
            for board in boards:
                board.mark(n)
                if board.wins():
                    return board.score(n)


class Part2(Day04):
    def __init__(self):
        super().__init__(2)

    def solve(self, input):
        numbers, boards = self.load_boards(input)

        for n in numbers:
            active_boards = []
            for board in boards:
                board.mark(n)
                if board.wins():
                    if len(boards) == 1:
                        return board.score(n)
                else:
                    active_boards.append(board)
            boards = active_boards


class Board:
    def __init__(self, board):
        self.board = board
        self.marks = [[float('nan') for _ in range(5)] for _ in range(5)]

    def mark(self, n):
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == n:
                    self.marks[i][j] = n

    def wins(self):
        for i in range(5):
            row_sum = sum(self.marks[i])
            if not isnan(row_sum):
                return True
            col_sum = sum(self.marks[j][i] for j in range(5))
            if not isnan(col_sum):
                return True
        return False

    def score(self, n):
        total_unmarked = 0
        for i in range(5):
            for j in range(5):
                if isnan(self.marks[i][j]):
                    total_unmarked += self.board[i][j]
        return total_unmarked * n


def main():
    Part1().check(EXAMPLE_INPUT, 4512)
    Part1().run("inputs/day04.txt")

    Part2().check(EXAMPLE_INPUT, 1924)
    Part2().run("inputs/day04.txt")


if __name__ == '__main__':
    EXAMPLE_INPUT = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

    main()
