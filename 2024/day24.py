from collections import namedtuple

filepath = "day24.txt"

Gate = namedtuple('Gate', 'in_node1 in_node2 out_node gate')

def read_file(filepath):
    initial_wire_values = {}
    gates = {}
    z_nodes = set()

    with open(filepath) as file:
        for line in file.readlines():
            if "->" in line:
                in_nodes, out_node = line.strip().split(" -> ")
                in_node1, gate, in_node2 = in_nodes.split()
                gates[out_node] = Gate(in_node1, in_node2, out_node, gate)
                if out_node.startswith('z'):
                    z_nodes.add(out_node)

            elif ":" in line:
                node, value = line.strip().split(": ")
                initial_wire_values[node] = int(value)

    return initial_wire_values, gates, z_nodes


def all_z_set(current_stack, z_nodes):
    return all(wire in current_stack for wire in z_nodes)

def get_value(wire, gates, current_stack):
    if wire in current_stack:
        return current_stack[wire]

    else:
        gate = gates[wire]
        value1 = get_value(gate.in_node1, gates, current_stack)
        value2 = get_value(gate.in_node2, gates, current_stack)

        if gate.gate == 'AND':
            output = value1 and value2
        elif gate.gate == 'OR':
            output = value1 or value2
        elif gate.gate == 'XOR':
            output = value1 ^ value2

        current_stack[wire] = output
        return output

def simulate_for_z(initial_values, gates, z_nodes):
    current_stack = initial_values
    for z_node in z_nodes:
        get_value(z_node, gates, current_stack)
        if all_z_set(current_stack, z_nodes):
            break

    return {node: value for node, value in current_stack.items() if node.startswith('z')}

def return_binary(z_value_map):
    return ''.join(str(z_value_map[node]) for node in sorted(z_value_map.keys()))[::-1]


def solve_part_i():
    initial_values, gates, z_nodes = read_file(filepath)
    z_value_map = simulate_for_z(initial_values, gates, z_nodes)
    binary_value = return_binary(z_value_map)
    print(binary_value)
    print(f"Part I: {int(binary_value, 2)}")


solve_part_i()