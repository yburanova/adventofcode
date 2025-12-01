from functools import lru_cache

filepath = "day19.txt"

def read_file():
    lines = [line.strip() for line in open(filepath)]

    towels = lines[0].split(", ")
    designs = lines[2:]

    return  towels, designs

def is_composite(string, parts):
    if not string:
        return True
    for part in parts:
        if string.startswith(part):
            if is_composite(string[len(part):], parts):
                return True
    return False

def clean_towels(towels):
    towels = list(set(towels))
    towels = set(sorted(towels, key = len))
    cleaned_towels = [
        towel for towel in towels if not is_composite(towel, towels - {towel})
    ]

    return cleaned_towels

def find_combination(design, towels):
    all_fitting_start_towels = [towel for towel in towels if design.startswith(towel)]
    #print("Design: ", design)
    #print("All fitting towels", all_fitting_start_towels)
    result = False
    for towel in all_fitting_start_towels:
        #print("Checking towel ", towel)
        if len(design[len(towel):]) != 0:
            result = find_combination(design[len(towel):], towels)
            if result:
                return True
            else:
                continue
        else:
            #print("Design Found")
            return True

    return result

def find_all_combinations(design, towels):

    @lru_cache(None)
    def helper(design):
        # Base case: if the design is empty, we found a valid combination
        if not design:
            return [[]]  # Return a list with an empty combination

        # Get all towels that fit the start of the current design
        all_fitting_start_towels = [towel for towel in towels if design.startswith(towel)]

        # If no towels fit, return empty list
        if not all_fitting_start_towels:
            return []

        # Store all valid combinations for the current design
        all_combinations = []

        # Try each towel and recursively find combinations
        for towel in all_fitting_start_towels:
            remaining_design = design[len(towel):]
            sub_combinations = helper(remaining_design)

            # Limit memory usage by avoiding nested combination generation if sub_combinations is too large
            #if len(sub_combinations) > 50000:  # Arbitrary threshold to prevent memory explosion
            #    continue

            all_combinations.extend([[towel] + combination for combination in sub_combinations])

        return all_combinations

    return helper(design)


def solve_part_i():
    towels, designs = read_file()
    towels = clean_towels(towels)
    result = 0
    for design in designs:
        print(f"Design: {design}")
        if find_combination(design, towels):
            result += 1
        print("-------------------------------------------------------------------------------")

    print(f"Part I: {result}")

def solve_part_ii():
    towels, designs = read_file()
    cleaned_towels = clean_towels(towels)
    result = 0
    working_designs = []
    for design in designs:
        if find_combination(design, cleaned_towels):
            working_designs.append(design)

    print(f"Found all {len(working_designs)} working combinations")
    for design in working_designs:
        print("Design", design)
        combinations = find_all_combinations(design, towels)
        #print(combinations)
        result += len(combinations)

    print(f"Part I: {result}")

# solve_part_i()
solve_part_ii()
