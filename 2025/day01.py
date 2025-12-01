file_path = "day01.txt"

INITIAL = 50

def load_data(filepath):
    return [line.strip() for line in open(filepath)]


def follow_command(initial, command):
    direction, turns = command
    if direction == 'R':
        initial = initial + turns
    else:
        initial = initial - turns

    while initial < 0:
        initial += 100
    while initial > 99:
        initial -= 100

    return initial


def solve_part_I():
    commands_raw = load_data(file_path)
    commands = [(command[0], int(command[1:])) for command in commands_raw]
    print(commands)

    initial = INITIAL
    how_many_0 = 0

    for command in commands:
        initial = follow_command(initial, command)
        print(f"Check is at: {initial}")
        if initial == 0:
            how_many_0 += 1

    return how_many_0


# def solve_part_II():
#     left, right = get_left_right_lists(file_path)
#     return sum(i * right.count(i) for i in left)


result_1 = solve_part_I()
print(result_1)

# result_2 = solve_part_II()
# print(result_2)