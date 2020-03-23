from GameClass import Position
from Service import ServiceUtils
from louis.Service import ServiceOrder


class ContextData(object):
    def __init__(self):
        # Current turn game input
        self.current_turn_x = None
        self.current_turn_y = None
        self.current_turn_my_life = None
        self.current_turn_opp_life = None
        self.current_turn_torpedo_cooldown = None
        self.current_turn_sonar_cooldown = None
        self.current_turn_silence_cooldown = None
        self.current_turn_sonar_result = None
        self.current_turn_opponent_orders = None

        # Last turn game input
        self.last_turn_turn_x = None
        self.last_turn_turn_y = None
        self.last_turn_turn_my_life = None
        self.last_turn_turn_opp_life = None
        self.last_turn_turn_torpedo_cooldown = None
        self.last_turn_turn_sonar_cooldown = None
        self.last_turn_turn_silence_cooldown = None
        self.last_turn_turn_sonar_result = None
        self.last_turn_turn_opponent_orders = None

        # Last turn game output
        self.last_turn_own_orders = None

        # computed field
        self.enemy_was_damaged = None

    def update_turn_data(self, turn_data, enemy_ship, board):
        self.current_turn_x = turn_data["x"]
        self.current_turn_y = turn_data["y"]
        self.current_turn_my_life = turn_data["my_life"]
        self.current_turn_opp_life = turn_data["opp_life"]
        self.current_turn_torpedo_cooldown = turn_data["torpedo_cooldown"]
        self.current_turn_sonar_cooldown = turn_data["sonar_cooldown"]
        self.current_turn_silence_cooldown = turn_data["silence_cooldown"]
        self.current_turn_sonar_result = turn_data["sonar_result"]
        self.current_turn_opponent_orders = turn_data["opponent_orders"]

        board.get_cell(
            Position(
                x=turn_data["x"],
                y=turn_data["y"]
            )
        ).is_visited = True
        self.analyse_turn_data(enemy_ship)

    def update_end_of_turn_data(self, orders):
        self.last_turn_turn_x = self.current_turn_x
        self.last_turn_turn_y = self.current_turn_y
        self.last_turn_turn_my_life = self.current_turn_my_life
        self.last_turn_turn_opp_life = self.current_turn_opp_life
        self.last_turn_turn_torpedo_cooldown = self.current_turn_torpedo_cooldown
        self.last_turn_turn_sonar_cooldown = self.current_turn_sonar_cooldown
        self.last_turn_turn_silence_cooldown = self.current_turn_silence_cooldown
        self.last_turn_turn_sonar_result = self.current_turn_sonar_result
        self.last_turn_turn_opponent_orders = self.current_turn_opponent_orders

        self.last_turn_own_orders = orders

    def analyse_turn_data(self, enemy_ship):
        self.compute_custom_fields()
        self.analyse_custom_fields(enemy_ship)

    def compute_enemy_was_damaged(self):
        if self.current_turn_opp_life is not None and self.last_turn_turn_opp_life is not None:
            self.enemy_was_damaged = not (
                    self.current_turn_opp_life == self.last_turn_turn_opp_life
            )
        else:
            self.enemy_was_damaged = None

    def analyse_enemy_damage(self, enemy_ship):
        # TODO: Case damage taken -> guess if it's for own torpedo or not
        if self.enemy_was_damaged:
            return
        # Case first turn
        if self.last_turn_own_orders is None:
            return
            # case damage taken but not because of our own torpedo (Surface or enemy torpedo)
        if not ServiceOrder.get_attack_order(self.last_turn_own_orders):
            return
        attack_order = ServiceOrder.get_attack_order(self.last_turn_own_orders)
        position_torpedo = ServiceOrder.get_position_from_attack_order(attack_order)
        enemy_ship.enemy_board.update_board_torpedo_did_not_hit_in_position(
            position_torpedo,
            enemy_ship.delta_position
        )

    def compute_custom_fields(self):
        self.compute_enemy_was_damaged()

    def analyse_custom_fields(self, enemy_ship):
        self.analyse_enemy_damage(enemy_ship)

    @staticmethod
    def analyse_opponent_move_order(enemy_ship, move_order):
        enemy_ship.delta_position = enemy_ship.delta_position.add_direction(
            ServiceOrder.get_direction_from_order(move_order)
        )
        enemy_ship.update_potential_position_from_geography()

    @staticmethod
    def extract_sector_from_opponent_surface_order(surface_order):
        return int(surface_order.replace("SURFACE ", ""))

    @staticmethod
    def analyse_opponent_attack_order(enemy_ship, attack_order):
        initial_count = enemy_ship.enemy_board.compute_number_of_potential_positions()

        attack_position = ServiceOrder.extract_position_from_attack_order(attack_order)
        enemy_ship.enemy_board.enemy_is_in_range(
            range_attack=4,
            attack_position=attack_position
        )
        enemy_ship.enemy_board.update_enemy_potential_start_position(enemy_ship.delta_position)

        final_count = enemy_ship.enemy_board.compute_number_of_potential_positions()
        ServiceUtils.print_log("From: {} to: {}".format(initial_count, final_count))

    @staticmethod
    def analyse_opponent_surface_order(enemy_ship, surface_order):
        sector = ContextData.extract_sector_from_opponent_surface_order(surface_order)
        enemy_ship.enemy_board.enemy_not_in_sector(sector)
        enemy_ship.enemy_board.update_enemy_potential_start_position(enemy_ship.delta_position)

    @staticmethod
    def analyse_opponent_silence_order(enemy_ship):
        enemy_ship.reset_delta_position()
        enemy_ship.enemy_board.update_possible_position_after_silence()
        enemy_ship.enemy_board.update_enemy_current_position(enemy_ship.delta_position)

    def read_opponent_order(self, enemy_ship):
        if self.current_turn_opponent_orders == "NA":
            return
        list_orders = ServiceOrder.split_orders(self.current_turn_opponent_orders)
        for order in list_orders:
            silence_order = ServiceOrder.get_silence_order(order)
            if silence_order:
                self.analyse_opponent_silence_order(enemy_ship)
            move_order = ServiceOrder.get_move_order(order)
            if move_order:
                self.analyse_opponent_move_order(enemy_ship, move_order)
            surface_order = ServiceOrder.get_surface_order(order)
            if surface_order:
                self.analyse_opponent_surface_order(enemy_ship, surface_order)
            attack_order = ServiceOrder.get_attack_order(order)
            if attack_order:
                self.analyse_opponent_attack_order(enemy_ship, attack_order)

