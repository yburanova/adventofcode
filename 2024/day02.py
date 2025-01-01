import numpy as np

filepath = "day02.txt"

def load_data(filepath):
    with open(filepath) as file:
        return [np.array(list(map(int, row.split()))) for row in file]

def is_safe(nums):
    diffs = np.diff(nums)
    if (diffs > 0).all() and (diffs <= 3).all():
        return True

    if (diffs < 0).all() and (diffs >= -3).all():
        return True

    return False

def solve_part_i():
    data = load_data(filepath)
    result = sum(is_safe(nums) for nums in data)
    print("Part I:", result)

def solve_part_ii():
    data = load_data(filepath)
    result = 0
    for nums in data:
        if is_safe(nums):
            result += 1
        else:
            result += any(is_safe(np.delete(nums, i)) for i in range(len(nums)))
    print("Part II", result)

solve_part_i()
solve_part_ii()