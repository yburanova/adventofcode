from collections import namedtuple
import networkx as nx
from itertools import combinations
from pyvis.network import Network

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

def visualize(gates):
    graph_list = {gate.out_node: [gate.in_node1, gate.in_node2] for key, gate in gates.items()}
    print(graph_list)
    G = nx.DiGraph(graph_list)
    nt = Network('600px', '600px', directed=True)
    nt.from_nx(G)
    nt.show('nx.html', notebook=False)

def test_swaps(gates, swaps, initial_values, z_nodes, expected_sum):
    print("Swapping", swaps)
    swapped_gates = gates.copy()

    for a, b in swaps:
        swapped_gates[a], swapped_gates[b] = (
            Gate(swapped_gates[b].in_node1, swapped_gates[b].in_node2, a, swapped_gates[b].gate),
            Gate(swapped_gates[a].in_node1, swapped_gates[a].in_node2, b, swapped_gates[a].gate),
        )

    result = simulate_for_z(initial_values, swapped_gates, z_nodes)

    z_value_binary = ''.join(str(result[node]) for node in sorted(z_nodes))
    z_value = int(z_value_binary, 2)
    print(z_value_binary)
    return z_value == expected_sum

def find_swaps(initial_values, gates):
    x_nodes = sorted([node for node in initial_values if node.startswith('x')])
    y_nodes = sorted([node for node in initial_values if node.startswith('y')])
    z_nodes = sorted([node for node in gates if node.startswith('z')])

    x_value = int(''.join(str(initial_values[node]) for node in x_nodes)[::-1], 2)
    y_value = int(''.join(str(initial_values[node]) for node in y_nodes)[::-1], 2)
    expected_sum = x_value + y_value
    expected_sum = str(bin(expected_sum))[2:]
    print("Expected Z values", expected_sum)

    initial_z_value_map = simulate_for_z(initial_values, gates, z_nodes)
    initial_binary_value = return_binary(initial_z_value_map)
    print("Initial Z values", initial_binary_value)

    problematic_wires = set()
    for i in range(len(initial_binary_value)):
        if initial_binary_value[-i-1] != expected_sum[-i-1]:
            problematic_wires.add(f"z{i:02}")

    # Only consider gates involved in problematic nodes
    for gate in gates.values():
        if gate.out_node in problematic_wires:
            if gate.in_node1 in gates:
                problematic_wires.add(gate.in_node1)
            if gate.in_node2 in gates:
                problematic_wires.add(gate.in_node2)


    possible_swaps = combinations(problematic_wires, 2)

    for swaps in combinations(possible_swaps, 4):
        flat_swaps = {item for pair in swaps for item in pair}
        if len(flat_swaps) != 8:
            continue

        if test_swaps(gates, swaps, initial_values, z_nodes, expected_sum):
            return sorted(flat_swaps)

    return []

def solve_part_i():
    initial_values, gates, z_nodes = read_file(filepath)
    z_value_map = simulate_for_z(initial_values, gates, z_nodes)
    binary_value = return_binary(z_value_map)
    print(binary_value)
    print(f"Part I: {int(binary_value, 2)}")

def solve_part_ii():
    initial_values, gates, z_nodes = read_file(filepath)
    #visualize(gates)
    swapped_wires = find_swaps(initial_values, gates)
    print(f"Part II: {','.join(swapped_wires)}")


#solve_part_i()
solve_part_ii()