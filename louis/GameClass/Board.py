from louis.GameClass import Cell, Position
from louis.Service import ServiceUtils
from louis.constants import directions


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

    def is_position_valid_for_enemy(self, position):
        if not self.is_position_in_grid(position):
            return False
        return not self.get_cell(position).is_island

    def get_cell(self, position):
        try:
            return self.map[position.y][position.x]
        except IndexError:
            return False

    def is_position_dead_end(self, position):
        available_direction = 0
        for direction in directions:
            new_position = position.add_direction(direction)
            if self.is_position_valid_for_move(new_position):
                available_direction += 1
        return available_direction == 0

    def update_enemy_potential_start_position(self, delta_position):
        for x in range(self.width):
            for y in range(self.height):
                start_position = Position(x, y)
                current_position = start_position.add_position(delta_position)
                if not self.is_position_valid_for_enemy(current_position):
                    self.get_cell(start_position).cannot_be_enemy_start()

    def compute_number_of_potential_positions(self):
        number_of_positions = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.get_cell(Position(x, y)).can_be_enemy_position:
                    number_of_positions += 1
        return number_of_positions

    def update_enemy_current_position(self, delta_position):
        for x in range(self.width):
            for y in range(self.height):
                current_position = Position(x, y)
                start_position = current_position.add_position(
                    delta_position.invert_position()
                )
                if not self.get_cell(start_position):
                    self.get_cell(current_position).can_be_enemy_position = False
                else:
                    can_be_position = self.get_cell(start_position).can_be_enemy_start
                    self.get_cell(current_position).can_be_enemy_position = can_be_position

    def reset_is_visited(self):
        for x in range(self.width):
            for y in range(self.height):
                self.get_cell(Position(x=x, y=y)).reset_visit()

    def reset_could_be_start(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(Position(x=x, y=y))
                cell.can_be_enemy_start = not cell.is_island

    def update_board_torpedo_did_not_hit_in_position(self, torpedo_position, delta_position):
        torpedo_delta_range = [-1, 0, 1]
        for x in torpedo_delta_range:
            for y in torpedo_delta_range:
                torpedo_delta_position = Position(x, y)
                current_position_without_enemy_boat = torpedo_position.add_position(torpedo_delta_position)
                start_position_without_enemy_boat = current_position_without_enemy_boat.add_position(
                    delta_position.invert_position()
                )
                start_cell = self.get_cell(start_position_without_enemy_boat)
                if start_cell:
                    start_cell.cannot_be_enemy_start()
        self.update_enemy_current_position(delta_position)

    def print_potential_position_board(self):
        for line in self.map:
            line_string = ""
            for cell in line:
                line_string += cell.print_can_be_here()
            ServiceUtils.print_log(line_string)
