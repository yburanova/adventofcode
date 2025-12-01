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


def follow_command_and_count_zeroes(initial, command):
    direction, turns = command
    how_many_zeroes = 0

    full_turns = turns//100
    how_many_zeroes += full_turns

    turns_under_100 = turns%100

    if direction == 'R':
        end_value = initial + turns_under_100
    else:
        end_value = initial - turns_under_100

    if end_value == 0:
        how_many_zeroes += 1

    if initial > 0 > end_value:
        end_value += 100
        how_many_zeroes += 1
    elif initial >= 0 > end_value:
        end_value += 100
    elif end_value > 99:
        end_value -= 100
        how_many_zeroes += 1


    return end_value, how_many_zeroes


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


def solve_part_II():
    commands_raw = load_data(file_path)
    commands = [(command[0], int(command[1:])) for command in commands_raw]
    print(commands)

    initial = INITIAL
    how_many_0 = 0

    for command in commands:
        print(f"The turn is: {command}")
        initial,how_many_zeroes = follow_command_and_count_zeroes(initial, command)
        how_many_0 += how_many_zeroes
        print(f"Check is at: {initial}, zeroes in this turn: {how_many_zeroes}, the total amount of counted zeroes {how_many_0}")

    return how_many_0


#result_1 = solve_part_I()
#print(result_1)

result_2 = solve_part_II()
print(result_2)