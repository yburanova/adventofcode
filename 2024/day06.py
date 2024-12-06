from copy import deepcopy
import stopit
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

filepath = "day06.txt"
directions = ['up', 'right', 'down', 'left']

class Guard:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Guard at: {self.x}:{self.y}"

def load_board(filepath):
    with open(filepath) as file:
        return np.array([list(line.strip()) for line in file])

def get_guard_position(board):
    guard_position = np.where(board == '^')
    return Guard(guard_position[1][0], guard_position[0][0])

def move_guard(board, guard, direction):
    direction_map = {
        'up': (-1, 0, '^'),
        'right': (0, 1, '>'),
        'down': (1, 0, 'v'),
        'left': (0, -1, '<')
    }

    dy, dx, symbol = direction_map[direction]

    while True:
        new_y = guard.y + dy
        new_x = guard.x + dx

        if (not (0 <= new_y < len(board) and 0 <= new_x < len(board[0]))
                or board[new_y][new_x] == '#'):
            break

        # Update board and guard position
        board[guard.y][guard.x] = 'X'
        guard.y, guard.x = new_y, new_x
        board[guard.y][guard.x] = symbol

    # Determine exit condition
    if not (0 <= new_y < len(board)) or not (0 <= new_x < len(board[0])):
        return '!'
    if board[new_y][new_x] == '#':
        return '#'

@stopit.threading_timeoutable()
def run_a_loop(original_board, guard):
    board = deepcopy(original_board)
    while True:
        for direction in directions:
            return_code = move_guard(board, guard, direction)
            if return_code == '!':
                board[guard.y][guard.x] = 'X'
                result = (board == 'X').sum()
                print(result)
                return board

def process_block_position(position, board, guard):
    y, x = position
    new_board = deepcopy(board)
    new_board[y][x] = '#'
    result = run_a_loop(timeout=1, original_board=new_board, guard=get_guard_position(board))
    if result is None:
        print((y, x), "is a possible loop")
        return (y, x)
    return None


def solve_part_I():
    board = load_board(filepath)
    guard = get_guard_position(board)
    run_a_loop(board, guard)


def solve_part_II():
    board = load_board(filepath)
    guard = get_guard_position(board)

    result_board = run_a_loop(board, guard)

    possible_block_positions = list(zip(*np.where(result_board == 'X')))
    loops = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_block_position, pos, board, guard) for pos in possible_block_positions]
        for future in as_completed(futures):
            result = future.result()
            if result:
                loops.append(result)


    print(len(loops))

#solve_part_I()
solve_part_II()
