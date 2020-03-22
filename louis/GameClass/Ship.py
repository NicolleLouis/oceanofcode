import random

from louis.GameClass import Position


class Ship(object):
    def __init__(self):
        self.position = Position(0, 0)
        self.direction = "N"
        self.torpedo_cooldown = 3
        self.life = 6

    def update_with_turn_data(self, context_data):
        self.torpedo_cooldown = context_data.current_turn_torpedo_cooldown
        self.life = context_data.current_turn_my_life

    def move(self, direction):
        self.direction = direction
        self.position = self.position.add_direction(direction)

    def get_position_after_move(self, direction):
        return self.position.add_direction(direction)

    def choose_starting_cell(self, board):
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        random_position = Position(x, y)
        while not board.is_position_valid_for_move(random_position):
            random_position.x = random.randint(0, board.width - 1)
            random_position.y = random.randint(0, board.height - 1)
        self.position = random_position
        print("{} {}".format(self.position.x, self.position.y))

    def __str__(self):
        return str(self.position)
