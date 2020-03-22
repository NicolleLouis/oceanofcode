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
