import numpy as np

filepath = "day02.txt"

file_reader_gen = (row.split() for row in open(filepath))

def get_nums(file_reader_gen):
    nums_array = []
    for row in file_reader_gen:
        nums_array.append(np.array([int(i) for i in row]))

    return nums_array

def solve_part_I():

    result = 0
    for row in file_reader_gen:
        nums = np.array([int(i) for i in row])
        if is_safe(nums):
            result += 1

    print("Part I:", result)

def is_safe(nums):
    diffs = np.diff(nums)
    if (diffs > 0).all() and (diffs <= 3).all():
        return True

    if (diffs < 0).all() and (diffs >= -3).all():
        return True

    return False

def solve_part_ii():
    nums_list = get_nums(file_reader_gen)
    result = 0
    for nums in nums_list:
        if is_safe(nums):
            result += 1
            continue

        for i in range(len(nums)):
            nums_copy = np.delete(nums, i)
            if is_safe(nums_copy):
                result += 1
                break
    print("Part II", result)

solve_part_I()
solve_part_ii()