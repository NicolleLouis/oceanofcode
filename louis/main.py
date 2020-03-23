from Service import ServiceRecharge
from constants import SILENCE
from louis.GameClass import Position, ContextData
from louis.Service import ServiceUtils, ServiceMovement, ServiceOrder, ServiceTorpedo

# Init
global_data, board, enemy_ship, my_ship = ServiceUtils.init()

context_data = ContextData()

# game loop
while True:
    # read turn data and analysis
    turn_data = ServiceUtils.read_turn_data()
    context_data.update_turn_data(turn_data, enemy_ship, board)
    my_ship.update_with_turn_data(context_data)
    enemy_ship.update_with_turn_data(context_data)

    # Read and analyse opponent order
    context_data.read_opponent_order(enemy_ship)

    should_surface = ServiceMovement.should_surface(my_ship, board)
    if not should_surface:
        direction_order = ServiceMovement.chose_direction(my_ship, board)
        locomotion_order = ServiceMovement.chose_locomotion(context_data)
        move_order = ServiceOrder.concatenate_direction_and_locomotion(direction_order, locomotion_order)
        recharge_order = ServiceRecharge.chose_recharge(context_data)
        move_and_recharge_order = ServiceOrder.concatenate_move_and_recharge_order(
            move_order=move_order,
            recharge_order=recharge_order
        )
    else:
        move_and_recharge_order = ServiceMovement.surface(board)
    attack_order = ServiceTorpedo.chose_torpedo(my_ship, enemy_ship)
    message_order = ServiceOrder.create_number_of_possible_position_order(enemy_ship)
    orders = ServiceOrder.concatenate_order([attack_order, move_and_recharge_order, message_order])
    ServiceOrder.display_order(orders)

    context_data.update_end_of_turn_data(orders, enemy_ship)
