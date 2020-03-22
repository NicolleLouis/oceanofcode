

import math
import random
import sys
directions = ["E", "S", "W", "N"]
opp_life_previous = 6
opp_life = 6
class Ship(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.past_moves = []
        self.dx = 0
        self.dy = 0
        self.torpedo_cooldown = -1
    def do_actions(self, action):
        if "MOVE N" in action:
            self.y -= 1
            self.dy -= 1
        if "MOVE E" in action:
            self.x += 1
            self.dx += 1
        if "MOVE S" in action:
            self.y += 1
            self.dy += 1
        if "MOVE W" in action:
            self.x -= 1
            self.dx -= 1
        if action == "SURFACE":
            board.clear_visits()
        return action
    def possible_moves(self, board):
        possible_moves = []
        for direction in directions:
            if board.get_cell_in_direction(self.x, self.y, direction).is_cell_valid():
                possible_moves.append("MOVE " + direction + " TORPEDO")
        return possible_moves
    def best_move_action(self, board):
        possible_moves = self.possible_moves(board)
        if len(possible_moves) > 0:
            if opp_life_previous != opp_life and enemy_orders + " TORPEDO" in possible_moves:
                return enemy_orders + "TORPEDO"
            else:
                return possible_moves[0]
        else:
            return "SURFACE"
    def best_attack_action(self, board):
        for cell in board.possible_enemy_cells:
            distance_to_cell = board.get_distance(board.get_cell(self.x, self.y), cell)
            # TODO: add probability based on how many cells in the area
            if distance_to_cell <= 4 and self.torpedo_cooldown == 0:
                return "TORPEDO " + str(cell.x) + " " + str(cell.y)
        return "DUNNO"
    def best_action(self, board):
        best_attack = self.best_attack_action(board)
        if best_attack == "DUNNO":
            return self.best_move_action(board)
        else:
            return best_attack
    def update_enemy_action(self, action):
        if "MOVE N" in action:
            self.dy -= 1
        if "MOVE E" in action:
            self.dx += 1
        if "MOVE S" in action:
            self.dy += 1
        if "MOVE W" in action:
            self.dx -= 1
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
        self.islands = []
        self.possible_enemy_starting_cells = []
        self.possible_enemy_cells = []
        for y, line in enumerate(lines):
            cell_line = []
            for x, char in enumerate(line):
                cell = Cell(x, y, char == "x")
                cell_line.append(cell)
                if char == "x":
                    self.islands.append(cell)
                else:
                    self.possible_enemy_starting_cells.append(cell)
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
        #return an island cell if out of grid
        else:
            return Cell(-1, -1, True)
    def is_position_valid(self, x, y):
        return self.get_cell(x, y).is_cell_valid()
    def is_position_island(self, x, y):
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
    def get_cell_from_vector(self, cell, dx, dy):
        return self.get_cell(cell.x + dx, cell.y + dy)
    def update_possible_starting_cells(self, enemy_ship):
        dx = enemy_ship.dx
        dy = enemy_ship.dy
        for cell_line in self.map:
            for cell in cell_line:
                if self.get_cell_from_vector(cell, dx, dy).is_island:
                    try:
                        self.possible_enemy_starting_cells.remove(cell)
                    # out of bounds cell will raise exceptions
                    except:
                        pass
    def update_possible_enemy_cells(self, enemy_ship):
        dx = enemy_ship.dx
        dy = enemy_ship.dy
        self.update_possible_starting_cells(enemy_ship)
        possible_cells = []
        for cell_line in self.map:
            for cell in cell_line:
                if cell in self.possible_enemy_starting_cells:
                    possible_cells.append(self.get_cell_from_vector(cell, dx, dy))
        self.possible_enemy_cells = possible_cells
    # to do: add pathing algo, to compute real distance.
    def get_distance(self, cell1, cell2):
        return math.fabs(cell1.x - cell2.x) + math.fabs(cell1.y - cell2.y)
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
    enemy_orders = input()
    return {
        "x": x,
        "y": y,
        "my_life": my_life,
        #"opp_life_previous" : opp_life_previous,
        "opp_life": opp_life,
        "torpedo_cooldown": torpedo_cooldown,
        "sonar_cooldown": sonar_cooldown,
        "silence_cooldown": silence_cooldown,
        "sonar_result": sonar_result,
        "enemy_orders": enemy_orders,
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
enemy_ship = Ship()
choose_starting_cell(my_ship, board)
# game loop
while True:
    turn_data = read_turn_data()
    my_ship.x = turn_data['x']
    my_ship.y = turn_data['y']
    my_ship.torpedo_cooldown = turn_data['torpedo_cooldown']
    my_ship_cell = board.get_cell(my_ship.x, my_ship.y)
    my_ship_cell.visit()
    enemy_orders = turn_data['enemy_orders']
    enemy_ship.update_enemy_action(enemy_orders)
    board.update_possible_enemy_cells(enemy_ship)
    best_action = my_ship.best_action(board)
    opp_life_previous = opp_life
    print(my_ship.do_actions(best_action))
