import random

from Service import ServiceUtils
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
        ponderated_random_decisions = []
        for direction in DIRECTIONS:
            if cls.is_move_possible_in_direction(ship, direction, board):
                number_of_move_possible = board.get_number_of_potential_move_position_from_position(
                    position=ship.get_position_after_move(direction)
                )
                for iteration in range(number_of_move_possible):
                    ponderated_random_decisions.append(direction)
        return random.choice(ponderated_random_decisions)

    @staticmethod
    def surface(board):
        board.reset_is_visited()
        return "SURFACE"
