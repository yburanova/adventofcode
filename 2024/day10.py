from copy import deepcopy

import numpy as np

filepath = "day10.txt"


def get_trailhead_score(trailhead, field):
    found_peaks = set()
    walk(trailhead, field, found_peaks)
    print(found_peaks)
    return len(found_peaks)


def walk(current_position, field, found_peaks):

    # print("Current value: ", current_value)
    # print("Current position: ", current_position)
    y = current_position[0]
    x = current_position[1]

    if field[y, x] == 9:
        print("Peak reached: ", current_position)
        found_peaks.add((y, x))
        return

    if y < len(field) - 1:
        dy = 1
        dx = 0
        get_value(field, x, y, dx, dy, found_peaks)

    if x < len(field[0]) - 1:
        dy = 0
        dx = 1
        get_value(field, x, y, dx, dy, found_peaks)

    if y > 0:
        dy = -1
        dx = 0
        get_value(field, x, y, dx, dy, found_peaks)

    if x > 0:
        dy = 0
        dx = -1
        get_value(field, x, y, dx, dy, found_peaks)

    return


def get_value(field, x, y, dx, dy, found_peaks):
    value_neighbor = field[y + dy][x + dx]
    if value_neighbor == field[y, x] + 1:
        walk([y + dy, x + dx], field, found_peaks)


def solve_part_I():
    field = get_field()
    trailheads = np.argwhere(field == 0)
    score = 0
    for trailhead in trailheads:
        score += get_trailhead_score(trailhead, field)

    print(score)
    return score


def get_field():
    field = []
    with open(filepath) as file:
        for line in file.readlines():
            field.append(list(line.strip()))
    field = np.array(field).astype(int)
    print(field)
    return field


solve_part_I()