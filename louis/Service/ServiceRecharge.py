class ServiceRecharge:
    TORPEDO = "TORPEDO"
    SILENCE = "SILENCE"
    SONAR = "SONAR"

    @staticmethod
    def chose_recharge(context_data):
        return ServiceRecharge.TORPEDO
