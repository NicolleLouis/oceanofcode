class ServiceOrder:
    @staticmethod
    def get_move_order(list_orders):
        for order in list_orders:
            if order.find("MOVE") > -1:
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
    def create_move_order(direction):
        return "MOVE {} TORPEDO".format(direction)

    @staticmethod
    def create_msg_order(msg):
        return "MSG {}".format(msg)

    @classmethod
    def create_number_of_possible_position_order(cls, enemy_ship):
        return cls.create_msg_order(
            enemy_ship.number_of_possible_positions
        )
