import numpy as np

filepath = "day10.txt"

def get_field():
    field = []
    with open(filepath) as file:
        for line in file.readlines():
            field.append(list(line.strip()))
    field = np.array(field).astype(int)
    return field

def get_trailhead_score(trailhead, field):
    found_peaks = list()
    walk(trailhead, field, found_peaks)
    return len(set(found_peaks)), len(found_peaks)


def walk(current_position, field, found_peaks):

    y, x = current_position

    if field[y, x] == 9:
        found_peaks.append((y, x))
        return

    for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # Down, Right, Up, Left
        new_y, new_x = y + dy, x + dx
        if 0 <= new_y < len(field) and 0 <= new_x < len(field[0]):  # Check boundaries
            if field[new_y][new_x] == field[y, x] + 1:
                walk((new_y, new_x), field, found_peaks)


def solve_both_parts():
    field = get_field()
    trailheads = [
        (y, x)
        for y, row in enumerate(field)
        for x, value in enumerate(row)
        if value == 0
    ]

    score_i, score_ii = 0, 0
    for trailhead in trailheads:
        scores = get_trailhead_score(trailhead, field)
        score_i += scores[0]
        score_ii += scores[1]

    print("Part I: ", score_i)
    print("Part II: ", score_ii)


solve_both_parts()