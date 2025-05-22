from sys import stderr
from collections import defaultdict

from base import Global, NodeType, get_opposite, is_team_sector

import unicodedata

def show_energy_field(space, only_visible=True):
    line = " + " + " ".join([f"{x:>2}" for x in range(Global.SPACE_SIZE)]) + "  +\n"
    str_grid = line
    for y in range(Global.SPACE_SIZE):

        str_row = []

        for x in range(Global.SPACE_SIZE):
            node = space.get_node(x, y)
            if node.energy is None or (only_visible and not node.is_visible):
                str_row.append(" ..")
            else:
                str_row.append(f"{node.energy:>3}")

        str_grid += "".join([f"{y:>2}", *str_row, f" {y:>2}", "\n"])

    str_grid += line
    print(str_grid, file=stderr)

    with open("stderror.txt", "a", encoding="UTF-8") as logfile:
        print("##############energy field#################", file=logfile)
        print(str_grid, file=logfile)

def show_map(space, fleet=None, opp_fleet=None, only_visible=True):
    """
    legend:
        n - nebula
        a - asteroid
        ~ - relic
        _ - reward
        1:H - ships
    """
    ship_signs = (
        [" "] + [str(x) for x in range(1, 10)] + ["A", "B", "C", "D", "E", "F", "H"]
    )
    opp_ship_signs = (
        [" "] + ["1\u0304", "2\u0304", "3\u0304", "4\u0304", "5\u0304", "6\u0304", "7\u0304", "8\u0304", "9\u0304", "A\u0304", "B\u0304", "C\u0304", "D\u0304", "E\u0304", "F\u0304", "G\u0304", "H\u0304"]
    )

    ships = defaultdict(int)
    if fleet:
        for ship in fleet:
            ships[ship.node.coordinates] += 1
    opp_ships = defaultdict(int)
    if opp_fleet:
        for opp_ship in opp_fleet:
            opp_ships[opp_ship.node.coordinates] += 1


    line = " + " + " ".join([f"{x:>2}" for x in range(Global.SPACE_SIZE)]) + "  +\n"
    str_grid = line
    for y in range(Global.SPACE_SIZE):

        str_row = []

        for x in range(Global.SPACE_SIZE):
            node = space.get_node(x, y)

            if node.type == NodeType.unknown or (only_visible and not node.is_visible):
                str_row.append("..")
                continue

            if node.type == NodeType.nebula:
                s1 = "ñ" if node.relic else "n"
            elif node.type == NodeType.asteroid:
                s1 = "ã" if node.relic else "a"
            else:
                s1 = "~" if node.relic else " "

            if node.reward:
                if s1 == " ":
                    s1 = "_"
            if node.reward and node.relic:
                s1 = "≃"
            if node.coordinates in ships:
                num_ships = ships[node.coordinates]
                s2 = str(ship_signs[num_ships])
            elif node.coordinates in opp_ships:
                num_opp_ships = opp_ships[node.coordinates]
                s2 = str(opp_ship_signs[num_opp_ships])
            else:
                s2 = " "

            str_row.append(s1 + s2)

        str_grid += " ".join([f"{y:>2}", *str_row, f"{y:>2}", "\n"])

    str_grid += line
    print(str_grid, file=stderr)


    with open("stderror.txt", "a", encoding="UTF-8") as logfile:
        print(str_grid, file=logfile)


def show_exploration_map(space):
    """
    legend:
        R - relic
        P - reward
    """
    print(
        f"all relics found: {Global.ALL_RELICS_FOUND}, "
        f"all rewards found: {Global.ALL_REWARDS_FOUND}",
        file=stderr,
    )

    line = " + " + " ".join([f"{x:>2}" for x in range(Global.SPACE_SIZE)]) + "  +\n"
    str_grid = line
    for y in range(Global.SPACE_SIZE):

        str_row = []

        for x in range(Global.SPACE_SIZE):
            node = space.get_node(x, y)
            if not node.explored_for_relic:
                s1 = "."
            else:
                s1 = "R" if node.relic else " "

            if not node.explored_for_reward:
                s2 = "."
            else:
                s2 = "P" if node.reward else " "

            str_row.append(s1 + s2)

        str_grid += " ".join([f"{y:>2}", *str_row, f"{y:>2}", "\n"])

    str_grid += line
    print(str_grid, file=stderr)


def get_relicnodes(team_id, space):
    my_relicnodes = []
    opp_relicnodes = []

    for y in range(Global.SPACE_SIZE):
        for x in range(Global.SPACE_SIZE):
            node = space.get_node(x, y)
            if node.relic:
                if is_team_sector(team_id, x, y):
                    my_relicnodes.append([x, y])
                else:
                    opp_relicnodes.append([x, y])
    
    return my_relicnodes, opp_relicnodes
    
def get_rewardnodes(team_id, space):
    my_rewards = []
    opp_rewards = []

    for y in range(Global.SPACE_SIZE):
        for x in range(Global.SPACE_SIZE):
            node = space.get_node(x, y)
            if node.reward:
                if is_team_sector(team_id, x, y):
                    my_rewards.append([x, y])
                else:
                    opp_rewards.append([x, y])
    
    return my_rewards, opp_rewards

