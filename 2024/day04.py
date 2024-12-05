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


def solve_part_I():
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

    print(result)



solve_part_I()