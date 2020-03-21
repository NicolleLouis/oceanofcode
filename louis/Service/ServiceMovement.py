import random

from louis.constants import directions
from louis.Service import ServiceOrder


class ServiceMovement:
    @staticmethod
    def is_move_possible_in_direction(ship, direction, board):
        next_position = ship.get_position_after_move(direction)
        return board.is_position_valid_for_move(next_position)

    @staticmethod
    def move_my_ship(ship, direction, board):
        board.get_cell(position=ship.position).has_been_visited()
        ship.move(direction)
        move_order = ServiceOrder.create_move_order(direction)
        return move_order

    @staticmethod
    def random_direction():
        return random.choice(directions)

    @classmethod
    def chose_movement_and_move(cls, ship, board):
        if board.is_position_dead_end(ship.position):
            return False
        direction = ship.direction
        while not cls.is_move_possible_in_direction(ship, direction, board):
            direction = cls.random_direction()
        move_order = cls.move_my_ship(ship, direction, board)
        return move_order

    @staticmethod
    def surface(board):
        board.reset_is_visited()
        return "SURFACE"
