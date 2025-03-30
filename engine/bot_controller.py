from bot import Bot
from utility import Direction, LocationInfo, ResourceInfo, Team, Location, BotType, BotInfo
from map import Map

class BotController:
    def __init__(self, map : Map, bot : Bot):
        self.map = map
        self.bot = bot

    def get_team(self) -> Team:
        return self.bot.team
    
    def get_type(self) -> BotType:
        return self.bot.type

    def get_id(self) -> int:
        return self.bot.id

    def get_location(self) -> Location:
        return self.bot.loc
    
    def get_hp(self) -> int:
        return self.bot.hp
    
    def get_map_size(self) -> tuple[int]:
        return self.map.map_size

    # TODO: Add constant
    def is_action_ready(self) -> bool:
        return self.bot.action_cooldown < 10
    
    # TODO: Add constant
    def is_movement_ready(self) -> bool:
        return self.bot.move_cooldown < 10
    
    def is_location_on_map(self, loc : Location) -> bool:
        return self.map.is_on_map(loc)

    def can_sense_location(self, loc : Location) -> bool:
        return self.map.can_sense_location(loc)
    
    def sense_location(self, loc : Location) -> LocationInfo:
        return self.map.sense_location(loc)

    def can_sense_bot_at_location(self, loc : Location) -> bool:
        return self.map.can_sense_bot_at_location(loc, self.bot.type)

    def sense_bot_at_location(self, loc : Location) -> BotInfo:
        return self.map.sense_bot_at_location(loc, self.bot.type)
    
    def sense_bots_in_range(self, team : Team, r : int = -1) -> list[BotInfo]:
        return self.map.sense_bots(self.bot.loc, self.bot.id,self.bot.type, team, r)
    
    def can_attack(self, loc : Location) -> bool:
        return self.is_action_ready() and self.map.can_attack(self.bot.loc, loc, self.bot.type)
    
    def attack(self, loc : Location):
        if not self.can_attack(loc):
            return
        if self.map.attack(self.bot.loc, loc, self.bot.type):
            self.bot.action_cooldown += self.bot.type.get_attack_cooldown()

    def can_move(self, dir : Direction) -> bool:
        return self.bot.type.can_move() and self.is_movement_ready() and self.map.can_move(self.bot.loc, self.bot.loc.add(dir))

    def move(self, dir : Direction):
        if not self.can_move(dir):
            return
        loc = self.bot.loc.add(dir)
        self.map.move_bot(self.bot.id, loc)
        self.bot.loc = loc
        self.bot.move_cooldown += self.bot.type.get_move_cooldown()        

    def can_take_resources(self, loc : Location):
        return self.is_action_ready() and self.map.can_take_resources(self.bot.loc, loc, self.bot.type)

    def take_resources(self, loc : Location):
        if not self.can_take_resources(loc):
            return
        self.map.take_resources(self.bot.loc, loc, self.bot.team, self.bot.type)
        self.bot.action_cooldown += self.bot.type.get_gather_cooldown()

    def get_team_resources(self) -> int:
        return self.map.get_team_resources(self.bot.team)

    def can_build_bot(self, loc : Location, type : BotType):
        return self.bot.type.can_build() and self.map.can_build_bot(self.bot.loc,loc,type,self.bot.team,self.bot.type)

    def build_bot(self, loc : Location, type : BotType):
        if not self.can_build_bot(loc, type):
            return
        self.map.build_bot(self.bot.loc,loc,type,self.bot.team,self.bot.type)

    def can_read_comms(self, i : int) -> bool:
        return self.map.can_read_comms(i)

    def read_comms(self, i : int) -> int:
        return self.read_comms(i)

    def can_write_comms(self, i : int, val : int) -> bool:
        return self.can_write_comms(i, val)

    def write_comms(self, i : int, val : int):
        self.map.write_comms(i, val, self.bot.team)

    def get_resources(self, r : int = -1) -> list[ResourceInfo]:
        return self.map.get_resources(self.bot.loc, self.bot.type, r)
    
    def get_round_number(self) -> int:
        return self.map.get_round_number()
    
    def set_indicator_string(self, s : str): # NOTE: Do not use commas or newlines for now
        self.bot.indicator_string = s

    def disintegrate(self):
        return self.map.disintegrate(self.bot.id)
    
    def resign(self):
        return self.map.resign(self.bot.team)
    
