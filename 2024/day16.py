import numpy as np
import sys, resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

filepath = "day16.txt"
max_path = sys.maxsize

def read_maze():
    maze = [list(line.strip()) for line in open(filepath)]
    return maze

def print_canvas(maze, paths):
    canvas = np.array(maze)
    print(canvas)

    for path in paths:
        print_path(maze, path)

def print_path(maze, path):
    canvas = np.array(maze)
    print(path)
    for step in path:
        canvas[step[0]][step[1]] = 'X'
    print(canvas)


def is_valid_move(maze, x, y, visited):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != '#' and (x, y) not in visited

def walk(maze, x, y, end, path, visited, paths):
    global max_path
    if max_path != sys.maxsize: # some path was already found
        path_len = evaluate_path(path)
        if path_len > max_path:
            print("too much")
            return

    if (x, y) == end:
        paths.append(path[:])  # Add a copy of the current path
        #print("Path found: ", path)
        path_len = evaluate_path(path)
        if path_len < max_path:
            max_path = path_len
            print("Path found, length: ", max_path)
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

def walk_maze(maze):
    paths = []
    start = (len(maze) - 2, 1) # initial position
    end = (1, len(maze[0]) - 2) # end position
    visited = set()

    walk(maze, start[0], start[1], end, [start], visited, paths)
    return paths

def evaluate_path(path):
    direction_map = {
        'r': {'next': (0, 1),
              'turns': {'d': (1, 0),
                        'u': (-1, 0)}},
        'l': {'next': (0, -1),
              'turns': {'d': (1, 0),
                        'u': (-1, 0)}},
        'u': {'next': (-1, 0),
              'turns': {'r': (0, 1),
                        'l': (0, -1)}},
        'd': {'next': (1, 0),
              'turns': {'r': (0, 1),
                        'l': (0, -1)}}
    }

    score = 0
    last = path[0]
    current_direction = 'r'
    for step in path:
        if step == path[0]:
            continue

        dx, dy = step[0] - last[0], step[1] - last[1]

        # Check if moving in the current direction
        expected_dx, expected_dy = direction_map[current_direction]['next']
        if (dx, dy) == (expected_dx, expected_dy):
            score += 1
        else:
            # Check if it's a valid turn
            for new_direction, (turn_dx, turn_dy) in direction_map[current_direction]['turns'].items():
                if (dx, dy) == (turn_dx, turn_dy):
                    current_direction = new_direction
                    score += 1001
                    break

        # Update the last position
        last = step

    return score

def evaluate_paths(maze, paths, start):
    scores = []
    for path in paths:
        score = evaluate_path(path)
        scores.append(score)

    print(scores)
    return scores


def solve_part_i():
    maze = read_maze()
    paths = walk_maze(maze)
    #print_canvas(maze, paths)
    scores = evaluate_paths(maze, paths, start = (len(maze) - 2, 1))
    print("Part I: ", min(scores))


solve_part_i()
