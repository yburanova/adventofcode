import numpy as np

filepath = "day15.txt"

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

    print(stones)
    print(walls)
    print(robot)
    print(canvas_size)
    return canvas_size, stones, walls, robot, commands

def print_canvas(canvas_size, walls, stones, robot):
    canvas = np.full(canvas_size, '.')
    for wall in walls:
        canvas[wall[1]][wall[0]] = '#'
    for stone in stones:
        canvas[stone[1]][stone[0]] = 'O'
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
    print(result)

solve_part_i()