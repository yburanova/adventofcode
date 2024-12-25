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
    current_stack_z_nodes = [wire for wire, value in current_stack.items() if wire.startswith('z')]
    if len(current_stack_z_nodes) == len(z_nodes):
        return True
    else:
        return False

def get_value(wire, gates, current_stack):
    wire_value = current_stack.get(wire)
    if wire_value is not None:
        return wire_value
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


def complete_wires(current_stack, gates, z_node):
    get_value(z_node, gates, current_stack)


def simulate_for_z(initial_values, gates, z_nodes):
    current_stack = initial_values
    for z_node in z_nodes:
        complete_wires(current_stack, gates, z_node)
        if all_z_set(current_stack, z_nodes):
            break

    return {node: value for node, value in current_stack.items() if node.startswith('z')}

def return_binary(z_value_map):
    sorted_map = {key: z_value_map[key] for key in sorted(z_value_map.keys())}
    result = ''
    for node, value in sorted_map.items():
        result += str(value)

    return result[::-1]




def solve_part_i():
    initial_values, gates, z_nodes = read_file(filepath)
    z_value_map = simulate_for_z(initial_values, gates, z_nodes)
    binary_value = return_binary(z_value_map)
    print(binary_value)
    print(f"Part I: {int(binary_value, 2)}")


solve_part_i()