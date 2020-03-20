import sys
import math
import random


class Ship(object):
    def __init__(self):
        self.x = 0
        self.y = 0


def print_log(log):
    print(log, file=sys.stderr)


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


def choose_starting_cell(ship, lines, width, height):
    ship.x = random.randint(0, width - 1)
    ship.y = random.randint(0, height - 1)
    print("{} {}".format(ship.x, ship.y))


# Read global input
global_data = read_global_data()

my_ship = Ship()
choose_starting_cell(
    ship=my_ship,
    lines=global_data["lines"],
    width=global_data["width"],
    height=global_data["height"],
)

print_log("####### map #########")
for line in global_data["lines"]:
    print_log(line)

# game loop
while True:
    turn_data = read_turn_data()

    print("MOVE N TORPEDO")
