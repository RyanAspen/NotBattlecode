from __future__ import annotations
from enum import Enum

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
            if y_diff > 0:
                return Direction.NORTHEAST
            elif y_diff < 0:
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
            if y_diff > 0:
                return Direction.NORTH
            elif y_diff < 0:
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

STARTING_HP = {"Basic" : 10}
BOT_COST = {"Basic" : 5}

class BotType:

    def __init__(self, type_str : str):
        self.type = type_str

    def __eq__(self, other : BotType):
        return self.type == other.type

    def get_starting_hp(self) -> int:
        return STARTING_HP[self.type]
    
    def get_cost(self) -> int:
        return BOT_COST[self.type]


class BotInfo:
    def __init__(self, id : int, loc : Location, type : BotType, hp : int, team : Team):
        self.id = id
        self.loc = loc
        self.botType = type
        self.hp = hp
        self.team = team

    def get_team(self) -> Team:
        return self.team

    def get_type(self) -> BotType:
        return self.botType

class LocationInfo:
    def __init__(self, loc : Location, resources : int, passable : bool):
        self.location = loc
        self.resources = resources
        self.passable = passable

class ResourceInfo:
    def __init__(self, loc : Location, resources : int):
        self.location = loc
        self.resources = resources

