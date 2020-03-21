import sys
import random

directions = ["N", "W", "E", "S"]


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_direction(self, direction):
        if direction == "N":
            return Position(self.x, self.y - 1)

        if direction == "W":
            return Position(self.x - 1, self.y)

        if direction == "S":
            return Position(self.x, self.y + 1)

        if direction == "E":
            return Position(self.x + 1, self.y)

    def __str__(self):
        return "x: {} / y: {}".format(self.x, self.y)


class Ship(object):
    def __init__(self):
        self.position = Position(0, 0)
        self.direction = "N"

    def move(self, direction):
        self.direction = direction
        self.position = self.position.add_direction(direction)

    def get_position_after_move(self, direction):
        return self.position.add_direction(direction)

    def __str__(self):
        return str(self.position)


class Cell(object):
    def __init__(self, position, is_island):
        self.position = position
        self.is_island = is_island
        self.is_visited = False

    def has_been_visited(self):
        self.is_visited = True

    def is_valid_for_move(self):
        return not (self.is_island or self.is_visited)

    def __str__(self):
        return "x" if self.is_island else "."

    def reset_visit(self):
        self.is_visited = False


class Board(object):
    def __init__(self, height, width, lines):
        self.height = height
        self.width = width
        self.map = []
        for y, line in enumerate(lines):
            cell_line = []
            for x, char in enumerate(line):
                cell_line.append(Cell(Position(x, y), char == "x"))
            self.map.append(cell_line)

    def is_position_in_grid(self, position):
        if position.x < 0 or position.x >= self.width:
            return False
        if position.y < 0 or position.y >= self.height:
            return False
        return True

    def is_position_valid_for_move(self, position):
        if not self.is_position_in_grid(position):
            return False
        return self.get_cell(position).is_valid_for_move()

    def get_cell(self, position):
        return self.map[position.y][position.x]

    def is_position_dead_end(self, position):
        available_direction = 0
        for direction in directions:
            new_position = position.add_direction(direction)
            if self.is_position_valid_for_move(new_position):
                available_direction += 1
        return available_direction == 0

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


def choose_starting_cell(ship, board):
    x = random.randint(0, board.width - 1)
    y = random.randint(0, board.height - 1)
    random_position = Position(x, y)
    while not board.is_position_valid_for_move(random_position):
        random_position.x = random.randint(0, board.width - 1)
        random_position.y = random.randint(0, board.height - 1)
    ship.position = random_position
    print("{} {}".format(ship.position.x, ship.position.y))


def is_move_possible_in_direction(ship, direction, board):
    next_position = ship.get_position_after_move(direction)
    return board.is_position_valid_for_move(next_position)


def move_my_ship(ship, direction, board):
    board.get_cell(position=ship.position).has_been_visited()
    ship.move(direction)
    move_order = "MOVE {} TORPEDO".format(direction)
    return move_order


def random_turn(direction):
    if direction in ["S", "N"]:
        return random.choice(["E", "W"])
    return random.choice(["S", "N"])


def chose_movement_and_move(ship, board):
    direction = ship.direction
    while not is_move_possible_in_direction(ship, direction, board):
        if board.is_position_dead_end(ship.position):
            return False
        direction = random_turn(ship.direction)
    move_order = move_my_ship(ship, direction, board)
    return move_order


def surface(board):
    for x in range(board.width):
        for y in range(board.height):
            board.get_cell(Position(x=x, y=y)).reset_visit()
    print("SURFACE")


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
    move_order = chose_movement_and_move(my_ship, board)
    if not move_order:
        surface(board)
    else:
        print(move_order)
