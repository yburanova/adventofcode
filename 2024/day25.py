filepath = "day25.txt"

def read_file(filepath):
    schemata = []
    last_schema = []
    with open(filepath) as file:
        for line in file.readlines():
            if line.strip() == '':
                schemata.append(last_schema)
                last_schema = []
            else:
                last_schema.append(line.strip())

        schemata.append(last_schema)

    return schemata

def convert(schemata):
    keys = []
    locks = []

    for schema in schemata:
        code = [0 for i in range(5)]
        if '#' in schema[0]: # lock
            for i in range(1, len(schema)):
                line = [1 if sign == '#' else 0 for sign in schema[i]]
                code = [x + y for x, y in zip(code, line)]
            locks.append(code)
        else:
            for i in range(0, len(schema) - 1):
                line = [1 if sign == '#' else 0 for sign in schema[i]]
                code = [x + y for x, y in zip(code, line)]
            keys.append(code)
    return locks, keys

def is_fitting(lock, key):
    for i in range(5):
        if lock[i] + key[i] > 5:
            return False

    return True

def find_fitting(locks, keys):
    fitting_pairs = []
    for lock in locks:
        for key in keys:
            if is_fitting(lock, key):
                fitting_pairs.append((lock,key))

    return fitting_pairs



def solve_part_i():
    schemata = read_file(filepath)
    locks, keys = convert(schemata)
    fitting_pairs = find_fitting(locks, keys)
    print(f"Part I: {len(fitting_pairs)}")

solve_part_i()
