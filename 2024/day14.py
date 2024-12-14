import math

filepath = "day14.txt"

class Robot:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def __repr__(self):
        return f"Robot at [{self.x}, {self.y}], Velocities are Vx: {self.vx}, Vy: {self.vy}"

def split_cells(string):
    return map(int, string.split("=")[1].split(","))

def read_file():
    robots = []
    with open(filepath) as file:
        for line in file.readlines():
            ps, vs = line.strip().split()
            x, y = split_cells(ps)
            vx, vy = split_cells(vs)
            robots.append(Robot(x, y, vx, vy))

    return robots

def move_robot(robot, times, field):
    c_x = robot.x + times * robot.vx
    c_y = robot.y + times * robot.vy

    robot.x = c_x % field[0]
    robot.y = c_y % field[1]

    return robot

def define_quadrants(field):
    field_middle_x = field[0] // 2
    field_middle_y = field[1] // 2

    q1 = (0, field_middle_x), (0, field_middle_y) # x_range, y_range
    q2 = (field_middle_x + 1, field[0]), (0, field_middle_y)
    q3 = (0, field_middle_x), (field_middle_y + 1, field[1])
    q4 = (field_middle_x + 1, field[0]), (field_middle_y + 1, field[1])

    return [q1, q2, q3, q4]


def filter_robot_in_quadrant(robot, x_range, y_range):
    if robot.x in list(range(x_range[0], x_range[1])) and robot.y in list(range(y_range[0], y_range[1])):
        return True
    else:
        return False


def solve_part_i():
    robots = read_file()
    field = (101, 103)
    quadrants = define_quadrants(field)
    robot_in_quadrant = {}

    for robot in robots:
        print(f"Robot before: {robot}")
        move_robot(robot, 100, field)
        print(f"Robot after 100s: {robot}")

        for q in quadrants:
            if filter_robot_in_quadrant(robot, q[0], q[1]):
                robot_in_quadrant[q] = robot_in_quadrant.get(q, 0) + 1

        print(robot_in_quadrant)
        result = math.prod(v for k,v in robot_in_quadrant.items())
        print(f"Part I: {result}")

solve_part_i()