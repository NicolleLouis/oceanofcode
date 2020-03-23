import sys
import random

DIRECTIONS = ["N", "W", "E", "S"]
MOVE = "MOVE"
SILENCE = "SILENCE"


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


class Ship(object):
    def __init__(self):
        self.position = Position(0, 0)
        self.direction = "N"
        self.torpedo_cooldown = 3
        self.life = 6

    def update_with_turn_data(self, context_data):
        self.position = Position(
            x=context_data.current_turn_x,
            y=context_data.current_turn_y
        )
        self.torpedo_cooldown = context_data.current_turn_torpedo_cooldown
        self.life = context_data.current_turn_my_life

    def get_position_after_move(self, direction):
        return self.position.add_direction(direction)

    def choose_starting_cell(self, board):
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        random_position = Position(x, y)
        while not board.is_position_valid_for_move(random_position):
            random_position.x = random.randint(0, board.width - 1)
            random_position.y = random.randint(0, board.height - 1)
        self.position = random_position
        print("{} {}".format(self.position.x, self.position.y))

    def __str__(self):
        return str(self.position)


class Cell(object):
    def __init__(self, position, is_island):
        self.position = position
        self.is_island = is_island
        self.is_visited = False
        self.can_be_enemy_start = not is_island
        self.can_be_enemy_position = not is_island
        self.sector = self.position.get_sector()

    def has_been_visited(self):
        self.is_visited = True

    def is_valid_for_move(self):
        return not (self.is_island or self.is_visited)

    def cannot_be_enemy_start(self):
        self.can_be_enemy_start = False

    def set_can_be_enemy_position(self, can_be_enemy_position):
        self.can_be_enemy_position = can_be_enemy_position

    def __str__(self):
        return "x" if self.is_island else "."

    def print_can_be_here(self):
        return "x" if not self.can_be_enemy_position else "."

    def reset_visit(self):
        self.is_visited = False


