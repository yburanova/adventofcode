from pyvis.network import Network
import networkx as nx
from collections import deque, namedtuple

filepath = "day11.txt"

Node = namedtuple('Node', 'label outputs')

def read_file():
    nodes = []
    with open(filepath) as file:
        for line in file.readlines():
            tokens = line.strip().split(" ")
            node = Node(tokens[0][:-1], tokens[1:])
            nodes.append(node)

    return nodes

def create_graph(nodes):
    graph_list = {node.label: node.outputs for node in nodes}
    #print(graph_list)
    G = nx.DiGraph(graph_list)
    #visualize(G)
    return G

def visualize(G):
    nt = Network('600px', '600px', directed=True)
    nt.from_nx(G)
    nt.show('nx.html', notebook=False)


def solve_part_I():
    nodes = read_file()
    print(nodes)

    G = create_graph(nodes)

    return len(list(nx.all_simple_paths(G, source='you', target='out')))


# result_1 = solve_part_I()
# print(result_1)

def count_paths_with_fft_and_dac(G, source, target,
                                 fft_node='fft', dac_node='dac'):

    # states:
    #   0 -> seen_fft = 0, seen_dac = 0
    #   1 -> seen_fft = 1, seen_dac = 0
    #   2 -> seen_fft = 0, seen_dac = 1
    #   3 -> seen_fft = 1, seen_dac = 1

    def state_idx(seen_fft, seen_dac):
        return (1 if seen_fft else 0) + (2 if seen_dac else 0)

    topo = list(nx.topological_sort(G))

    # 4 per node for the 4 states above
    counts = {v: [0, 0, 0, 0] for v in G.nodes}

    # initialise at source
    seen_fft = (source == fft_node)
    seen_dac = (source == dac_node)
    counts[source][state_idx(seen_fft, seen_dac)] = 1

    for u in topo:
        cu = counts[u]
        if not any(cu):
            continue  # no paths reach u

        for v in G.successors(u):
            is_fft = (v == fft_node)
            is_dac = (v == dac_node)

            # propagate all 4 states from u to v
            for idx, c in enumerate(cu):
                if c == 0:
                    continue

                # decode current state
                sf = bool(idx & 1)
                sd = bool(idx & 2)

                # update with v
                new_sf = sf or is_fft
                new_sd = sd or is_dac
                new_idx = state_idx(new_sf, new_sd)
                counts[v][new_idx] += c

    # only paths that have seen BOTH fft and dac at the target
    return counts[target][3]


def solve_part_II():
    nodes = read_file()
    #print(nodes)

    G = create_graph(nodes)

    print(nx.is_directed_acyclic_graph(G))

    paths = count_paths_with_fft_and_dac(G, 'svr', 'out', 'fft', 'dac')
    return paths


result_2 = solve_part_II()
print(result_2)
