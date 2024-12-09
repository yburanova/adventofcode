filepath = "day09.txt"

def decipher_disk(line):
    current_id = 0
    deciphered_line = []
    is_file = True

    for sign in line:
        num = int(sign)

        if is_file:
            for i in range(num):
                deciphered_line.append(str(current_id))
            current_id += 1
            is_file = False
        else:
            for i in range(num):
                deciphered_line.append('.')
            is_file = True

    return deciphered_line

def compact_file(line):
    while '.' in line:
        index = line.index('.')
        line[index] = line[-1]
        del line[-1]

    return line

def compact_file_eager(line):
    last_id = line[-1]

    while int(last_id) > 0:

        last_id_indices = [i for i, x in enumerate(line) if x == last_id]
        print("Last id ", last_id, " indices: ", last_id_indices)
        current_group = []

        for i, char in enumerate(line):

            if char == '.':
                current_group.append(i)
            else:
                if current_group:  # If a group of consecutive '.' ends
                    print("current group ", current_group)

                    if current_group[0] >= last_id_indices[0]:
                        break

                    if len(last_id_indices) <= len(current_group):
                        move_block(line, current_group, last_id_indices)
                        print(line)
                        break
                    else:
                        current_group = []
                        continue

        last_id = str(int(last_id) - 1)

        # to not hold all the ending dots in memory
        while line[-1] == '.':
            del line[-1]

    return line


def move_block(line, where_to, from_to):
    id_to_move = 0
    for index in where_to:
        line[index] = line[from_to[id_to_move]]
        line[from_to[id_to_move]] = '.'
        id_to_move += 1
        if len(from_to) == id_to_move:
            break


def calculate_checksum(line):
    result = 0
    for i in range(len(line)):
        if line[i] != '.':
            result += i * int(line[i])

    return result


def solve_part_I():
    with open(filepath) as file:
        line = file.read().strip()

    deciphered = decipher_disk(line)
    compacted = compact_file(deciphered)
    checksum = calculate_checksum(compacted)
    print(checksum)

def solve_part_II():
    with open(filepath) as file:
        line = file.read().strip()

    print(line)
    deciphered = decipher_disk(line)
    print(deciphered)
    compacted = compact_file_eager(deciphered)
    print(compacted)
    checksum = calculate_checksum(compacted)
    print(checksum)


solve_part_II()