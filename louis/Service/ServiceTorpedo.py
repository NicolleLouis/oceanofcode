class ServiceTorpedo:
    @staticmethod
    def chose_torpedo(ship):
        if ship.torpedo_cooldown == 0:
            return "TORPEDO 0 0"
