from itertools import product

filepath = "day07.txt"

def solve_part_I():
    lines = (line.strip() for line in open(filepath))

    correct_lines = []
    result = 0
    for line in lines:
        result += process_line(correct_lines, line)

    print(result)


def solve_part_II():
    lines = (line.strip() for line in open(filepath))

    correct_lines = []
    result = 0
    for line in lines:
        result += process_line(correct_lines, line, "+*|")

    print(result)


def get_equation_result(eq_params, sign_combi):
    result = eq_params[0]

    for i in range(len(sign_combi)):
        if sign_combi[i] == '+':
            result += eq_params[i+1]
        elif sign_combi[i] == "*":
            result *= eq_params[i+1]
        elif sign_combi[i] == "|":
            result = int(str(result) + str(eq_params[i+1]))

    return result


def process_line(correct_lines, line, signs = "+*"):
    value, param_str = line.split(":")
    params = [int(param) for param in param_str.split()]
    value = int(value)

    for combi in product(signs, repeat=len(params) - 1):

        if value == get_equation_result(params, combi):
            print(line)
            correct_lines.append(line)
            return value

    return 0


#solve_part_I()
solve_part_II()