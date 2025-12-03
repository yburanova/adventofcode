import numpy as np

filepath = "day03.txt"


def read_file():
    return [line.strip() for line in open(filepath)]

def find_max_in_bank_two_numbers(bank):
    print(bank)
    all_numbers_in_lines = [int(i) for i in set(bank)]
    max_num = max(all_numbers_in_lines)
    pos_max_num = bank.index(str(max_num))
    print(f"Max num: {max_num}, at position: {pos_max_num}")

    if pos_max_num < len(bank) - 1:
        rest_of_line = bank[pos_max_num+1:]
        print(f"Rest of line: {rest_of_line}")
        all_numbers_in_rest_line = [int(i) for i in set(rest_of_line)]
        max_num_in_rest = max(all_numbers_in_rest_line)
        return int(str(max_num) + str(max_num_in_rest))
    else: # max num is at the end of line
        rest_of_line = bank[:pos_max_num]
        print(f"Rest of line: {rest_of_line}")
        all_numbers_in_rest_line = [int(i) for i in set(rest_of_line)]
        max_num_in_rest = max(all_numbers_in_rest_line)
        return int(str(max_num_in_rest) + str(max_num))


def solve_part_I():
    banks = read_file()
    total = 0
    for bank in banks:
        max_joltage = find_max_in_bank_two_numbers(bank)
        print(f"Found max joltage: {max_joltage}")
        total += max_joltage

    return total


def find_max_in_bank_twelve_numbers(bank):
    print(bank)
    bank_len = len(bank)

    to_remove = bank_len - 12
    stack = []

    for num in bank:
        while to_remove > 0 and stack and stack[-1] < num:
            stack.pop()
            to_remove -= 1
        stack.append(num)

    if to_remove > 0:
        stack = stack[:-to_remove]

    result_digits = stack[:12]
    return int(''.join(result_digits))




def solve_part_II():
    banks = read_file()
    total = 0
    for bank in banks:
        max_joltage = find_max_in_bank_twelve_numbers(bank)
        print(f"Found max joltage: {max_joltage}")
        total += max_joltage

    return total


# result_1 = solve_part_I()
# print(result_1)

result_2 = solve_part_II()
print(result_2)