file_path = "day01.txt"

def get_left_right_lists(file_path):
    left = []
    right = []

    with open(file_path, 'r') as file:
        for line in file:
            left_token, right_token = line.strip().split()
            left.append(int(left_token))
            right.append(int(right_token))

    return left, right

def solve_part_I():
    left, right = get_left_right_lists(file_path)
    return sum(abs(r - l) for l, r in zip(sorted(left), sorted(right)))

def solve_part_II():
    left, right = get_left_right_lists(file_path)
    return sum(i * right.count(i) for i in left)


result_1 = solve_part_I()
print(result_1)

result_2 = solve_part_II()
print(result_2)