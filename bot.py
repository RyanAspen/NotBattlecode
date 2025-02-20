from utility import Location, BotType, Team
from id_generator import id_generator

class Bot:

    def __init__(self, loc : Location, type : BotType, team : Team):
        self.id = id_generator.get_next_id()
        self.loc = loc
        self.type = type
        self.hp = type.get_starting_hp()
        self.team = team
        self.action_cooldown = 0
        self.move_cooldown = 0

    def __str__(self):
        s = str(self.id) + ","
        s += str(self.loc.x) + "," + str(self.loc.y) + ","
        s += self.type.type + ","
        s += str(self.hp) + ","
        s += str(self.team.team_id)
        return s

    def get_type(self) -> BotType:
        return self.type
