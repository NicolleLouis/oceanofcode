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
        ship.direction = direction
        move_order = ServiceOrder.create_move_order(direction)
        return move_order

    @staticmethod
    def random_direction():
        return random.choice(directions)

    @staticmethod
    def should_surface(ship, board):
        return board.is_position_dead_end(ship.position)

    @classmethod
    def chose_movement(cls, ship, board):
        direction = cls.random_direction()
        while not cls.is_move_possible_in_direction(ship, direction, board):
            direction = cls.random_direction()
        move_order = ServiceOrder.create_move_order(direction)
        return move_order

    @staticmethod
    def surface(board):
        board.reset_is_visited()
        return "SURFACE"
