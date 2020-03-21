from louis.GameClass import Position
from louis.Service import ServiceUtils, ServiceMovement


def surface(board):
    for x in range(board.width):
        for y in range(board.height):
            board.get_cell(Position(x=x, y=y)).reset_visit()
    print("SURFACE")


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
    if not move_order:
        surface(board)
    else:
        print(move_order)
