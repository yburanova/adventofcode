import numpy as np
from collections import deque

filepath = "day20.txt"


def read_file():
    return [list(line.strip()) for line in open(filepath)]

def find_start_end(field):
    start = None
    end = None
    for i, line in enumerate(field):
        for j, sign in enumerate(line):
            if field[i][j] == 'S':
                start = i, j
            elif field[i][j] == 'E':
                end = i, j
        if start is not None and end is not None:
            return start, end

def print_canvas(maze, paths):
    for path in paths:
        print_path(maze, path)

def print_path(maze, path):
    canvas = np.array(maze)
    for step in path:
        canvas[step[0]][step[1]] = 'X'
    print(canvas)

def is_valid_move(maze, y, x, visited):
    rows, cols = len(maze), len(maze[0])
    return 0 <= y < rows and 0 <= x < cols and maze[y][x] != '#' and (y, x) not in visited

def walk_maze(maze, start, end):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    queue = deque([start])
    parent = {start: None}

    while queue:
        current_position = queue.popleft()
        x, y = current_position
        #print(current_position)

        if current_position == end:  # If we've reached the end, save the path
            path = []
            while current_position:
                path.append(current_position)
                current_position = parent[current_position]
            # print_path(maze, path[::-1])
            return path[::-1]  # Reverse the path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            next_position = (nx, ny)

            if is_valid_move(maze, nx, ny, parent):
                queue.append(next_position)
                parent[next_position] = current_position

    return None


def get_cheats(path):
    cheats = {}
    # print("complete path", path)
    for i in range(len(path)):
        current_position = path[i]
        rest_path = path[i + 1:]
        # print("Current Position", current_position)
        # print("Rest path:", rest_path)

        y, x = current_position
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dy, dx in directions:
            wy, wx = y + dy, x + dx  # possible wall
            ny, nx = y + 2 * dy, x + 2 * dx

            if (ny, nx) in rest_path and (wy, wx) not in rest_path:
                # print("Cheat found", (ny, nx))
                index_to_jump_to = path.index((ny, nx))
                saved_steps = index_to_jump_to - i - 2
                #print("Saved steps", saved_steps)
                cheats[saved_steps] = cheats.setdefault(saved_steps, 0) + 1

    return cheats


def solve_part_i():
    maze = read_file()
    start, end = find_start_end(maze)
    path = walk_maze(maze, start, end)
    print_path(maze, path)
    print("Path: ", len(path) - 1)

    cheats = get_cheats(path)
    print(cheats)

    counter = sum([counter for steps_saved, counter in cheats.items() if steps_saved >= 100])
    print("Part I: ", counter)


# def solve_part_ii():
#     falling_bytes = read_file()
#     previous_path = None
#     for i in range(bytes_felt+1, len(falling_bytes)):
#
#         next_byte = falling_bytes[i - 1]
#         if previous_path is not None and next_byte not in previous_path:
#             print(f"The same path found byte {i}: {next_byte}")
#             continue
#
#         bytes_to_check = falling_bytes[:i]
#         path = walk_maze(field, bytes_to_check)
#         if path is None:
#             print(f"No exit! Stopped by the byte {i}: {next_byte}")
#             print(f"Part II: {next_byte[1]},{next_byte[0]}")
#             break
#         else:
#             print(f"Path found byte {i}: {next_byte}, path length: {len(path) - 1}")
#             previous_path = path

solve_part_i()
# solve_part_ii()
