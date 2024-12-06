import numpy as np

filepath = "day06.txt"

class Guard:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Guard at: {self.x}:{self.y}"

def go_up(board, guard):

    while True:
        if (guard.y == 0) or (board[guard.y - 1][guard.x] == '#'):
            break
        board[guard.y][guard.x] = 'X'
        guard.y = guard.y - 1
        board[guard.y][guard.x] = '^'

    print(board)

    if guard.y == 0:
        return '!'

    if board[guard.y - 1][guard.x] == '#':
        return "#"


def go_right(board, guard):

    while True:
        if (guard.x == len(board[0]) - 1) or (board[guard.y][guard.x + 1] == '#'):
            break
        board[guard.y][guard.x] = 'X'
        guard.x = guard.x + 1
        board[guard.y][guard.x] = '>'

    print(board)

    if guard.x == len(board[0]) - 1:
        return '!'

    if board[guard.y][guard.x + 1] == '#':
        return "#"


def go_down(board, guard):

    while True:
        if (guard.y == len(board) - 1) or (board[guard.y + 1][guard.x] == '#'):
            break
        board[guard.y][guard.x] = 'X'
        guard.y = guard.y + 1
        board[guard.y][guard.x] = 'v'

    print(board)

    if guard.y == len(board) - 1:
        return '!'

    if board[guard.y + 1][guard.x] == '#':
        return "#"


def go_left(board, guard):

    while True:
        if (guard.x == 0) or (board[guard.y][guard.x - 1] == '#'):
            break
        board[guard.y][guard.x] = 'X'
        guard.x = guard.x - 1
        board[guard.y][guard.x] = '<'

    print(board)

    if guard.x == 0:
        return '!'

    if board[guard.y][guard.x - 1] == '#':
        return "#"



def solve_part_I():
    with open(filepath) as file:
        board = np.array([list(line.strip()) for line in file])

        print(board)
        guard_position = np.where(board == '^')
        print(guard_position)
        guard = Guard(guard_position[1][0], guard_position[0][0])
        print("start!")

        while True:
            return_code = go_up(board, guard)
            if return_code == '!':
                break

            return_code = go_right(board, guard)
            if return_code == '!':
                break

            return_code = go_down(board, guard)
            if return_code == '!':
                break

            return_code = go_left(board, guard)
            if return_code == '!':
                break

        result = (board == 'X').sum() + 1
        print(result)

solve_part_I()