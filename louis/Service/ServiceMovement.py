import random

class ServiceMovement:
    @staticmethod
    def is_move_possible_in_direction(ship, direction, board):
        next_position = ship.get_position_after_move(direction)
        return board.is_position_valid_for_move(next_position)

    @staticmethod
    def move_my_ship(ship, direction, board):
        board.get_cell(position=ship.position).has_been_visited()
        ship.move(direction)
        move_order = "MOVE {} TORPEDO".format(direction)
        return move_order

    @staticmethod
    def random_turn(direction):
        if direction in ["S", "N"]:
            return random.choice(["E", "W"])
        return random.choice(["S", "N"])

    @classmethod
    def chose_movement_and_move(cls, ship, board):
        direction = ship.direction
        while not cls.is_move_possible_in_direction(ship, direction, board):
            if board.is_position_dead_end(ship.position):
                return False
            direction = cls.random_turn(ship.direction)
        move_order = cls.move_my_ship(ship, direction, board)
        return move_order
