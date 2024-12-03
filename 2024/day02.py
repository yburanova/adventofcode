import numpy as np

filepath = "day02.txt"

file_reader_gen = (row for row in open(filepath))

def solve_part_I():

    result = 0
    for row in file_reader_gen:
        nums = np.array([int(i) for i in row.split()])
        diffs = np.diff(nums)

        if (diffs > 0).all() and (diffs <= 3).all():
            result += 1

        if (diffs < 0).all() and (diffs >= -3).all():
            result += 1

    return result


result_1 = solve_part_I()
print(result_1)