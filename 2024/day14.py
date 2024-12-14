import math
import numpy as np
import pygame
import time

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

def robots_to_array(field, robots):
    canvas = np.full((field[1], field[0]), 0)

    for robot in robots:
        canvas[robot.y][robot.x] = 1

    return canvas


def solve_part_ii():
    robots = read_file()
    field = (101, 103)

    # Initialize pygame
    pygame.init()

    # Set up dimensions
    rows, cols = field  # Size of the 2D array
    cell_size = 10  # Size of each cell in pixels
    width, height = cols * cell_size, rows * cell_size

    # Create a 2D array filled with '.'
    array = np.full((rows, cols), '.', dtype=str)

    # Set up the screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("2D Array Visualization")

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BEIGE = (255, 216, 172)

    def draw_grid(arr):
        for row in range(rows):
            for col in range(cols):
                # Determine the color based on the value in the array
                if arr[row, col] == '.':
                    color = BEIGE  # Color for '.'
                else:
                    color = RED  # Color for 'X'

                # Draw the cell
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                )
                # Draw a border around the cell
                pygame.draw.rect(
                    screen,
                    BLACK,
                    pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size),
                    1
                )

    # Main loop
    running = True
    second = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        print(f"Second: {second}")
        # array = np.full((rows, cols), '.', dtype=str)
        if second < 100000:
            for robot in robots:
                array[robot.x, robot.y] = 'X'
                move_robot(robot, 1, field)
            second += 1

        # Clear the screen
        # screen.fill(BEIGE)

        # Draw the updated grid
        draw_grid(array)
        pygame.image.save(screen, f"second_{second}.png")
        array = np.full((rows, cols), '.', dtype=str)

        # Update the display
        pygame.display.flip()

        # Delay for visibility
        # time.sleep(0.5)

    # Quit pygame
    pygame.quit()


solve_part_ii()