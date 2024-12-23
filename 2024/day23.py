from itertools import combinations

filepath = "day23.txt"

def read_file(filepath):
    return (line.strip().split("-") for line in open(filepath))

def find_three_comp_connections(connections):
    connections_map = {}
    for connection in connections:
        comp1, comp2 = connection
        connections_map[comp2] = connections_map.get(comp2, []) + [comp1]
        connections_map[comp1] = connections_map.get(comp1, []) + [comp2]

    three_comp_connections = set()
    for key, value in connections_map.items():
        possible_connection_couples = combinations(value, 2)
        for couple in possible_connection_couples:
            comp1, comp2 = couple
            if comp2 in connections_map.get(comp1):
                l = sorted([key, comp1, comp2])
                three_comp_connections.add(tuple(l))

    return three_comp_connections

def is_with_t(three_comp_connection):
    for comp in three_comp_connection:
        if comp.startswith('t'):
            return True

    return False

def filter_with_t(three_comp_connections):
    return [connection for connection in three_comp_connections if is_with_t(connection)]

def solve_part_i():
    connections_gen = read_file(filepath)
    three_comp_connections = find_three_comp_connections(connections_gen)
    three_comp_connections_with_t  =filter_with_t(three_comp_connections)
    print(f"Part I: {len(three_comp_connections_with_t)}")

solve_part_i()