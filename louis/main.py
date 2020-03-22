from louis.GameClass import Position, ContextData
from louis.Service import ServiceUtils, ServiceMovement, ServiceOrder, ServiceTorpedo

# Init
global_data, board, enemy_ship, my_ship = ServiceUtils.init()

context_data = ContextData()

# game loop
while True:
    # read turn data and analysis
    turn_data = ServiceUtils.read_turn_data()
    context_data.update_turn_data(turn_data, enemy_ship)
    my_ship.update_with_turn_data(context_data)
    enemy_ship.update_with_turn_data(context_data)

    # Read and analyse opponent order
    enemy_ship.read_opponent_order(context_data.current_turn_opponent_orders)

    move_order = ServiceMovement.chose_movement_and_move(my_ship, board)
    attack_order = ServiceTorpedo.chose_torpedo(my_ship, enemy_ship)
    message_order = ServiceOrder.create_number_of_possible_position_order(enemy_ship)
    if not move_order:
        move_order = ServiceMovement.surface(board)
    orders = ServiceOrder.concatenate_order([move_order, attack_order, message_order])
    ServiceOrder.display_order(orders)

    context_data.update_end_of_turn_data(orders)
