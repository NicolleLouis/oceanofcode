class OpponentOrder:
    @staticmethod
    def get_move_order(list_orders):
        for order in list_orders:
            if order.find("MOVE") > -1:
                return order
        return False

    @staticmethod
    def get_direction_from_order(move_order):
        return move_order.replace("MOVE ", "")
