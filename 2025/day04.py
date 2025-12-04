import numpy as np

filepath = "day04.txt"


def read_file():
    return [line.strip() for line in open(filepath)]

def get_rolls(lines):
    rolls_of_paper = []
    row = 0
    for line in lines:
        tokens = list(line)
        for column in range(len(tokens)):
            if tokens[column] == '@':
                rolls_of_paper.append((row, column))
        row += 1

    return rolls_of_paper

def is_accessed(roll, all_rolls):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    adjacent_rolls_count = 0
    for direction in directions:
        possible_direction = tuple(x + y for x, y in zip(roll, direction))
        if possible_direction in all_rolls:
            adjacent_rolls_count += 1
            if adjacent_rolls_count > 3:
                return False

    return True


def solve_part_I():
    lines = read_file()
    rolls_of_paper = get_rolls(lines)
    print(rolls_of_paper)

    accessible_rolls = 0
    for roll in rolls_of_paper:
        if is_accessed(roll, rolls_of_paper):
            accessible_rolls += 1

    return accessible_rolls


# result_1 = solve_part_I()
# print(result_1)


def get_accessible_rolls(rolls_of_paper):
    accessible_rolls = []
    for roll in rolls_of_paper:
        if is_accessed(roll, rolls_of_paper):
            accessible_rolls.append(roll)
    print(f"Totally accessible rolls: {len(accessible_rolls)}")
    return accessible_rolls


def solve_part_II():
    lines = read_file()
    rolls_of_paper = get_rolls(lines)
    print(rolls_of_paper)

    accessible_rolls = rolls_of_paper
    sum_accessed_rolls = 0
    while len(accessible_rolls) > 0:
        accessible_rolls = get_accessible_rolls(rolls_of_paper)
        sum_accessed_rolls += len(accessible_rolls)
        rolls_of_paper = list(set(rolls_of_paper) - set(accessible_rolls))
    print(f"Totally removed: {sum_accessed_rolls}")

    return sum_accessed_rolls


result_2 = solve_part_II()
print(result_2)
