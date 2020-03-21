from louis.GameClass import Position, Board
from louis.Service import ServiceOrder, ServiceUtils


class EnemyShip(object):
    def __init__(self, height, width, lines):
        self.delta_position = Position(0, 0)
        self.enemy_board = Board(
            height=height,
            width=width,
            lines=lines
        )

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
