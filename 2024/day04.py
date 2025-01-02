filepath = "day04.txt"

def search_in_lines(lines):
    result = 0
    for line in lines:
        result += line.count("XMAS")
        result += line.count("SAMX")

    return result

def transpose_and_search(lines):
    result = 0
    new_lines = [''.join(list(x)) for x in zip(*lines)]
    result += search_in_lines(new_lines)
    return result


def solve_part_i():
    lines = [line.strip() for line in open(filepath)]

    result = 0

    # straight
    result += search_in_lines(lines)

    # transposed
    result += transpose_and_search(lines)

    # create diagonals
    new_lines = []
    for i in range(len(lines)):
        new_line = '.'*i + lines[i] + '.'*(len(lines) - i - 1)
        new_lines.append(new_line)
    result += transpose_and_search(new_lines)

    new_lines = []
    for i in range(len(lines)):
        new_line = '.'*(len(lines) - i - 1) + lines[i] + '.'*i
        new_lines.append(new_line)
    result += transpose_and_search(new_lines)

    print("Part I:", result)


def is_x_mas(pos_a, lines):
    if pos_a[0] == 0 or pos_a[0] == len(lines) - 1 or pos_a[1] == 0 or pos_a[1] == len(lines[0]) - 1:
        return False

    diag_1 = f"{lines[pos_a[0] - 1][pos_a[1] - 1]}A{lines[pos_a[0] + 1][pos_a[1] + 1]}"
    diag_2 = f"{lines[pos_a[0] + 1][pos_a[1] - 1]}A{lines[pos_a[0] - 1][pos_a[1] + 1]}"

    if diag_1 in ['MAS', 'SAM'] and diag_2 in ['MAS', 'SAM']:
        return True

    return False


def solve_part_ii():
    lines = [line.strip() for line in open(filepath)]
    all_a_positions = []
    for i, row in enumerate(lines):
        for j, sign in enumerate(row):
            if sign == 'A':
                all_a_positions.append((i,j))

    result = 0
    for pos_a in all_a_positions:
        if is_x_mas(pos_a, lines):
            result += 1

    print("Part II:", result)

solve_part_i()
solve_part_ii()