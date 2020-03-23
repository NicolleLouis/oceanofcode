from louis.Service import ServiceUtils


class Position(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def get_sector(self):
        first_tier = range(0, 5, 1)
        second_tier = range(5, 10, 1)
        if self.y in first_tier:
            if self.x in first_tier:
                return 1
            elif self.x in second_tier:
                return 2
            else:
                return 3
        elif self.y in second_tier:
            if self.x in first_tier:
                return 4
            elif self.x in second_tier:
                return 5
            else:
                return 6
        else:
            if self.x in first_tier:
                return 7
            elif self.x in second_tier:
                return 8
            else:
                return 9

    def invert_position(self):
        return Position(
            x=self.x * -1,
            y=self.y * -1
        )

    def get_distance(self, position):
        return abs(self.x - position.x) + abs(self.y - position.y)

    def add_direction(self, direction):
        if direction == "N":
            return Position(self.x, self.y - 1)

        if direction == "W":
            return Position(self.x - 1, self.y)

        if direction == "S":
            return Position(self.x, self.y + 1)

        if direction == "E":
            return Position(self.x + 1, self.y)

    def add_position(self, position):
        return Position(
            x=int(self.x) + int(position.x),
            y=int(self.y) + int(position.y)
        )

    def __str__(self):
        return "x: {} / y: {}".format(self.x, self.y)
