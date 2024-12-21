import numpy as np

filepath = "day21_test.txt"

numeric_keyboard = np.array([['7','8','9'],['4','5','6'],['1','2','3'],['','0','A']])
directional_keyboard = np.array([['','^','A'],['<','v', '>']])

def read_file():
    return [line.strip() for line in open(filepath)]

def is_valid_move(maze, x, y, visited):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != '' and (x, y) not in visited

def walk(maze, x, y, end, path, visited, paths):

    if (x, y) == end:
        paths.append(path[:])  # Add a copy of the current path
        return

    visited.add((x, y))

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy  # next position
        if is_valid_move(maze, nx, ny, visited):
            path.append((nx, ny))
            walk(maze, nx, ny, end, path, visited, paths)
            path.pop()  # Backtrack to explore other paths

    # Unmark this cell (backtrack)
    visited.remove((x, y))

def find_paths(keyboard, from_code, to_code):
    start = tuple(np.argwhere(keyboard == from_code)[0])
    end = tuple(np.argwhere(keyboard == to_code)[0])
    paths = []
    visited = set()

    walk(keyboard, start[0], start[1], end, [start], visited, paths)
    shortest_paths = [path for path in paths if len(path) == len(min(paths, key=len))]
    return shortest_paths

def turn_sequences_to_signs(sequences):
    # Initialize an empty list to store commands
    sign_sequences = []

    # Loop through consecutive pairs of points
    for points in sequences:
        commands = []
        for i in range(1, len(points)):
            if points[i] == 'A':
                commands.append('A')
                i += 2
                continue
            elif points[i] != 'A' and points[i-1] != 'A':
                (y1, x1) = points[i - 1]
                (y2, x2) = points[i]

                # Determine the movement direction
                if x2 > x1:
                    commands.append(">")
                elif x2 < x1:
                    commands.append("<")
                elif y2 > y1:
                    commands.append("v")
                elif y2 < y1:
                    commands.append("^")

        sign_sequences.append(commands)

    return sign_sequences

def get_sequences(code, keyboard):
    print("Code", code)
    start_position = 'A'
    sequences = []

    for i in range(len(code)):
        paths = find_paths(keyboard, start_position, code[i])
        if len(sequences) == 0:
            for path in paths:
                sequences.append(path)
        else:
            new_sequences = []
            for sequence in sequences:
                for path in paths:
                    new_sequences.append(sequence + path)
            sequences = new_sequences
        start_position = code[i]
        for sequence in sequences:
            sequence.append('A')

    sequences = turn_sequences_to_signs(sequences)
    for sequence in sequences:
        print(sequence)
    return sequences


def get_shortest_sequence(code):
    sequences = get_sequences(code, keyboard=numeric_keyboard)
    sequences_complete = []

    for i in range(2):
        sequences_1 = []
        for sequence in sequences:
            sequences_2 = get_sequences(sequence, keyboard=directional_keyboard)
            sequences_1.extend(sequences_2)
        shortest_sequences = [path for path in sequences_1 if len(path) == len(min(sequences_1, key=len))]
        #sequences_complete.extend(shortest_sequences)
        sequences = shortest_sequences

    print(sequences_complete[0])

    return ''


def solve_part_i():
    codes = read_file()
    for code in codes:
        sequence = get_shortest_sequence(code)
        print(sequence)

solve_part_i()