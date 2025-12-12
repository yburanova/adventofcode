
from collections import namedtuple

filepath = "day12.txt"

Shape = namedtuple('Shape', 'index form area full_area')
Region = namedtuple('Region', 'form quantity')

def read_file():
    shapes = []
    regions = []
    with open(filepath) as file:
        shape_index = 0
        shape_form = []


        for line in file.readlines():
            if ':' in line and 'x' not in line:
                shape_index = int(line.strip()[0])
            elif '#' in line or '.' in line:
                shape_form.append([1 if sign == '#' else 0 for sign in line.strip()])
            elif 'x' in line:
                tokens = line.strip().split(' ')
                region_quantities = list(map(int, tokens[1:]))
                region_form = list(map(int, tokens[0][:-1].split('x')))
                regions.append(Region(region_form, region_quantities))
            else:
                # empty
                full_area = len(shape_form) * len(shape_form[0])
                area = sum(y for x in shape_form for y in x)
                shapes.append(Shape(shape_index, shape_form, area, full_area))
                shape_form = []

    shapes_map = {shape.index: shape for shape in shapes}

    return shapes_map, regions

def solve_region(region, shapes):
    totally_required_area = sum(quantity * shapes[idx].area for idx, quantity in enumerate(region.quantity))
    totally_required_full_area = sum(quantity * shapes[idx].full_area for idx, quantity in enumerate(region.quantity))
    region_area = region.form[0] * region.form[1]
    area_frac = totally_required_area / region_area
    full_area_frac = totally_required_full_area / region_area
    print(f"Region: {region}; Area: {region_area}; All shapes would need the area: {totally_required_area}, that is {area_frac * 100}%; If we ignore the shape - required area is {totally_required_full_area}, that is {full_area_frac * 100}%")
    return area_frac < 1, full_area_frac < 1

def solve_part_I():
    shapes, regions = read_file()
    print(shapes)
    print(regions)

    counter = 0
    counter_ignore_shape = 0
    for region in regions:
        is_fittable, is_fittable_ignore_shape = solve_region(region, shapes)
        if is_fittable:
            counter += 1
        if is_fittable_ignore_shape:
            counter_ignore_shape += 1

    print(f"Totally: {counter}")
    print(f"And if we ignore shapes: {counter_ignore_shape}")
    return counter



result_1 = solve_part_I()
print(result_1)


# def solve_part_II():
#     nodes = read_file()
#     #print(nodes)
#
#     G = create_graph(nodes)
#
#     print(nx.is_directed_acyclic_graph(G))
#
#     paths = count_paths_with_fft_and_dac(G, 'svr', 'out', 'fft', 'dac')
#     return paths
#
#
# result_2 = solve_part_II()
# print(result_2)
