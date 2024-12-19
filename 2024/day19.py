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
            print("Design Found")
            return True


    return result

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

solve_part_i()
