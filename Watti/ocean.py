import math
import random
import sys

directions = ["E", "S", "W", "N"]

class Ship(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.past_moves = []
        self.dx = 0
        self.dy = 0

    def move(self, direction):
        if direction == "N":
            self.y -= 1

        if direction == "E":
            self.x += 1

        if direction == "S":
            self.y += 1

        if direction == "W":
            self.x -= 1

    def possible_moves(self, board):
        possible_moves = []
        for direction in directions:
            if board.get_cell_in_direction(self.x, self.y, direction).is_cell_valid():
                possible_moves.append("MOVE " + direction)
        return possible_moves

    def best_action(self, board):
        possible_moves = self.possible_moves(board)
        if len(possible_moves) > 0:
            return possible_moves[0]
        else:
            board.clear_visits()
            return "SURFACE"

    def __str__(self):
        return "x: {} / y: {}".format(self.x, self.y)


class Cell(object):
    def __init__(self, x, y, is_island):
        self.x = x
        self.y = y
        self.is_island = is_island
        self.is_visited = False

    def visit(self):
        self.is_visited = True

    def is_cell_valid(self):
        return not (self.is_island or self.is_visited)

    def __str__(self):
        return "x" if self.is_island else "."


class Board(object):
    def __init__(self, height, width, lines):
        self.height = height
        self.width = width
        self.map = []
        for y, line in enumerate(lines):
            cell_line = []
            for x, char in enumerate(line):
                cell_line.append(Cell(x, y, char == "x"))
            self.map.append(cell_line)

    def is_position_in_grid(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True

    def get_cell(self, x, y):
        if self.is_position_in_grid(x, y):
            return self.map[y][x]
        else:
            return Cell(-1, -1, True)

    def is_position_valid(self, x, y):
        return self.get_cell(x, y).is_cell_valid()

    def is_cell_island(self, x, y):
        return self.get_cell(x, y).is_island()

    def get_cell_in_direction(self, x, y, direction):
        if direction == "N":
            return self.get_cell(x, y - 1)
        if direction == "E":
            return self.get_cell(x + 1, y)
        if direction == "S":
            return self.get_cell(x, y + 1)
        if direction == "W":
            return self.get_cell(x - 1, y)

    def get_sector_center(self, sector):
        return self.get_cell(2 + 5 * int((sector - 1) / 3), 2 + 5 * int((sector - 1) % 3))

    def available_cells_in_sector(self, sector):
        count = 0
        center = self.get_sector_center(sector)
        for i in range(-2,3):
            for j in range(-2,3):
                if self.is_position_valid(center.x+i, center.y+j):
                    count+=1
        return count

    def clear_visits(self):
        for cell_line in self.map:
            for cell in cell_line:
                cell.is_visited = False

    def print_board(self):
        for line in self.map:
            line_string = ""
            for cell in line:
                line_string += str(cell)
            print_log(line_string)

def print_log(log):
    print(log, file=sys.stderr)

def vectToDir(x):
    ints=[[1, 0], [0, 1], [-1, 0], [0, -1]]
    strs=["E", "S", "W", "N"]
    return strs[ints.index(x)]

def dirToVect(x):
    ints=[[1, 0], [0, 1], [-1, 0], [0, -1]]
    strs=["E", "S", "W", "N"]
    return ints[strs.index(x)]

def nextPositionFromVect(x, y, vect):
    return [x + vect[0], y + vect[1]]

def nextPositionFromDir(x, y, dir):
    return nextPositionFromVect(x, y, dirToVect(dir))

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


def choose_starting_cell(ship, board):
    x = int(board.width / 2)
    y = int(board.height / 2)
    valid_position_found = board.is_position_valid(x,y)
    while not valid_position_found:
        x += random.randint(-1,1)
        y += random.randint(-1,1)
        valid_position_found = board.is_position_valid(x,y)
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
    board=board
)

# game loop
while True:
    turn_data = read_turn_data()
    my_ship.x = turn_data['x']
    my_ship.y = turn_data['y']
    board.get_cell(turn_data['x'], turn_data['y']).visit()
    print(my_ship.best_action(board))
