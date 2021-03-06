from louis.GameClass import Cell, Position
from louis.Service import ServiceUtils
from louis.constants import DIRECTIONS


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

    def compute_is_in_move_range(self, cell):
        if (not cell.is_in_move_range) and cell.is_valid_for_move():
            cell.is_in_move_range = True
            neighbours = self.get_neighbours(cell)
            for neighbour in neighbours:
                self.compute_is_in_move_range(neighbour)

    def get_number_of_potential_move_position_from_position(self, position):
        self.set_is_in_move_range_false()
        # Beware we are entering recursions
        self.compute_is_in_move_range(self.get_cell(position))
        number_of_move_position = self.compute_number_of_move_position_in_range()
        self.set_is_in_move_range_false()
        return number_of_move_position

    def get_neighbours(self, cell):
        neighbours = []
        for (x, y) in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]:
            neighbour_position = Position(x, y).add_position(cell.position)
            if bool(self.get_cell(neighbour_position)):
                neighbours.append(self.get_cell(neighbour_position))
        return neighbours

    def get_all_cells(self):
        cells = []
        for x in range(self.width):
            for y in range(self.height):
                cells.append(self.get_cell(Position(x, y)))
        return cells

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

    def enemy_not_in_sector(self, sector):
        cells = self.get_all_cells()
        for cell in cells:
            if cell.sector != sector:
                cell.can_be_enemy_position = False

    def is_position_dead_end(self, position):
        available_direction = 0
        for direction in DIRECTIONS:
            new_position = position.add_direction(direction)
            if self.is_position_valid_for_move(new_position):
                available_direction += 1
        return available_direction == 0

    def update_enemy_potential_start_position_from_geography(self, delta_position):
        for x in range(self.width):
            for y in range(self.height):
                start_position = Position(x, y)
                current_position = start_position.add_position(delta_position)
                if not self.is_position_valid_for_enemy(current_position):
                    self.get_cell(start_position).cannot_be_enemy_start()

    def update_enemy_potential_start_position(self, delta_position):
        for x in range(self.width):
            for y in range(self.height):
                start_position = Position(x, y)
                current_position = start_position.add_position(delta_position)
                cell = self.get_cell(current_position)
                if cell:
                    if not self.get_cell(current_position).can_be_enemy_position:
                        self.get_cell(start_position).cannot_be_enemy_start()

    def enemy_is_in_range(self, range_detection, attack_position):
        cells = self.get_all_cells()
        for cell in cells:
            if cell.position.get_distance(attack_position) > range_detection:
                cell.can_be_enemy_position = False

    def compute_number_of_potential_positions(self):
        number_of_positions = 0
        cells = self.get_all_cells()
        for cell in cells:
            if cell.can_be_enemy_position:
                number_of_positions += 1
        return number_of_positions

    def compute_number_of_move_position_in_range(self):
        number_of_move_positions = 0
        cells = self.get_all_cells()
        for cell in cells:
            if cell.is_in_move_range:
                number_of_move_positions += 1
        return number_of_move_positions

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
        cells = self.get_all_cells()
        for cell in cells:
            cell.reset_visit()

    def reset_could_be_start(self):
        cells = self.get_all_cells()
        for cell in cells:
            cell.can_be_enemy_start = not cell.is_island

    def update_possible_start_position_after_silence_from_current_position(self, position):
        for x in range(-4, 4, 1):
            delta_position = Position(x, 0)
            new_position = position.add_position(delta_position)
            cell_new_position = self.get_cell(new_position)
            if cell_new_position:
                cell_new_position.can_be_enemy_start = not cell_new_position.is_island
        for y in range(-4, 4, 1):
            delta_position = Position(0, y)
            new_position = position.add_position(delta_position)
            cell_new_position = self.get_cell(new_position)
            if cell_new_position:
                cell_new_position.can_be_enemy_start = not cell_new_position.is_island

    def update_possible_position_after_silence(self):
        self.set_could_be_start_false()
        cells = self.get_all_cells()
        for cell in cells:
            if cell.can_be_enemy_position:
                self.update_possible_start_position_after_silence_from_current_position(
                    cell.position
                )

    def set_could_be_start_false(self):
        cells = self.get_all_cells()
        for cell in cells:
            cell.can_be_enemy_start = False

    def set_is_in_move_range_false(self):
        cells = self.get_all_cells()
        for cell in cells:
            cell.is_in_move_range = False

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
