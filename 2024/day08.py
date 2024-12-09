from itertools import combinations
filepath = "day08.txt"


def get_field_and_antennas():
    antenna_map = {}
    with open(filepath) as file:
        row = 0
        for line in file.readlines():
            tokens = list(line.strip())
            for column in range(len(tokens)):
                if tokens[column] != '.':
                    if antenna_map.get(tokens[column]):
                        antenna_map.get(tokens[column]).append((row, column))
                    else:
                        antenna_map[tokens[column]] = [(row, column)]
            row += 1

        print((row,column))
    print(antenna_map)
    return antenna_map, (row, column)


def print_field_and_result(antinodes, field):
    print(field)
    for i in range(field[0]):
        for j in range(field[1]):
            if (i, j) in antinodes:
                print('#', end='')
            else:
                print('.', end='')
        print()
    # print(antinodes)
    print(len(antinodes))




def solve_part_I():
    antenna_map, field = get_field_and_antennas()

    antinodes = set()
    for key, values in antenna_map.items():
        combis = combinations(values, 2)
        for combi in combis:
            # print(combi)
            point_1 = combi[0]
            point_2 = combi[1]
            dx = point_1[0] - point_2[0]
            dy = point_1[1] - point_2[1]

            antinode_1 = (point_1[0] + dx, point_1[1] + dy)
            antinode_2 = (point_2[0] - dx, point_2[1] - dy)

            # print(antinode_1)
            # print(antinode_2)

            if field[0] > antinode_1[0] >= 0 and field[1] >= antinode_1[1] >= 0:
                antinodes.add(antinode_1)

            if field[0] > antinode_2[0] >= 0 and field[1] >= antinode_2[1] >= 0:
                antinodes.add(antinode_2)

    print_field_and_result(antinodes, field)

def generate_antinodes(point_a, point_b, field_bounds):
    """Generate antinodes along the line defined by two points."""
    antinodes = set()
    dx = point_a[0] - point_b[0]
    dy = point_a[1] - point_b[1]

    # Traverse in the forward direction
    x, y = point_a[0], point_a[1]
    while 0 <= x < field_bounds[0] and 0 <= y < field_bounds[1]:
        antinodes.add((x, y))
        x += dx
        y += dy

    # Traverse in the backward direction
    x, y = point_b[0], point_b[1]
    while 0 <= x < field_bounds[0] and 0 <= y < field_bounds[1]:
        antinodes.add((x, y))
        x -= dx
        y -= dy

    return antinodes

def solve_part_II():
    antenna_map, field = get_field_and_antennas()

    antinodes = set()
    for key, values in antenna_map.items():
        combis = combinations(values, 2)
        for combi in combis:
            # print(combi)
            point_1 = combi[0]
            point_2 = combi[1]

            antinodes.add(point_1)
            antinodes.add(point_2)

            dx = point_1[0] - point_2[0]
            dy = point_1[1] - point_2[1]

            new_x = point_1[0]
            new_y = point_1[1]

            while True:
                new_x += dx
                new_y += dy

                if field[0] > new_x >= 0 and field[1] >= new_y >= 0:
                    antinodes.add((new_x, new_y))
                else:
                    break

            new_x = point_2[0]
            new_y = point_2[1]

            while True:
                new_x -= dx
                new_y -= dy

                if field[0] > new_x >= 0 and field[1] >= new_y >= 0:
                    antinodes.add((new_x, new_y))
                else:
                    break




    print_field_and_result(antinodes, field)


#solve_part_I()
solve_part_II()