import math
from functools import cmp_to_key

filepath = "day05.txt"

class Node:

    def __init__(self, key, children):
        self.key = key
        self.children = set()
        self.children.add(children)

    def __repr__(self):
        return f"({self.key}: {self.children})"


def clean_chain(chain):
    clean_chain = {}

    for node in chain:
        if node.key not in clean_chain.keys():
            clean_chain[node.key] = node.children
        else:
            clean_chain[node.key].update(node.children)

    return clean_chain


def get_chain_and_orders():
    chain = []
    orders = []
    with open(filepath) as file:
        for line in file:
            if "|" in line:
                value, child = line.strip().split("|")
                chain.append(Node(value, child))
            elif "," in line:
                order = line.strip().split(",")
                orders.append(order)

    cleaned_chain = clean_chain(chain)
    return cleaned_chain, orders


def get_sum_middle_nums(correct_orders):
    return sum(int(order[math.floor(len(order) / 2)]) for order in correct_orders)


def correct_order(command1, command2, command_chain):
    if command_chain.get(command1) is not None and command2 in command_chain[command1]:
        return True
    else:
        return False


def is_order_correct(order, command_chain):
    print("incoming order:", order, end='')
    for i in range(len(order)):
        for j in range(i+1, len(order)):
            # order[i] must be always larger than order[j]
            #print("Order 1:", order[i], ", Order 2:", order[j])
            if not correct_order(order[i], order[j], command_chain):
                return False
    return True


def solve_part_I():
    chain, orders = get_chain_and_orders()
    correct_orders = []
    incorrect_orders = []
    for order in orders:
        if is_order_correct(order, chain):
            print(" All correct")
            correct_orders.append(order)
        else:
            print(" Incorrect")
            incorrect_orders.append(order)

    result = get_sum_middle_nums(correct_orders)
    print("Part I:", result)

    return incorrect_orders


def solve_part_II(incorrect_orders):
    chain, _ = get_chain_and_orders()

    def compare_pages(a, b):
        if b in chain.get(a, set()):
            return -1  # a must come before b
        elif a in chain.get(b, set()):
            return 1  # b must come before a
        return 0  # no specific order between a and b

    corrected_orders = []
    for incorrect_order in incorrect_orders:
        # Sort the incorrect order using the custom comparator
        sorted_order = sorted(incorrect_order, key=cmp_to_key(compare_pages))
        corrected_orders.append(sorted_order)

    # Calculate the sum of middle numbers for corrected orders
    result = get_sum_middle_nums(corrected_orders)
    print("Part II:", result)



orders_to_correct_in_part_II = solve_part_I()
solve_part_II(orders_to_correct_in_part_II)