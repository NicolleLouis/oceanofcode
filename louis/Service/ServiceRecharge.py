class ServiceRecharge:
    TORPEDO = "TORPEDO"
    SILENCE = "SILENCE"
    SONAR = "SONAR"

    @staticmethod
    def chose_recharge(context_data):
        # Decision order: TORPEDO > SILENCE > SONAR
        if (context_data.current_turn_torpedo_cooldown is None or
                context_data.current_turn_torpedo_cooldown > 0):
            return ServiceRecharge.TORPEDO
        if context_data.current_turn_silence_cooldown > 0:
            return ServiceRecharge.SILENCE
        return ServiceRecharge.SONAR
