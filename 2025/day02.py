import numpy as np

filepath = "day02.txt"


def read_file():
    input = [line.strip().split(",") for line in open(filepath)][0]
    ranges = [i.split("-") for i in input]
    return [(int(r[0]), int(r[1])) for r in ranges]

def find_invalid_ids_part_I(range):
    all_numbers = np.arange(range[0], range[1]+1)
    print(all_numbers)
    invalid_ids = []
    for num in all_numbers:
        num_str = str(num)
        if len(num_str) % 2 != 0:
            continue
        else:
            half_len = len(num_str) // 2
            if num_str[:half_len] == num_str[half_len:]:
                print(f"invalid id: {num_str}")
                invalid_ids.append(int(num))

    return invalid_ids


def find_invalid_ids_part_II(incoming_range):
    all_numbers = np.arange(incoming_range[0], incoming_range[1] + 1)
    print(all_numbers)
    invalid_ids = set()
    for num in all_numbers:
        num_str = str(num)
        tokens = [num_str[:i] for i in range(1, len(num_str) // 2 + 1)]
        for token in tokens:
            if len(num_str) % len(token) != 0:
                continue

            repetitions = len(num_str) // len(token)
            if token * repetitions == num_str:
                invalid_ids.add(int(num))

    return invalid_ids


def solve_part_I():
    ranges = read_file()
    print(ranges)

    all_invalid_ids = []
    for range in ranges:
        invalid_ids = find_invalid_ids_part_I(range)
        all_invalid_ids.extend(invalid_ids)

    print(all_invalid_ids)
    return sum(all_invalid_ids)


def solve_part_II():
    ranges = read_file()

    all_invalid_ids = set()
    for range in ranges:
        invalid_ids = find_invalid_ids_part_II(range)
        all_invalid_ids.update(invalid_ids)

    print(all_invalid_ids)
    return sum(all_invalid_ids)



# result_1 = solve_part_I()
# print(result_1)

result_2 = solve_part_II()
print(result_2)