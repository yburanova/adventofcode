import math

filepath = "day17.txt"

def read_file():
    with open(filepath) as file:
        for line in file.readlines():
            if line.startswith("Register A"):
                reg_A = int(line.strip().split()[-1])
            elif line.startswith("Register B"):
                reg_B = int(line.strip().split()[-1])
            elif line.startswith("Register C"):
                reg_C = int(line.strip().split()[-1])
            elif line.startswith("Program"):
                program = list(map(int, line.strip().split()[-1].split(",")))

    return reg_A, reg_B, reg_C, program

def combi_operand(a, b, c, operand):
    if operand == 4:
        return a
    if operand == 5:
        return b
    if operand == 6:
        return c
    if operand == 7:
        print("Something is wrong, Operator cannot be 7")

    return operand

def adv(a,b,c, operand):
    operand = combi_operand(a, b, c, operand)
    a = int(a // math.pow(2, operand))
    return a, b, c, ""

def bxl(a, b,c, operand):
    b = b^operand
    return a, b, c, ""

def bst(a,b,c,operand):
    operand = combi_operand(a, b, c, operand)
    b = operand%8
    return a, b, c, ""

def bxc(a,b,c,operand):
    operand = combi_operand(a, b, c, operand)
    b = b^c
    return a, b, c, ""

def out(a,b,c,operand):
    operand = combi_operand(a, b, c, operand)
    result = operand%8
    return a, b, c, result

def bdv(a,b,c, operand):
    operand = combi_operand(a, b, c, operand)
    b = int(a // math.pow(2, operand))
    return a, b, c, ""

def cdv(a,b,c, operand):
    operand = combi_operand(a, b, c, operand)
    c = int(a // math.pow(2, operand))
    return a, b, c, ""

instructions = {
    0: adv,
    1: bxl,
    2: bst,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}

def solve_part_i():
    reg_A, reg_B, reg_C, program = read_file()
    outs = []

    instruction_index = 0
    while instruction_index < len(program):
        print(f"Registers: {reg_A}, {reg_B}, {reg_C}")
        if program[instruction_index] != 3:
            reg_A, reg_B, reg_C, out = instructions.get(program[instruction_index])(reg_A, reg_B, reg_C, program[instruction_index + 1])
            if out != "":
                outs.append(str(out))
        else:
            if reg_A != 0:
                instruction_index = program[instruction_index + 1]
                continue

        instruction_index += 2
    print(f"Registers: {reg_A}, {reg_B}, {reg_C}")
    print(",".join(outs))
    print("".join(outs))

solve_part_i()
