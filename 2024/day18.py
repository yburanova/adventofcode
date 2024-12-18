import numpy as np
from collections import deque

MAX_DEPTH = 1500
filepath ="day18.txt"
field = (71,71)
bytes_felt = 1024
#field = (7,7)
#bytes_felt = 12

def read_file():
    coordinates = [line.strip().split(",") for line in open(filepath)]
    return [(int(c[1]), int(c[0])) for c in coordinates]

def print_canvas(maze, bytes, paths):
    for path in paths:
        print_path(maze, bytes, path)

def print_path(maze, bytes, path):
    canvas = np.full(maze, '.')
    for byte in bytes:
        canvas[byte[0]][byte[1]] = '#'
    for step in path:
        canvas[step[0]][step[1]] = 'X'
    print(canvas)

def is_valid_move(bytes, y, x, visited):
    rows, cols = field
    return 0 <= y < rows and 0 <= x < cols and (y, x) not in bytes and (y, x) not in visited

def walk_maze(maze, falling_bytes):

    start = (0, 0) # initial position
    end = (maze[1] - 1, maze[0] - 1) # end position
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Initialize queue and visited paths
    queue = deque([(start, 0)])
    parent = {start: None}

    while queue:
        current_position, current_depth = queue.popleft()
        x, y = current_position

        # If we've reached the end, save the path
        if current_position == end:
            path = []
            while current_position:
                path.append(current_position)
                current_position = parent[current_position]
            #print("Path found: ", path[::-1])
            #print_path(maze, falling_bytes, current_path)
            return path[::-1]  # Reverse the path

        if current_depth > MAX_DEPTH:
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            next_position = (nx, ny)

            if is_valid_move(falling_bytes, nx, ny, parent):  # Avoid revisiting cells in the current path
                queue.append((next_position, current_depth + 1))
                parent[next_position] = current_position  # Track parent

    return None



def solve_part_i():
    falling_bytes = read_file()[:bytes_felt]
    path = walk_maze(field, falling_bytes)
    print_path(field, falling_bytes, path)
    #scores = list(map(len, paths))
    print("Part I: ", len(path) - 1)

def solve_part_ii():
    falling_bytes = read_file()
    previous_path = None
    for i in range(bytes_felt+1, len(falling_bytes)):

        next_byte = falling_bytes[i - 1]
        if previous_path is not None and next_byte not in previous_path:
            print(f"The same path found byte {i}: {next_byte}")
            continue

        bytes_to_check = falling_bytes[:i]
        path = walk_maze(field, bytes_to_check)
        if path is None:
            print(f"No exit! Stopped by the byte {i}: {next_byte}")
            print(f"Part II: {next_byte[1]},{next_byte[0]}")
            break
        else:
            print(f"Path found byte {i}: {next_byte}, path length: {len(path) - 1}")
            previous_path = path
            #print_path(field, falling_bytes, path)

#solve_part_i()
solve_part_ii()