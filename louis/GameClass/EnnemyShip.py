from louis.GameClass import Position, Board
from louis.Service import ServiceOrder, ServiceUtils


class EnemyShip(object):
    def __init__(self, height, width, lines):
        self.delta_position = Position(0, 0)
        self.life = 6
        self.enemy_board = Board(
            height=height,
            width=width,
            lines=lines
        )
        self.number_of_possible_positions = height*width

    def update_with_turn_data(self, context_data):
        self.life = context_data.current_turn_opp_life

    def update_number_of_possible_positions(self):
        self.number_of_possible_positions = self.enemy_board.compute_number_of_potential_positions()

    def read_opponent_order(self, opponent_order):
        if opponent_order == "NA":
            return
        list_opponent_order = opponent_order.split("|")
        move_order = ServiceOrder.get_move_order(list_opponent_order)
        if move_order:
            self.delta_position = self.delta_position.add_direction(
                ServiceOrder.get_direction_from_order(move_order)
            )
        self.enemy_board.update_enemy_start_position(self.delta_position)
        self.enemy_board.update_enemy_current_position(self.delta_position)
        self.update_number_of_possible_positions()
