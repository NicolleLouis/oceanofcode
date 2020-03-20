import sys
import math


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


def choose_starting_cell(lines):
    number_of_free_cell = 0
    for line in lines:
        number_of_free_cell += line.count('.')
    print_log(number_of_free_cell)


global_data = read_global_data()

choose_starting_cell(global_data["lines"])

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print_log("####### map #########")
for line in global_data["lines"]:
    print_log(line)

# game loop
while True:
    turn_data = read_turn_data()

    print("MOVE N TORPEDO")
