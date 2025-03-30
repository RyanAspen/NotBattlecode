import random

from stubs import *

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

def turn():

    #set_indicator_string("Hello World!")
    for dir in dirs:
        if can_build_bot(get_location().add(dir), BotType("Basic")):
            build_bot(get_location().add(dir), BotType("Basic"))
            set_indicator_string("Built bot at " + str(dir))
            break

    set_indicator_string("TEST")
    bots = sense_bots_in_range(get_team().get_opponent())
    set_indicator_string(str(len(bots)))
    for bot in bots:
        if can_attack(bot.loc):
            attack(bot.loc)
            set_indicator_string("Attacking")
            break
        
    for dir in dirs:
        if can_take_resources(get_location().add(dir)):
            take_resources(get_location().add(dir))
            set_indicator_string("Taking resources at " + str(dir))
            break
        
    dir = random.choice(dirs)


    #set_indicator_string(str(can_move(dir)))
    if can_move(dir):
        set_indicator_string("Moving to " + str(dir))
        move(dir)
    else:
        set_indicator_string("Cannot move to " + str(dir))

    
    