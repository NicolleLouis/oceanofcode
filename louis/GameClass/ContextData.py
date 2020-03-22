class ContextData(object):
    def __init__(self):
        self.current_turn_x = None
        self.current_turn_y = None
        self.current_turn_my_life = None
        self.current_turn_opp_life = None
        self.current_turn_torpedo_cooldown = None
        self.current_turn_sonar_cooldown = None
        self.current_turn_silence_cooldown = None
        self.current_turn_sonar_result = None
        self.current_turn_opponent_orders = None

    def update_turn_data(self, turn_data):
        self.current_turn_x = turn_data["x"]
        self.current_turn_y = turn_data["y"]
        self.current_turn_my_life = turn_data["my_life"]
        self.current_turn_opp_life = turn_data["opp_life"]
        self.current_turn_torpedo_cooldown = turn_data["torpedo_cooldown"]
        self.current_turn_sonar_cooldown = turn_data["sonar_cooldown"]
        self.current_turn_silence_cooldown = turn_data["silence_cooldown"]
        self.current_turn_sonar_result = turn_data["sonar_result"]
        self.current_turn_opponent_orders = turn_data["opponent_orders"]
