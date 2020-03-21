from louis.GameClass import Cell, Position
from louis.Service import ServiceUtils
from louis.constants import directions

directions = ["N", "W", "E", "S"]

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
            ServiceUtils.print_log(line_string)
