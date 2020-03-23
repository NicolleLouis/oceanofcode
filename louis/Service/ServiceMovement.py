import random

from louis.constants import DIRECTIONS, MOVE, SILENCE
from louis.Service import ServiceOrder


class ServiceMovement:
    @staticmethod
    def chose_locomotion(context_data):
        return MOVE if context_data.current_turn_silence_cooldown > 0 else SILENCE

    @staticmethod
    def is_move_possible_in_direction(ship, direction, board):
        next_position = ship.get_position_after_move(direction)
        return board.is_position_valid_for_move(next_position)

    @staticmethod
    def random_direction():
        return random.choice(DIRECTIONS)

    @staticmethod
    def should_surface(ship, board):
        return board.is_position_dead_end(ship.position)

    @classmethod
    def chose_direction(cls, ship, board):
        direction = cls.random_direction()
        while not cls.is_move_possible_in_direction(ship, direction, board):
            direction = cls.random_direction()
        return direction

    @staticmethod
    def surface(board):
        board.reset_is_visited()
        return "SURFACE"
