import numpy as np

file_path = "day01.txt"

def get_left_right_lists(file_path):
    left = []
    right = []

    with open(file_path) as file:
        for line in file.readlines():
            left_token, right_token = line.split()
            left.append(int(left_token))
            right.append((int(right_token.replace('\n', ''))))

    return left, right

def solve_part_I():
    left, right = get_left_right_lists(file_path)
    left_np = np.array(left)
    left_np.sort()

    right_np = np.array(right)
    right_np.sort()

    return sum(np.abs(right_np - left_np))

def solve_part_II():
    left, right = get_left_right_lists(file_path)
    return sum(i * right.count(i) for i in left)


result_1 = solve_part_I()
print(result_1)

result_2 = solve_part_II()
print(result_2)