class Board(object):
    def __init__(self, height, width, lines):
        self.height = height
        self.width = width
        self.map = []
        for y, line in enumerate(lines):
            cell_line = []
            for x, char in enumerate(line):
                cell_line.append(Cell(Position(x, y), char == "x"))
            self.map.append(cell_line)

    def is_position_in_grid(self, position):
        if position.x < 0 or position.x >= self.width:
            return False
        if position.y < 0 or position.y >= self.height:
            return False
        return True

    def is_position_valid_for_move(self, position):
        if not self.is_position_in_grid(position):
            return False
        return self.get_cell(position).is_valid_for_move()

    def is_position_valid_for_enemy(self, position):
        if not self.is_position_in_grid(position):
            return False
        return not self.get_cell(position).is_island

    def get_cell(self, position):
        try:
            return self.map[position.y][position.x]
        except IndexError:
            return False

    def enemy_not_in_sector(self, sector):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(Position(x, y))
                if cell.sector != sector:
                    cell.can_be_enemy_position = False

    def is_position_dead_end(self, position):
        available_direction = 0
        for direction in DIRECTIONS:
            new_position = position.add_direction(direction)
            if self.is_position_valid_for_move(new_position):
                available_direction += 1
        return available_direction == 0

    def update_enemy_potential_start_position_from_geography(self, delta_position):
        for x in range(self.width):
            for y in range(self.height):
                start_position = Position(x, y)
                current_position = start_position.add_position(delta_position)
                if not self.is_position_valid_for_enemy(current_position):
                    self.get_cell(start_position).cannot_be_enemy_start()

    def update_enemy_potential_start_position(self, delta_position):
        for x in range(self.width):
            for y in range(self.height):
                start_position = Position(x, y)
                current_position = start_position.add_position(delta_position)
                cell = self.get_cell(current_position)
                if cell:
                    if not self.get_cell(current_position).can_be_enemy_position:
                        self.get_cell(start_position).cannot_be_enemy_start()

    def enemy_is_in_range(self, range_attack, attack_position):
        self.print_potential_position_board()
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(Position(x, y))
                if cell.position.get_distance(attack_position) > range_attack:
                    cell.can_be_enemy_position = False
        self.print_potential_position_board()

    def compute_number_of_potential_positions(self):
        number_of_positions = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.get_cell(Position(x, y)).can_be_enemy_position:
                    number_of_positions += 1
        return number_of_positions

    def update_enemy_current_position(self, delta_position):
        for x in range(self.width):
            for y in range(self.height):
                current_position = Position(x, y)
                start_position = current_position.add_position(
                    delta_position.invert_position()
                )
                if not self.get_cell(start_position):
                    self.get_cell(current_position).can_be_enemy_position = False
                else:
                    can_be_position = self.get_cell(start_position).can_be_enemy_start
                    self.get_cell(current_position).can_be_enemy_position = can_be_position

    def reset_is_visited(self):
        for x in range(self.width):
            for y in range(self.height):
                self.get_cell(Position(x=x, y=y)).reset_visit()

    def reset_could_be_start(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(Position(x=x, y=y))
                cell.can_be_enemy_start = not cell.is_island

    def update_possible_start_position_after_silence_from_current_position(self, position):
        for x in range(-4, 4, 1):
            delta_position = Position(x, 0)
            new_position = position.add_position(delta_position)
            cell_new_position = self.get_cell(new_position)
            if cell_new_position:
                cell_new_position.can_be_enemy_start = not cell_new_position.is_island
        for y in range(-4, 4, 1):
            delta_position = Position(0, y)
            new_position = position.add_position(delta_position)
            cell_new_position = self.get_cell(new_position)
            if cell_new_position:
                cell_new_position.can_be_enemy_start = not cell_new_position.is_island

    def update_possible_position_after_silence(self):
        self.set_could_be_start_false()
        for x in range(self.width):
            for y in range(self.height):
                cell_position = Position(x=x, y=y)
                cell = self.get_cell(cell_position)
                if cell.can_be_enemy_position:
                    self.update_possible_start_position_after_silence_from_current_position(cell_position)

    def set_could_be_start_false(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(Position(x=x, y=y))
                cell.can_be_enemy_start = False

    def update_board_torpedo_did_not_hit_in_position(self, torpedo_position, delta_position):
        torpedo_delta_range = [-1, 0, 1]
        for x in torpedo_delta_range:
            for y in torpedo_delta_range:
                torpedo_delta_position = Position(x, y)
                current_position_without_enemy_boat = torpedo_position.add_position(torpedo_delta_position)
                start_position_without_enemy_boat = current_position_without_enemy_boat.add_position(
                    delta_position.invert_position()
                )
                start_cell = self.get_cell(start_position_without_enemy_boat)
                if start_cell:
                    start_cell.cannot_be_enemy_start()
        self.update_enemy_current_position(delta_position)

    def print_potential_position_board(self):
        for line in self.map:
            line_string = ""
            for cell in line:
                line_string += cell.print_can_be_here()
            ServiceUtils.print_log(line_string)


class EnemyShip(object):
    def __init__(self, height, width, lines):
        self.delta_position = Position(0, 0)
        self.life = 6
        self.enemy_board = Board(
            height=height,
            width=width,
            lines=lines
        )
        self.number_of_possible_positions = height * width

    def reset_delta_position(self):
        self.delta_position = Position(0, 0)

    def update_with_turn_data(self, context_data):
        self.life = context_data.current_turn_opp_life

    def update_number_of_possible_positions(self):
        self.number_of_possible_positions = self.enemy_board.compute_number_of_potential_positions()


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

    @staticmethod
    def update_current_position(enemy_ship):
        enemy_ship.enemy_board.update_enemy_potential_start_position_from_geography(enemy_ship.delta_position)
        enemy_ship.enemy_board.update_enemy_current_position(enemy_ship.delta_position)
        enemy_ship.update_number_of_possible_positions()

    def read_opponent_order(self, enemy_ship):
        if self.current_turn_opponent_orders == "NA":
            return
        silence_order = ServiceOrder.get_silence_order(self.current_turn_opponent_orders)
        if silence_order:
            self.analyse_opponent_silence_order(enemy_ship)
        move_order = ServiceOrder.get_move_order(self.current_turn_opponent_orders)
        if move_order:
            self.analyse_opponent_move_order(enemy_ship, move_order)
        surface_order = ServiceOrder.get_surface_order(self.current_turn_opponent_orders)
        if surface_order:
            self.analyse_opponent_surface_order(enemy_ship, surface_order)
        attack_order = ServiceOrder.get_attack_order(self.current_turn_opponent_orders)
        if attack_order:
            self.analyse_opponent_attack_order(enemy_ship, attack_order)
        self.update_current_position(enemy_ship)


class ServiceUtils:
    @staticmethod
    def print_log(log):
        print(log, file=sys.stderr)

    @staticmethod
    def read_turn_data():
        x, y, my_life, opp_life, torpedo_cooldown, \
        sonar_cooldown, silence_cooldown, \
        mine_cooldown = [int(i) for i in input().split()]
        sonar_result = input()
        opponent_orders = input()
        return {
            "x": x,
            "y": y,
            "my_life": my_life,
            "opp_life": opp_life,
            "torpedo_cooldown": torpedo_cooldown,
            "sonar_cooldown": sonar_cooldown,
            "silence_cooldown": silence_cooldown,
            "sonar_result": sonar_result,
            "opponent_orders": opponent_orders,
        }

    @staticmethod
    def read_global_data():
        width, height, my_id = [int(i) for i in input().split()]
        lines = []
        for i in range(height):
            lines.append(input())
        return {
            "width": width,
            "height": height,
            "lines": lines
        }

    @classmethod
    def init(cls):
        global_data = cls.read_global_data()
        board = Board(
            height=global_data["height"],
            width=global_data["width"],
            lines=global_data["lines"]
        )
        ennemy_ship = EnemyShip(
            height=global_data["height"],
            width=global_data["width"],
            lines=global_data["lines"]
        )

        my_ship = Ship()
        my_ship.choose_starting_cell(
            board=board
        )
        return global_data, board, ennemy_ship, my_ship


class ServiceMovement:
    @staticmethod
    def chose_locomotion(context_data):
        return MOVE if context_data.current_turn_silence_cooldown > 0 else SILENCE

    @staticmethod
    def is_move_possible_in_direction(ship, direction, board):
        next_position = ship.get_position_after_move(direction)
        return board.is_position_valid_for_move(next_position)

    @staticmethod
    def move_my_ship(ship, direction, board):
        board.get_cell(position=ship.position).has_been_visited()
        ship.direction = direction
        move_order = ServiceOrder.create_direction_order(direction)
        return move_order

    @staticmethod
    def random_direction():
        return random.choice(DIRECTIONS)

    @staticmethod
    def should_surface(ship, board):
        return board.is_position_dead_end(ship.position)

    @classmethod
    def chose_direction(cls, ship, board):
        direction = cls.random_direction()
        while not cls.is_move_possible_in_direction(ship, direction, board):
            direction = cls.random_direction()
        return direction

    @staticmethod
    def surface(board):
        board.reset_is_visited()
        return "SURFACE"


class ServiceOrder:
    @staticmethod
    def extract_position_from_attack_order(attack_order):
        string_position = attack_order.replace("TORPEDO ", "")
        list_coordinates = string_position.split(" ")
        return Position(list_coordinates[0], list_coordinates[1])

    @staticmethod
    def concatenate_move_and_recharge_order(move_order, recharge_order):
        if move_order.find("SILENCE") > -1:
            return move_order
        return "{} {}".format(move_order, recharge_order)

    @staticmethod
    def split_orders(orders):
        return orders.split("|")

    @staticmethod
    def get_attack_order(orders):
        list_orders = ServiceOrder.split_orders(orders)
        for order in list_orders:
            if order.find("TORPEDO") > -1 and order.find("MOVE") == -1:
                return order
        return False

    @staticmethod
    def get_position_from_attack_order(attack_order):
        coordinates = attack_order.replace("TORPEDO ", "")
        list_coordinate = coordinates.split(" ")
        return Position(list_coordinate[0], list_coordinate[1])

    @staticmethod
    def get_move_order(orders):
        list_orders = ServiceOrder.split_orders(orders)
        for order in list_orders:
            if order.find("MOVE") > -1:
                return order
        return False

    @staticmethod
    def get_surface_order(orders):
        list_orders = ServiceOrder.split_orders(orders)
        for order in list_orders:
            if order.find("SURFACE") > -1:
                return order
        return False

    @staticmethod
    def get_silence_order(orders):
        list_orders = ServiceOrder.split_orders(orders)
        for order in list_orders:
            if order.find("SILENCE") > -1:
                return order
        return False

    @staticmethod
    def get_direction_from_order(move_order):
        return move_order.replace("MOVE ", "")

    @staticmethod
    def concatenate_order(list_orders):
        filtered_list = list(filter(lambda order: order, list_orders))
        return "|".join(filtered_list)

    @staticmethod
    def display_order(order):
        print(order)

    @staticmethod
    def create_msg_order(msg):
        return "MSG {}".format(msg)

    @staticmethod
    def create_attack_order(position):
        return "TORPEDO {} {}".format(position.x, position.y)

    @staticmethod
    def create_number_of_possible_position_order(enemy_ship):
        return ServiceOrder.create_msg_order(
            enemy_ship.number_of_possible_positions
        )

    @staticmethod
    def concatenate_direction_and_locomotion(direction_order, locomotion_order):
        if locomotion_order == MOVE:
            return "{} {}".format(locomotion_order, direction_order)
        else:
            return "{} {} 1".format(locomotion_order, direction_order)


class ServiceTorpedo:
    @staticmethod
    def chose_torpedo(ship, enemy_ship):
        if ship.torpedo_cooldown > 0:
            return False
        within_range_positions = ServiceTorpedo.find_within_range_torpedo_positions(
            ship,
            enemy_ship
        )
        possible_attack_position = ServiceTorpedo. find_position_in_range_with_potential_enemy(
            within_range_positions,
            enemy_ship
        )
        if len(possible_attack_position) == 0:
            return False
        safe_attack_position = ServiceTorpedo.find_safest_attack_position(
            ship,
            possible_attack_position
        )
        return ServiceOrder.create_attack_order(safe_attack_position)

    @staticmethod
    def find_safest_attack_position(ship, positions):
        best_position = positions[0]
        best_distance = 0
        for position in positions:
            distance = position.get_distance(ship.position)
            if distance > best_distance:
                best_distance = distance
                best_position = position
        return best_position

    @staticmethod
    def find_within_range_torpedo_positions(ship, enemy_ship):
        possible_positions = []
        for x in range(enemy_ship.enemy_board.width):
            for y in range(enemy_ship.enemy_board.height):
                if ship.position.get_distance(Position(x, y)) <= 4:
                    possible_positions.append(Position(x, y))
        return possible_positions

    @staticmethod
    def find_position_in_range_with_potential_enemy(list_positions, enemy_ship):
        potential_positions = []
        for position in list_positions:
            if enemy_ship.enemy_board.get_cell(position).can_be_enemy_position:
                potential_positions.append(position)
        return potential_positions


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


#################
#################
##### Main ######
#################
#################
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

    context_data.update_end_of_turn_data(orders)
