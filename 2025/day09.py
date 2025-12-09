
from itertools import permutations
from shapely.geometry.polygon import Polygon

filepath = "day09.txt"


def read_file():
    return [list(map(int, line.strip().split(","))) for line in open(filepath)]

def normalize_coordinates(all_coordinates):
    min_x = min(x for (x, y) in all_coordinates)
    min_y = min(y for (x, y) in all_coordinates)

    return [(x - min_x, y - min_y) for x, y in all_coordinates]

def calculate_area(coordinates_pair):
    area = (abs(coordinates_pair[0][0] - coordinates_pair[1][0]) + 1) * (abs(coordinates_pair[0][1] - coordinates_pair[1][1]) + 1)
    print(f"Pair of coordinates to calculate: {coordinates_pair}, the area is: {area}")
    return area


def solve_part_I():
    all_coordinates = read_file()
    print(all_coordinates)

    return max(calculate_area(perm) for perm in permutations(all_coordinates, 2))

# result_1 = solve_part_I()
# print(result_1)


def solve_part_II():
    all_coordinates = read_file()
    print(all_coordinates)

    polygon = Polygon(all_coordinates)

    max_area = 0
    for perm in permutations(all_coordinates, 2):
        polygon_to_prove = Polygon([perm[0], (perm[0][0], perm[1][1]), perm[1], (perm[1][0], perm[0][1])])
        if polygon.contains(polygon_to_prove):
            max_area = max(max_area, calculate_area(perm))

    return max_area



result_2 = solve_part_II()
print(result_2)
