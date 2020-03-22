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

    def update_turn_data(self, turn_data, enemy_ship):
        self.current_turn_x = turn_data["x"]
        self.current_turn_y = turn_data["y"]
        self.current_turn_my_life = turn_data["my_life"]
        self.current_turn_opp_life = turn_data["opp_life"]
        self.current_turn_torpedo_cooldown = turn_data["torpedo_cooldown"]
        self.current_turn_sonar_cooldown = turn_data["sonar_cooldown"]
        self.current_turn_silence_cooldown = turn_data["silence_cooldown"]
        self.current_turn_sonar_result = turn_data["sonar_result"]
        self.current_turn_opponent_orders = turn_data["opponent_orders"]

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
