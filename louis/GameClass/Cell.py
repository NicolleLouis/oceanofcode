class Cell(object):
    def __init__(self, position, is_island):
        self.position = position
        self.is_island = is_island
        self.is_visited = False
        self.can_be_ennemy_start = not is_island

    def has_been_visited(self):
        self.is_visited = True

    def is_valid_for_move(self):
        return not (self.is_island or self.is_visited)

    def __str__(self):
        return "x" if self.is_island else "."

    def reset_visit(self):
        self.is_visited = False
