import math
from collections import defaultdict

from numpy._core.strings import isdigit

filepath = "day08.txt"


def read_file():
    return [list(map(int, line.strip().split(","))) for line in open(filepath)]

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        # path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def build_edges(all_coordinates):
    edges = []
    n = len(all_coordinates)
    for i in range(n):
        x1, y1, z1 = all_coordinates[i]
        for j in range(i + 1, n):
            x2, y2, z2 = all_coordinates[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            d2 = dx * dx + dy * dy + dz * dz  # squared distance is enough
            edges.append((d2, i, j))
    edges.sort(key=lambda e: e[0])
    return edges


def solve_part_I(num_connections):
    all_coordinates = read_file()
    print(all_coordinates)

    n = len(all_coordinates)

    edges = build_edges(all_coordinates)
    #print(f"All edges: {edges}")

    uf = UnionFind(n)

    for _, i, j in edges[:num_connections]:
        uf.union(i, j)

    comp_sizes = defaultdict(int)
    for i in range(n):
        root = uf.find(i)
        comp_sizes[root] += 1

    sizes = sorted(comp_sizes.values(), reverse=True)

    if len(sizes) < 3:
        return None

    return sizes[0] * sizes[1] * sizes[2]



# result_1 = solve_part_I(num_connections=1000)
# print(result_1)


def solve_part_II():
    all_coordinates = read_file()
    n = len(all_coordinates)
    edges = build_edges(all_coordinates)
    uf = UnionFind(n)

    components = n
    last_pair = None

    for d2, i, j in edges:
        if uf.union(i, j):
            components -= 1
            last_pair = (all_coordinates[i], all_coordinates[j])
            if components == 1:
                break

    if last_pair is None:
        return None  # should not happen with valid input

    (x1, _, _), (x2, _, _) = last_pair
    return x1 * x2


result_2 = solve_part_II()
print(result_2)
