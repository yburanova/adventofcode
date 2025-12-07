import math
from collections import defaultdict

from numpy._core.strings import isdigit

filepath = "day07.txt"


def read_file():
    source = ()
    splitters = []
    all_lines = [line.strip() for line in open(filepath)]
    for i, line in enumerate(all_lines):
        for j, sign in enumerate(line):
            if sign == 'S':
                source = (j, i)
            if sign == '^':
                splitters.append((j, i))

    return source, set(splitters), len(all_lines)


def beam_step(prev_beams, splitters):
    next_beam_positions = set()
    split_count = 0
    for beam in prev_beams:
        next_pos = (beam[0], beam[1] + 1)
        if next_pos in splitters:
            split_count += 1
            next_left = (next_pos[0] - 1, next_pos[1])
            next_right = (next_pos[0] + 1, next_pos[1])
            if next_left not in splitters:
                next_beam_positions.add(next_left)
            if next_right not in splitters:
                next_beam_positions.add(next_right)
        else:
            next_beam_positions.add(next_pos)

    return next_beam_positions, split_count


def solve_part_I():
    source, splitters, board_len = read_file()
    print(source)
    print(splitters)
    print(board_len)

    prev_beam = [source]
    total_split = 0
    for i in range(board_len):
        print(f"Previously created beams {prev_beam}")
        prev_beam, split_count = beam_step(prev_beam, splitters)
        total_split += split_count

    return total_split


# result_1 = solve_part_I()
# print(result_1)

def beam_step_part_II(prev_beams, splitters):
    next_beam_positions = defaultdict(int)
    path_count = 0

    for (x, y), count in prev_beams.items():
        ny = y + 1
        next_pos = (x, ny)

        if next_pos in splitters:
            path_count += count

            left = (x - 1, ny)
            right = (x + 1, ny)
            if left not in splitters:
                next_beam_positions[left] += count
            if right not in splitters:
                next_beam_positions[right] += count
        else:
            next_beam_positions[next_pos] += count

    print(f"Previously created beams: {prev_beams}")
    print(f"Newly created beams: {next_beam_positions}")
    print(f"Added paths: {path_count}")
    return dict(next_beam_positions), path_count

def solve_part_II():
    source, splitters, board_len = read_file()
    print(source)
    print(splitters)
    print(board_len)

    prev_beam = {source: 1}
    total_paths = 1
    for _ in range(board_len):
        prev_beam, path_count = beam_step_part_II(prev_beam, splitters)
        total_paths += path_count
        print(f"Total paths: {total_paths}")

    return total_paths


result_2 = solve_part_II()
print(result_2)
