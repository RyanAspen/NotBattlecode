import random

from stubs import *

def get_nearest_enemy_base():
    closest_base = None
    closest_dist = 9999
    for i in range(3):
        bx = read_comms(2*i) - 1
        by = read_comms(2*i+1) - 1
        if bx >= 0:
            loc = Location(bx,by)
            dist = loc.distance_squared_to(get_location())
            if dist < closest_dist:
                closest_base = loc
                closest_dist = dist
    return closest_base

def refresh_enemy_bases():
    for i in range(3):
        bx = read_comms(2*i) - 1
        by = read_comms(2*i+1) - 1
        if bx >= 0:
            loc = Location(bx,by)
            if can_sense_bot_at_location(loc):
                b = sense_bot_at_location(loc)
                #if b is None or b.get_type() != BotType("Base"):
                #    write_comms(2*i,0)
                #    write_comms(2*i+1,0)


def report_enemy_bases():
    bots = sense_bots_in_range(get_team().get_opponent())
    bases = []
    for bot in bots:
        if bot.get_type() == BotType("Base"):
            bases.append(bot.get_location())
    for base in bases:
        idx = -1
        for i in range(3):
            bx = read_comms(2*i) - 1
            by = read_comms(2*i + 1) - 1
            if bx < 0:
                idx = i
            elif bx == base.x and by == base.y:
                idx = -1
                break
        if idx > -1:
            write_comms(2*idx, base.x+1)
            write_comms(2*idx+1, base.y+1)


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

def my_move(target = None):
    if not is_movement_ready() or not get_type().can_move():
        return
    if target is not None:
        dir = get_location().direction_to(target)
        if can_move(dir):
            move(dir)
        else:
            dirs_copy = dirs.copy()
            random.shuffle(dirs_copy)
            for d in dirs_copy:
                if can_move(d):
                    move(d)
    else:
        d = dirs.copy()
        random.shuffle(d)
        for dir in d:
            if can_move(dir):
                move(dir)

def my_attack():
    if not is_action_ready():
        return
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

def gather():
    if not get_type().can_take_resources():
        return
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
        my_move(closest_loc)
    if can_take_resources(get_location()):
        take_resources(get_location())
    else:
        for dir in dirs:
            if can_take_resources(get_location().add(dir)):
                take_resources(get_location().add(dir))
                break

def turn():
    report_enemy_bases()
    refresh_enemy_bases()
    target = get_nearest_enemy_base()
    #if target is not None:
    #    set_indicator_string(str(target.x) + "-" + str(target.y))
    if get_type() == BotType("Base"):
        for dir in dirs:
            if can_build_bot(get_location().add(dir), BotType("Basic")):
                build_bot(get_location().add(dir), BotType("Basic"))
                break
    my_attack()
    gather()
    my_move(target)