from curses.ascii import isdigit

import numpy as np

filepath = "day05.txt"


def read_file():
    ranges = []
    ingredients = []
    with open(filepath) as file:
        for line in file.readlines():
            line = line.strip()
            if '-' in line:
                ranges.append(line.split("-"))
            elif len(line) == 0:
                continue
            else:
                ingredients.append(int(line))

    ranges = [(int(r[0]), int(r[1])) for r in ranges]
    return ranges, ingredients

def join_ranges(ranges):
    # sort by start
    ranges = sorted(ranges, key=lambda r: r[0])
    merged = [ranges[0]]

    for current in ranges[1:]:
        last_start, last_end = merged[-1]
        cur_start, cur_end = current

        if cur_start <= last_end:  # overlap or touching
            merged[-1] = (last_start, max(last_end, cur_end))
        else:
            merged.append(current)

    return merged


def remove_fresh_ingredients(id_range, ingredients_under_questions):
    print(f"ID range for fresh ingredients: {id_range}", end='; ')
    start, end = id_range

    ingredients_under_questions = [
        x for x in ingredients_under_questions
        if not (start <= x <= end)
    ]

    print(f"Still questionable ingredients: {ingredients_under_questions}")
    return ingredients_under_questions


def solve_part_I():
    ranges, ingredients = read_file()
    print(ranges)
    print(ingredients)

    ranges = join_ranges(ranges)
    print(f"Merged ranges: {ranges}")

    ingredients_under_questions = ingredients
    for id_range in ranges:
        ingredients_under_questions = remove_fresh_ingredients(id_range, ingredients_under_questions)


    return len(ingredients) - len(ingredients_under_questions)

#
# result_1 = solve_part_I()
# print(result_1)



def solve_part_II():
    ranges, ingredients = read_file()
    print(ranges)
    print(ingredients)

    ranges = join_ranges(ranges)
    print(f"Merged ranges: {ranges}")

    total = 0
    for id_range in ranges:
        x, y = id_range
        total += y - x + 1

    return total




result_2 = solve_part_II()
print(result_2)