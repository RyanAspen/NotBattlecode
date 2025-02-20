from __future__ import annotations
from enum import Enum

from constants import ATTACK_COOLDOWN, ATTACK_RANGE, ATTACK_STRENGTH, BOT_COST, BUILD_RANGE, CAN_BUILD, CAN_GATHER, CAN_MOVE, GATHER_COOLDOWN, GATHER_RANGE, MOVE_COOLDOWN, STARTING_HP, VISION_RANGE


class Direction(Enum):
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7
    NORTHWEST = 8
    CENTER = 9

DIRECTION_OFFSETS = {
    Direction.NORTH : (0,-1),
    Direction.NORTHEAST : (1,-1),
    Direction.EAST : (1,0),
    Direction.SOUTHEAST : (1,1),
    Direction.SOUTH : (0,1),
    Direction.SOUTHWEST : (-1,1),
    Direction.WEST : (-1, 0),
    Direction.NORTHWEST : (-1,-1),
    Direction.CENTER : (0,0)
}

class Location:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y

    def __eq__(self, other : Location):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance_squared_to(self, loc : Location) -> int:
        return (self.x-loc.x)**2 + (self.y-loc.y)**2
    
    def is_within_distance_squared(self, loc : Location, dist : int) -> bool:
        return (self.x-loc.x)**2 + (self.y-loc.y)**2 <= dist
    
    def is_adjacent_to(self, loc : Location) -> bool:
        return abs(self.x-loc.x) <= 1 and abs(self.y-loc.y) <= 1

    def add(self, dir : Direction) -> Location:
        dx, dy = DIRECTION_OFFSETS[dir]
        return Location(self.x + dx, self.y + dy)

    def direction_to(self, loc : Location) -> Direction:
        x_diff = loc.x - self.x
        y_diff = loc.y - self.y
        if x_diff > 0:
            if y_diff < 0:
                return Direction.NORTHEAST
            elif y_diff > 0:
                return Direction.SOUTHEAST
            else:
                return Direction.EAST
        elif x_diff < 0:
            if y_diff > 0:
                return Direction.NORTHWEST
            elif y_diff < 0:
                return Direction.SOUTHWEST
            else:
                return Direction.WEST
        else:
            if y_diff < 0:
                return Direction.NORTH
            elif y_diff > 0:
                return Direction.SOUTH
            else:
                return Direction.CENTER

class Team:
    def __init__(self, team_id : bool):
        self.team_id = team_id

    def __eq__(self, other : Team):
        return self.team_id == other.team_id

    def get_opponent(self) -> Team:
        return Team(not self.team_id)



class BotType:

    def __init__(self, type_str : str):
        self.type = type_str

    def __eq__(self, other : BotType):
        return self.type == other.type

    def get_starting_hp(self) -> int:
        return STARTING_HP[self.type]
    
    def get_cost(self) -> int:
        return BOT_COST[self.type]
    
    def get_attack_range(self) -> int:
        return ATTACK_RANGE[self.type]
    
    def get_vision_range(self) -> int:
        return VISION_RANGE[self.type]
    
    def get_build_range(self) -> int:
        return BUILD_RANGE[self.type]
    
    def get_gather_range(self) -> int:
        return GATHER_RANGE[self.type]
    
    def get_attack_cooldown(self) -> int:
        return ATTACK_COOLDOWN[self.type]
    
    def get_gather_cooldown(self) -> int:
        return GATHER_COOLDOWN[self.type]
    
    def get_move_cooldown(self) -> int:
        return MOVE_COOLDOWN[self.type]
    
    def can_move(self) -> bool:
        return CAN_MOVE[self.type]
    
    def can_take_resources(self) -> bool:
        return CAN_GATHER[self.type]

    def can_build(self) -> bool:
        return CAN_BUILD[self.type]
    
    def get_attack_strength(self) -> int:
        return ATTACK_STRENGTH[self.type]


class BotInfo:
    def __init__(self, id : int, loc : Location, type : BotType, hp : int, team : Team):
        self.id = id
        self.loc = loc
        self.botType = type
        self.hp = hp
        self.team = team

    def get_id(self) -> int:
        return self.id

    def get_team(self) -> Team:
        return self.team

    def get_hp(self) -> int:
        return self.hp

    def get_type(self) -> BotType:
        return self.botType
    
    def get_location(self) -> Location:
        return self.loc

class LocationInfo:
    def __init__(self, loc : Location, resources : int, passable : bool):
        self.location = loc
        self.resources = resources
        self.passable = passable

    def get_location(self) -> Location:
        return self.location
    
    def get_resources(self) -> int:
        return self.resources
    
    def is_passable(self) -> bool:
        return self.passable

class ResourceInfo:
    def __init__(self, loc : Location, resources : int):
        self.location = loc
        self.resources = resources

    def get_location(self) -> Location:
        return self.location
    
    def get_resources(self) -> int:
        return self.resources

