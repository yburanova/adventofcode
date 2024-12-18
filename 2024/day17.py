import math
import pandas as pd
import numpy as np

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
    outs = run_program(program, reg_A, reg_B, reg_C)
    print(f'Part I: {",".join(outs)}')
    return outs


def run_program(program, reg_A, reg_B, reg_C):
    outs = []
    instruction_index = 0
    print(f"Registers at start: {reg_A}, {reg_B}, {reg_C}")
    while instruction_index < len(program):
        if program[instruction_index] != 3:
            reg_A, reg_B, reg_C, out = instructions.get(program[instruction_index])(reg_A, reg_B, reg_C,
                                                                                    program[instruction_index + 1])
            print(f"Registers after instruction {program[instruction_index]} : {reg_A}, {reg_B}, {reg_C}")
            #print(f"Registers after instruction {program[instruction_index]} : {bin(reg_A)}, {bin(reg_B)}, {bin(reg_C)}")
            if out != "":
                outs.append(str(out))
                print(f"Outputs at the point: {outs}")
        else:
            if reg_A != 0:
                instruction_index = program[instruction_index + 1]
                print(f"Moving to: {instruction_index}")
                continue

        instruction_index += 2
    print(f"Registers at end: {reg_A}, {reg_B}, {reg_C}")
    return outs

def reconstruct_initial_a(program, outputs):
    # Reverse engineer A from outputs
    outputs.reverse()  # Start with the last output
    initial_a = 0
    for i, output in enumerate(outputs):
        initial_a += int(output) * (2 ** (3 * i))  # Each output contributes 3 bits (mod 8)

    return initial_a


def process_table(table, input_column, output_filter, output_value):

    table[f"{input_column}mod8"] = table[input_column] % 8
    table[f"{input_column}mod8xor3"] = table[f"{input_column}mod8"] ^ 3
    table[f"{input_column}mod8xor3xor5"] = table[f"{input_column}mod8xor3"] ^ 5
    table[f"C_{input_column[-1]}"] = table[input_column] // np.pow(2, table[f"{input_column}mod8xor3"])
    table[f"B_{input_column[-1]}"] = table[f"{input_column}mod8xor3xor5"] ^ table[f"C_{input_column[-1]}"]
    table[output_filter] = table[f"B_{input_column[-1]}"] % 8

    # Compute the next input column for further iterations
    next_input_column = f"A{int(input_column[-1]) + 1}"
    table[next_input_column] = table[input_column] // np.pow(2, 3)

    # Filter table based on the output condition
    table = table[table[output_filter] == output_value]
    return table, next_input_column


def solve_part_ii():
    reg_A, reg_B, reg_C, program = read_file()
    must_be_result = solve_part_i()
    #reg_A_new = reconstruct_initial_a(program, must_be_result)


    table = pd.DataFrame(data = range(63687531), columns=["A0"])

    # Process A3 -> A4
    table, next_column = process_table(table, "A0", "output0", 1)
    table, next_column = process_table(table, "A1", "output1", 6)
    table, next_column = process_table(table, "A2", "output2", 7)
    table, next_column = process_table(table, "A3", "output3", 4)
    table, next_column = process_table(table, "A4", "output4", 3)
    table, next_column = process_table(table, "A5", "output5", 0)
    table, next_column = process_table(table, "A6", "output6", 5)
    table, next_column = process_table(table, "A7", "output7", 0)
    table, next_column = process_table(table, "A8", "output8", 6)

    print(table)

#solve_part_i()
solve_part_ii()
