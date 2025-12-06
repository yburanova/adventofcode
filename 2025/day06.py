import math

from numpy._core.strings import isdigit

filepath = "day06.txt"


def read_file():
    all_lines= [line.strip().split(" ") for line in open(filepath)]
    all_lines = [[sign for sign in line if sign != ''] for line in all_lines]
    return all_lines

def solve_line(line):
    sign = line[-1]
    if sign == '+':
        return sum(int(sign) for sign in line[:-1])
    elif sign == '*':
        return math.prod(int(sign) for sign in line[:-1])

def solve_part_I():
    all_lines = read_file()
    print(all_lines)

    transposed = tuple(zip(*all_lines))
    print(transposed)

    result = 0
    for line in transposed:
        line_solution = solve_line(line)
        result += line_solution

    return result

# result_1 = solve_part_I()
# print(result_1)

def read_file_part_II():
    lines= [line.rstrip("\n") for line in open(filepath)]
    return lines


def calculate(last_sign, nums):
    if last_sign == '+':
        return sum(int(sign) for sign in nums)
    elif last_sign == '*':
        return math.prod(int(sign) for sign in nums)


def solve_part_II():
    all_lines = read_file_part_II()

    max_len = max(len(line) for line in all_lines)
    updated_all_lines = [line.ljust(max_len) for line in all_lines] # all lines must have equal length

    transposed = zip(*updated_all_lines)

    result = 0
    nums = []
    last_sign = ''

    for line in transposed:
        num = ''

        for sign in line:
            if isdigit(sign):
                num += sign
            if sign == '+' or sign == '*':
                last_sign = sign

        if num == '':
            r = calculate(last_sign, nums)
            result += r
            print(f"Numbers {nums} with sign: {last_sign} gives result: {r}")
            nums = []
            last_sign = ''
        else:
            nums.append(int(num))

    r = calculate(last_sign, nums)
    result += r
    print(f"Numbers {nums} with sign: {last_sign} gives result: {r}")

    return result


result_2 = solve_part_II()
print(result_2)