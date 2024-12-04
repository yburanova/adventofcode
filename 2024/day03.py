import re

filepath = "day03.txt"
pattern_mul = r"mul\((\d{1,3}),(\d{1,3})\)"
pattern_do_dont = r"do\(\)(.*?)don't\(\)"

def solve_part_I():
    with open(filepath) as file:
        lines = file.readlines()

    result = 0
    for line in lines:
        reg_result = re.findall(pattern_mul, line)
        result += sum(int(i) * int(j) for i, j in reg_result)

    print(result)

def solve_part_II():
    with open(filepath) as file:
        line = "do()" + file.read().replace('\n', '') + "don't()"

    result = 0

    tokens = re.findall(pattern_do_dont, line)
    for token in tokens:
        reg_result = re.findall(pattern_mul, token)

        result += sum(int(i) * int(j) for i, j in reg_result)

    print(result)

solve_part_I()
solve_part_II()