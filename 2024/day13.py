from collections import namedtuple
from sympy import symbols, Eq, solve, Integer

filepath = "day13.txt"

Prize = namedtuple('Prize', 'x y')
Button = namedtuple('Button', 'x y')
Machine = namedtuple('Machine', 'prize button_a button_b')

def read_file(part = 1):
    with open(filepath) as file:
        machines = []
        button_a = None
        button_b = None
        prize = None
        for line in file.readlines():
            if line.startswith("Button A"):
                button_a = get_button(line)
            elif line.startswith("Button B"):
                button_b = get_button(line)
            elif line.startswith("Prize"):
                prize = get_prize(line, part)
            else: # empty line
                machines.append(Machine(prize, button_a, button_b))

    return machines

def get_prize(line, part = 1):
    tokens = line.strip().split()
    x = int(tokens[1].split("=")[1][:-1])
    y = int(tokens[2].split("=")[1])
    if part == 2:
        x += 10000000000000
        y += 10000000000000
    return Prize(x, y)

def get_button(line):
    tokens = line.strip().split()
    x = int(tokens[2].split("+")[1][:-1])
    y = int(tokens[3].split("+")[1])
    return Button(x, y)

def solve_machine_equation(machine: Machine):
    x, y = symbols('x y')

    eq1 = Eq(machine.button_a.x * x + machine.button_b.x * y, machine.prize.x)
    eq2 = Eq(machine.button_a.y * x + machine.button_b.y * y, machine.prize.y)

    solution = solve((eq1, eq2), (x, y))

    return solution[x], solution[y]

def solve_part_i():
    machines = read_file()
    sum_tokens = 0
    for machine in machines:
        print(machine)
        push_a, push_b = solve_machine_equation(machine)
        print(push_a, ",", push_b)

        if isinstance(push_a, Integer) and isinstance(push_b, Integer):
            if int(push_a) <= 100 and int(push_b) <= 100:
                sum_tokens += int(push_a) * 3 + int(push_b)

    print(f"Part I: {sum_tokens}")

def solve_part_ii():
    machines = read_file(part = 2)
    sum_tokens = 0
    for machine in machines:
        print(machine)
        push_a, push_b = solve_machine_equation(machine)
        print(push_a, ",", push_b)

        if isinstance(push_a, Integer) and isinstance(push_b, Integer):
            sum_tokens += int(push_a) * 3 + int(push_b)

    print(f"Part II: {sum_tokens}")

solve_part_ii()