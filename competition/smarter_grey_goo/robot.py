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

    if get_type() == BotType("Base"):
        for dir in dirs:
            if can_build_bot(get_location().add(dir), BotType("Basic")):
                build_bot(get_location().add(dir), BotType("Basic"))
                break

    is_base = False
    min_hp = 9999
    attack_loc = None
    bots = sense_bots_in_range(get_team().get_opponent())
    for bot in bots:
        if can_attack(bot.loc):
            hp = bot.get_hp()
            if is_base and bot.get_type() != BotType("Base"):
                continue
            elif not is_base and bot.get_type() == BotType("Base"):
                is_base = True
                min_hp = hp
                attack_loc = bot.get_location()
            elif hp < min_hp:
                min_hp = hp
                attack_loc = bot.get_location()

    if attack_loc is not None:
        attack(attack_loc)

    if get_type() == BotType("Basic"):
        
        #closest_loc = None
        #closest_dist = 99999
        #for bot in bots:
        #    if bot.get_type() == BotType("Base"):
        #        #print("Enemy Base at ", bot.get_location())
        #        dist = bot.get_location().distance_squared_to(bc.get_location())
        #        if dist < closest_dist:
        #            closest_dist = dist
        #            closest_loc = bot.get_location()
        
        #if closest_loc is not None and bc.can_move(bc.get_location().direction_to(closest_loc)) and bc.get_hp() > 5:
        #    #print("Moving towards Enemy Base at ", closest_loc)
        #    bc.move(bc.get_location().direction_to(closest_loc))
        #else:
        closest_loc = None
        closest_dist = 99999
        for r in get_resources():
            dist = r.get_location().distance_squared_to(get_location())
            if dist < closest_dist:
                closest_dist = dist
                closest_loc = r.get_location()
        if closest_loc is not None and closest_loc == get_location():
            pass
        elif closest_loc is not None and can_move(get_location().direction_to(closest_loc)):
            #print("Moving towards Resource at ", closest_loc)
            move(get_location().direction_to(closest_loc))
        else:
            #print("Moving randomly")
            d = dirs.copy()
            random.shuffle(d)
            for dir in d:
                if can_move(dir):
                    move(dir)
        if can_take_resources(get_location()):
            take_resources(get_location())
        else:
            for dir in dirs:
                if can_take_resources(get_location().add(dir)):
                    take_resources(get_location().add(dir))
                    break
        
        
        
    
    