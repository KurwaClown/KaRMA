from CONST import constants
from random import randint, sample


def apexLoadout():
    loadout = sample(range(1,len(constants.WEAPONS)),2)
    return f"{constants.LEGENDS[randint(1, len(constants.LEGENDS))]} with {constants.WEAPONS[loadout[0]]} and {constants.WEAPONS[loadout[1]]}"


def owChar(arg):
    if arg=="all":
        role = randint(1,3)
        return constants.HEROES[role][randint(1,len(constants.HEROES[role]))]
    elif arg == "tank":
        return constants.HEROES[1][randint(1,8)]
    elif arg == "dps":
        return constants.HEROES[2][randint(1,17)]
    elif arg == "heal":
        return constants.HEROES[3][randint(1,7)]
    elif arg == "role":
        return constants.OWROLE[randint(1,3)]


def r6Char(arg):
    return constants.OPERATORS[arg][randint(1, len(constants.OPERATORS[arg]))]


def lolChar():
    return constants.CHAMPIONS[randint(1, len(constants.CHAMPIONS))]