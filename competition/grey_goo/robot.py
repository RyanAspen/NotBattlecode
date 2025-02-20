from bot_controller import BotController
from utility import Direction, BotType
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

    for dir in dirs:
        if bc.can_build_bot(bc.get_location().add(dir), BotType("Basic")):
            bc.build_bot(bc.get_location().add(dir), BotType("Basic"))
            return

    bots = bc.sense_bots_in_range(bc.get_team().get_opponent())
    for bot in bots:
        if bc.can_attack(bot.loc):
            bc.attack(bot.loc)
            return
        
    for dir in dirs:
        if bc.can_take_resources(bc.get_location().add(dir)):
            bc.take_resources(bc.get_location().add(dir))
            return
        
    dir = random.choice(dirs)
    if bc.can_move(dir):
        bc.move(dir)
    
    