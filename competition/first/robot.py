from bot_controller import BotController
from utility import Direction
import random


dirs = [
    Direction.NORTH,
    Direction.NORTHEAST,
    Direction.EAST,
    Direction.SOUTHEAST,
    Direction.SOUTH,
    Direction.SOUTHWEST,
    Direction.WEST,
    Direction.NORTHWEST
]

def run(bc : BotController):
    dir = random.choice(dirs)
    if bc.can_move(dir):
        bc.move(dir)

    bots = bc.sense_bots_in_range(bc.get_team().get_opponent())
    for bot in bots:
        if bc.can_attack(bot.loc):
            bc.attack(bot.loc)
            break