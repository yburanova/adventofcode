import numpy as np

filepath = "day15_test.txt"

directions = {
    '^': (0, -1), # (x,y)
    'v':  (0, 1),
    '>': (1, 0),
    '<': (-1, 0)
}

class Robot():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Robot at: {self.x}, {self.y}"

def get_stones_and_walls():
    field = []
    commands = []
    with open(filepath) as file:
        for line in file.readlines():
            if line.startswith('#'):
                field.append(line.strip())
            elif line[0] in "<v>^":
                commands.extend(list(line.strip()))

    stones = []
    walls = []
    canvas_size = (len(field[0]), len(field))
    robot = Robot(0,0)
    for i, line in enumerate(field):
        for j, sign in enumerate(line):
            if sign == '#':
                walls.append((j, i))
            elif sign == 'O':
                stones.append((j, i))
            elif sign == '@':
                robot = Robot(j, i)

    #print(stones)
    #print(walls)
    #print(robot)
    #print(canvas_size)
    return canvas_size, stones, walls, robot, commands

def print_canvas(canvas_size, walls, stones, robot, left_stones = [], right_stones = []):
    canvas = np.full((canvas_size[1], canvas_size[0]), '.')
    for wall in walls:
        canvas[wall[1]][wall[0]] = '#'
    for stone in stones:
        canvas[stone[1]][stone[0]] = 'O'
    for stone in left_stones:
        canvas[stone[1]][stone[0]] = '['
    for stone in right_stones:
        canvas[stone[1]][stone[0]] = ']'
    canvas[robot.y][robot.x] = '@'

    print(canvas)

def move(command, stones, walls, robot):
    direction = directions.get(command)
    # print(command)
    where = robot.x + direction[0], robot.y + direction[1]
    if where not in walls and where not in stones:
        robot.x += direction[0]
        robot.y += direction[1]

    if where in stones:
        to_move = [where]
        next_element = where[0], where[1]
        while True:
            next_element = next_element[0] + direction[0], next_element[1] + direction[1]
            if next_element not in walls and next_element not in stones:
                break
            elif next_element in stones:
                to_move.append(next_element)
            elif next_element in walls:
                to_move = [] # no moves, there is a wall in front!
                break

        if len(to_move) != 0:
            new_positions = []
            for stone_to_move in to_move:
                new_positions.append((stone_to_move[0] + direction[0], stone_to_move[1] + direction[1]))

            stones = [e for e in stones if e not in to_move]
            stones.extend(new_positions)
            robot.x += direction[0]
            robot.y += direction[1]

    if where in walls:
        # no move!
        return robot, stones

    # print(robot)
    return robot, stones

def solve_part_i():
    canvas_size, stones, walls, robot, commands = get_stones_and_walls()
    print_canvas(canvas_size, walls, stones, robot)

    for command in commands:
        robot, stones = move(command, stones, walls, robot)

    print("Final: ")
    print_canvas(canvas_size, walls, stones, robot)
    result = 100*sum(stone[1] for stone in stones) + sum(stone[0]  for stone in stones)
    print("Part I:", result)

def double_walls(positions):
    new_positions = []
    for position in positions:
        new_positions.append((position[0] * 2, position[1]))
        new_positions.append((position[0] * 2 + 1, position[1]))
    return new_positions

def double_stones(positions):
    left_stones = []
    right_stones = []
    for position in positions:
        left_stones.append((position[0] * 2, position[1]))
        right_stones.append((position[0] * 2 + 1, position[1]))
    return left_stones, right_stones

def move_double(command, walls, robot, left_stones, right_stones):
    direction = directions.get(command)
    # print(command)
    where = robot.x + direction[0], robot.y + direction[1]
    if where not in walls and where not in left_stones and where not in right_stones:
        # empty space, just move the robot
        robot.x += direction[0]
        robot.y += direction[1]
        return robot, left_stones, right_stones

    if where in walls:
        # no move!
        return robot, left_stones, right_stones

    if command == '<' and where in right_stones:
        to_move_right = [where]
        next_element = where[0], where[1]
        to_move_left = []
        while True:
            next_element = next_element[0] + direction[0], next_element[1] + direction[1]
            if next_element not in walls and next_element not in left_stones and next_element not in right_stones:
                break
            elif next_element in right_stones:
                to_move_right.append(next_element)
            elif next_element in left_stones:
                to_move_left.append(next_element)
            elif next_element in walls:
                to_move_right = [] # no moves, there is a wall in front!
                break

        if len(to_move_right) != 0:
            return move_stones(direction, robot, left_stones, right_stones, to_move_left, to_move_right)

    if command == '>' and where in left_stones:
        to_move_left = [where]
        next_element = where[0], where[1]
        to_move_right = []
        while True:
            next_element = next_element[0] + direction[0], next_element[1] + direction[1]
            if next_element not in walls and next_element not in left_stones and next_element not in right_stones:
                break
            elif next_element in right_stones:
                to_move_right.append(next_element)
            elif next_element in left_stones:
                to_move_left.append(next_element)
            elif next_element in walls:
                to_move_left = [] # no moves, there is a wall in front!
                break

        if len(to_move_left) != 0:
            return move_stones(direction, robot, left_stones, right_stones, to_move_left, to_move_right)

    if command == '^' and where in left_stones or where in right_stones:
        to_move_left = []
        to_move_right = []

        if where in left_stones:
            to_move_left.append(where)
            to_move_right.append((where[0] + 1, where[1]))


    # print(robot)
    return robot, left_stones, right_stones

def move_stones_up_or_down(direction, where, walls, robot, left_stones, right_stones):
    to_move_left = []
    to_move_right = []

    if where in left_stones:
        to_move_left.append(where)
        to_move_right.append((where[0] + 1, where[1]))

        next_element_left = where[0], where[1]
        next_element_right = where[0] + 1, where[1]


def move_stones(direction, robot, left_stones, right_stones, to_move_left, to_move_right):
    new_positions = []
    for stone_to_move in to_move_right:
        new_positions.append((stone_to_move[0] + direction[0], stone_to_move[1] + direction[1]))
    right_stones = [e for e in right_stones if e not in to_move_right]
    right_stones.extend(new_positions)

    new_positions = []
    for stone_to_move in to_move_left:
        new_positions.append((stone_to_move[0] + direction[0], stone_to_move[1] + direction[1]))
    left_stones = [e for e in left_stones if e not in to_move_left]
    left_stones.extend(new_positions)

    robot.x += direction[0]
    robot.y += direction[1]
    return robot, left_stones, right_stones


def solve_part_ii():
    canvas_size, stones, walls, robot, commands = get_stones_and_walls()
    print(canvas_size)
    print_canvas(canvas_size, walls, stones, robot)

    canvas_size = (canvas_size[0] * 2, canvas_size[1])
    left_stones, right_stones = double_stones(stones)
    walls = double_walls(walls)
    robot = Robot(robot.x * 2, robot.y)
    print_canvas(canvas_size, walls, [], robot, left_stones, right_stones)

    for command in commands:
        robot, left_stones, right_stones = move_double(command, walls, robot, left_stones, right_stones)

    print("Final: ")
    print_canvas(canvas_size, walls, [], robot, left_stones, right_stones)

#solve_part_i()
solve_part_ii()