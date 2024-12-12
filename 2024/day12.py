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

    # print("Processing positions: ", current_position)
    # print("The same letter at: ", all_letter_positions)
    # print("I saw positions: ", visited_positions)

    area_r, perimeter_r = visit_position(current_position, 1, 0, all_letter_positions, visited_positions)
    area_d, perimeter_d = visit_position(current_position, 0, 1, all_letter_positions, visited_positions)
    area_l, perimeter_l = visit_position(current_position, -1, 0, all_letter_positions, visited_positions)
    area_u, perimeter_u = visit_position(current_position, 0, -1, all_letter_positions, visited_positions)

    area += area_r
    area += area_u
    area += area_l
    area += area_d

    perimeter += perimeter_r
    perimeter += perimeter_u
    perimeter += perimeter_l
    perimeter += perimeter_d

    return area, perimeter


def visit_position(current_position, dx, dy, all_letter_positions, visited_positions):
    pos = (current_position[0] + dy, current_position[1] + dx)
    if pos in all_letter_positions: # continue in field
        area, perimeter = process_position(pos, all_letter_positions, visited_positions)
        return area, perimeter
    elif pos not in visited_positions: # border - other type or field border
        return 0, 1
    else: # we were there
        return 0, 0


def get_area_and_perimeter(all_letter_positions):
    new_positions = deepcopy(all_letter_positions)

    area, perimeter = process_position(new_positions[0], new_positions, list())
    # print("Area: ", area)
    # print("Perimeter: ", perimeter)

    return area, perimeter, new_positions



def solve_part_i():
    letter_map = get_letter_map()
    print(letter_map)
    result = 0
    for letter, coordinates in letter_map.items():
        while len(coordinates) != 0:
            area, perimeter, coordinates = get_area_and_perimeter(coordinates)
            result += area * perimeter

    print(result)

solve_part_i()