import sys
import math
import random


class Ship(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction):
        if direction == "N":
            self.y -= 1

        if direction == "E":
            self.x -= 1

        if direction == "S":
            self.y += 1

        if direction == "W":
            self.x += 1

    def __str__(self):
        return "x: {} / y: {}".format(self.x, self.y)


class Cell(object):
    def __init__(self, x, y, is_island):
        self.x = x
        self.y = y
        self.is_island = is_island
        self.is_visited = False

    def __str__(self):
        return "x" if self.is_island else "."


class Board(object):
    def __init__(self, height, width, lines):
        self.map = []
        for y, line in enumerate(lines):
            cell_line = []
            for x, char in enumerate(line):
                cell_line.append(Cell(x, y, char == "x"))
            self.map.append(cell_line)

    def get_cell(self, x, y):
        return self.map[y][x]

    def print_board(self):
        for line in self.map:
            line_string = ""
            for cell in line:
                line_string += str(cell)
            print_log(line_string)


def print_log(log):
    print(log, file=sys.stderr)


def read_turn_data():
    x, y, my_life, opp_life, torpedo_cooldown, \
    sonar_cooldown, silence_cooldown, \
    mine_cooldown = [int(i) for i in input().split()]
    sonar_result = input()
    opponent_orders = input()
    return {
        "x": x,
        "y": y,
        "my_life": my_life,
        "opp_life": opp_life,
        "torpedo_cooldown": torpedo_cooldown,
        "sonar_cooldown": sonar_cooldown,
        "silence_cooldown": silence_cooldown,
        "sonar_result": sonar_result,
        "opponent_orders": opponent_orders,
    }


def read_global_data():
    width, height, my_id = [int(i) for i in input().split()]
    lines = []
    for i in range(height):
        lines.append(input())
    return {
        "width": width,
        "height": height,
        "lines": lines
    }


def is_cell_island(x, y, lines):
    return lines[y][x] == "x"


def choose_starting_cell(ship, lines, width, height):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    while is_cell_island(x, y, lines):
        print_log("{} {} {}".format(x, y, is_cell_island(x, y, lines)))
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
    ship.x = x
    ship.y = y
    print("{} {}".format(ship.x, ship.y))


# Read global input
global_data = read_global_data()
board = Board(
    height=global_data["height"],
    width=global_data["width"],
    lines=global_data["lines"]
)

my_ship = Ship()
choose_starting_cell(
    ship=my_ship,
    lines=global_data["lines"],
    width=global_data["width"],
    height=global_data["height"],
)

# game loop
while True:
    turn_data = read_turn_data()
    print_log(str(my_ship))
    my_ship.move("N")
    print("MOVE N TORPEDO")
