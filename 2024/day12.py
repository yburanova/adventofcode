from copy import deepcopy

filepath = "day12.txt"

def get_file_data():
    return [line.strip() for line in open(filepath)]

def get_letter_map():
    lines = get_file_data()
    letter_map = {}
    for i, line in enumerate(lines):
        for j, sign in enumerate(line):
            letter_map.setdefault(sign, list()).append((i,j))

    return letter_map

def process_position(current_position, all_letter_positions, visited_positions):
    area = 1
    perimeter = 0
    all_letter_positions.remove(current_position)
    visited_positions.append(current_position)

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dx, dy in directions:
        area_delta, perimeter_delta = visit_position(current_position, dx, dy, all_letter_positions, visited_positions)
        area += area_delta
        perimeter += perimeter_delta

    return area, perimeter


def visit_position(current_position, dx, dy, all_letter_positions, visited_positions):
    pos = (current_position[0] + dy, current_position[1] + dx)
    if pos in all_letter_positions: # continue in field
        area, perimeter = process_position(pos, all_letter_positions, visited_positions)
        return area, perimeter
    elif pos in visited_positions: # we were there
        return 0, 0
    else: # border - other type or field border
        return 0, 1


def get_area_and_perimeter(all_letter_positions):
    visited_positions = list()
    area, perimeter = process_position(all_letter_positions[0], all_letter_positions, visited_positions)
    return area, perimeter, all_letter_positions, visited_positions

def get_corners(coordinates):
    all_corners_map = {}
    directions = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for coordinate in coordinates:
        for dx, dy in directions:
            all_corners_map.setdefault((coordinate[0] + dy, coordinate[1] + dx), list()).append(coordinate)

    corner_sum = 0
    for corner, neig_blocks in all_corners_map.items():
        if len(neig_blocks) in {1, 3}:
            corner_sum += 1
        elif len(neig_blocks) == 2:
            block_1, block_2 = neig_blocks
            if block_1[0] != block_2[0] and block_1[1] != block_2[1]:
                corner_sum += 2

    return corner_sum

def solve():
    letter_map = get_letter_map()
    result_part_i = 0
    result_part_ii = 0
    for letter, coordinates in letter_map.items():
        while len(coordinates) != 0:
            area, perimeter, coordinates, visited_positions = get_area_and_perimeter(coordinates)
            result_part_i += area * perimeter

            corners = get_corners(visited_positions)
            result_part_ii += area * corners

    print("Part I", result_part_i)
    print("Part II", result_part_ii)

if __name__ == "__main__":
    solve()