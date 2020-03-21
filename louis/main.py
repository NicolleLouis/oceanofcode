from louis.GameClass import Position
from louis.Service import ServiceUtils, ServiceMovement, ServiceOrder


def surface(board):
    for x in range(board.width):
        for y in range(board.height):
            board.get_cell(Position(x=x, y=y)).reset_visit()
    return "SURFACE"


#################
#################
##### Main ######
#################
#################
global_data, board, ennemy_ship, my_ship = ServiceUtils.init()

# game loop
while True:
    turn_data = ServiceUtils.read_turn_data()
    ennemy_ship.read_opponent_order(turn_data["opponent_orders"])
    move_order = ServiceMovement.chose_movement_and_move(my_ship, board)
    message_order = ServiceOrder.create_msg_order("Test")
    if not move_order:
        move_order = surface(board)
    orders = ServiceOrder.concatenate_order([move_order, message_order])
    ServiceOrder.display_order(orders)
