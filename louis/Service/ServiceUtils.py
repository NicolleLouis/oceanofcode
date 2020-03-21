import sys

from louis.GameClass import Board, Ship, EnemyShip


class ServiceUtils:
    @staticmethod
    def print_log(log):
        print(log, file=sys.stderr)

    @staticmethod
    def read_turn_data():
        x, y, my_life, opp_life, torpedo_cooldown, \
        sonar_cooldown, silence_cooldown, \
        mine_cooldown = [int(i) for i in input().split()]
        sonar_result = input()
        opponent_orders = input()
        return {
            "x": x,
            "y": y,
            "my_life": my_life,
            "opp_life": opp_life,
            "torpedo_cooldown": torpedo_cooldown,
            "sonar_cooldown": sonar_cooldown,
            "silence_cooldown": silence_cooldown,
            "sonar_result": sonar_result,
            "opponent_orders": opponent_orders,
        }

    @staticmethod
    def read_global_data():
        width, height, my_id = [int(i) for i in input().split()]
        lines = []
        for i in range(height):
            lines.append(input())
        return {
            "width": width,
            "height": height,
            "lines": lines
        }

    @classmethod
    def init(cls):
        global_data = cls.read_global_data()
        board = Board(
            height=global_data["height"],
            width=global_data["width"],
            lines=global_data["lines"]
        )
        ennemy_ship = EnemyShip(
            height=global_data["height"],
            width=global_data["width"],
            lines=global_data["lines"]
        )

        my_ship = Ship()
        my_ship.choose_starting_cell(
            board=board
        )
        return global_data, board, ennemy_ship, my_ship
