from utility import Direction, Team, Location, BotType, BotInfo
from map import Map

class BotController:
    def __init__(self, map : Map, id : int):
        bot = map.bots[id]
        self.map = map
        self.team = bot.team
        self.type = bot.type
        self.id = bot.id
        self.loc = bot.loc
        self.hp = bot.hp
        self.action_cooldown = bot.action_cooldown
        self.move_cooldown = bot.move_cooldown

    def get_team(self) -> Team:
        return self.team
    
    def get_type(self) -> BotType:
        return self.type

    def get_id(self) -> int:
        return self.id

    def get_location(self) -> Location:
        return self.loc
    
    def get_hp(self) -> int:
        return self.hp
    
    def get_map_size(self) -> tuple[int]:
        return self.map.map_size

    # TODO: Add constant
    def is_action_ready(self) -> bool:
        return self.action_cooldown < 10
    
    # TODO: Add constant
    def is_movement_ready(self) -> bool:
        return self.move_cooldown < 10
    
    def is_location_on_map(self, loc : Location) -> bool:
        return self.map.is_on_map(loc)

    def can_sense_bot_at_location(self, loc : Location) -> bool:
        return self.map.can_sense_bot_at_location(loc)

    def sense_bot_at_location(self, loc : Location) -> BotInfo:
        return self.map.sense_bot_at_location(loc)

    def sense_bots_in_range(self, r : int = -1) -> list[BotInfo]:
        return self.map.sense_bots(self.loc, self.id, r)
    
    def sense_bots_in_range(self, team : Team, r : int = -1) -> list[BotInfo]:
        return self.map.sense_bots(self.loc, self.id,team, r)
    
    def can_attack(self, loc : Location) -> bool:
        return self.is_action_ready() and self.map.can_attack(self.loc, loc)
    
    def attack(self, loc : Location):
        if not self.can_attack(loc):
            return
        if self.map.attack(self.loc, loc):
            self.action_cooldown += 10

    def can_move(self, dir : Direction) -> bool:
        return self.is_movement_ready() and self.map.can_move(self.loc, self.loc.add(dir))

    def move(self, dir : Direction):
        if not self.can_move(dir):
            return
        loc = self.loc.add(dir)
        self.map.move_bot(self.id, loc)
        self.loc = loc
        self.move_cooldown += 10        