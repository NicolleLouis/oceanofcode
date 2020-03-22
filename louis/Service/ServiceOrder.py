from constants import MOVE
from louis.GameClass import Position


class ServiceOrder:
    @staticmethod
    def concatenate_move_and_recharge_order(move_order, recharge_order):
        if move_order.find("SILENCE") > -1:
            return move_order
        return "{} {}".format(move_order, recharge_order)

    @staticmethod
    def split_orders(orders):
        return orders.split("|")

    @staticmethod
    def get_attack_order(orders):
        list_orders = ServiceOrder.split_orders(orders)
        for order in list_orders:
            if order.find("TORPEDO") > -1 and order.find("MOVE") == -1:
                return order
        return False

    @staticmethod
    def get_position_from_attack_order(attack_order):
        coordinates = attack_order.replace("TORPEDO ", "")
        list_coordinate = coordinates.split(" ")
        return Position(list_coordinate[0], list_coordinate[1])

    @staticmethod
    def get_move_order(orders):
        list_orders = ServiceOrder.split_orders(orders)
        for order in list_orders:
            if order.find("MOVE") > -1:
                return order
        return False

    @staticmethod
    def get_silence_order(orders):
        list_orders = ServiceOrder.split_orders(orders)
        for order in list_orders:
            if order.find("SILENCE") > -1:
                return order
        return False

    @staticmethod
    def get_direction_from_order(move_order):
        return move_order.replace("MOVE ", "")

    @staticmethod
    def concatenate_order(list_orders):
        filtered_list = list(filter(lambda order: order, list_orders))
        return "|".join(filtered_list)

    @staticmethod
    def display_order(order):
        print(order)

    @staticmethod
    def create_msg_order(msg):
        return "MSG {}".format(msg)

    @staticmethod
    def create_attack_order(position):
        return "TORPEDO {} {}".format(position.x, position.y)

    @staticmethod
    def create_number_of_possible_position_order(enemy_ship):
        return ServiceOrder.create_msg_order(
            enemy_ship.number_of_possible_positions
        )

    @staticmethod
    def concatenate_direction_and_locomotion(direction_order, locomotion_order):
        if locomotion_order == MOVE:
            return "{} {}".format(locomotion_order, direction_order)
        else:
            return "{} {} 1".format(locomotion_order, direction_order)
