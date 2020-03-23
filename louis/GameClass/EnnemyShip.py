from louis.GameClass import Position, Board
from louis.Service import ServiceOrder, ServiceUtils


class EnemyShip(object):
    def __init__(self, height, width, lines):
        self.delta_position = Position(0, 0)
        self.last_turn_delta_position = Position(0, 0)
        self.life = 6
        self.enemy_board = Board(
            height=height,
            width=width,
            lines=lines
        )
        self.number_of_possible_positions = height*width

    def enemy_was_in_range(self, range_detection, detection_position):
        enemy_board = self.enemy_board
        for x in range(enemy_board.width):
            for y in range(enemy_board.height):
                starting_cell = enemy_board.get_cell(Position(x, y))
                last_turn_position_from_starting_position = Position(x, y).add_position(self.last_turn_delta_position)
                last_turn_position = enemy_board.get_cell(last_turn_position_from_starting_position)
                # Case last_turn_position not on board
                if not bool(last_turn_position):
                    starting_cell.cannot_be_enemy_start()
                # Case last_turn_position_hors de_range
                elif last_turn_position.position.get_distance(detection_position) > range_detection:
                    starting_cell.cannot_be_enemy_start()
        enemy_board.update_enemy_current_position(self.delta_position)

    def reset_delta_position(self):
        self.delta_position = Position(0, 0)

    def update_with_turn_data(self, context_data):
        self.life = context_data.current_turn_opp_life

    def update_number_of_possible_positions(self):
        self.number_of_possible_positions = self.enemy_board.compute_number_of_potential_positions()

    def update_potential_position_from_geography(self):
        self.enemy_board.update_enemy_potential_start_position_from_geography(self.delta_position)
        self.enemy_board.update_enemy_current_position(self.delta_position)
        self.update_number_of_possible_positions()
