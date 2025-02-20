import random
import numpy as np

import os

from bot import Bot
from game_state import RoundData
from utility import BotInfo, BotType, Location, LocationInfo, Team

MAX_GAME_LENGTH = 2000
PASSIVE_INCOME = 1

# Maintains location information
class Map:

    def __init__(self, map_name, red_mod, blue_mod, red_name, blue_name):
        self.red_mod = red_mod
        self.blue_mod = blue_mod
        self.replay_name_file = "replays\\" + map_name + "_" + red_name + "vs" + blue_name + ".rpy"
        
        self.bots = {}
        self.bot_order = []
        self.round = 1        

        self.red_resources = 0
        self.blue_resources = 0

        with open("maps\\" + map_name + ".map", "r") as f:
            lines = f.readlines()
            if lines[2].strip() not in ('HORIZONTAL', 'VERTICAL', 'ROTATIONAL'):
                print("Invalid Symmetry = ", lines[1])
                return
            self.map_name = lines[0]
            self.map_size = tuple(map(int,lines[1].split()))
            self.symmetry = lines[2].strip()
            self.terrain_map = np.ones(self.map_size, dtype=bool)
            self.resource_map = np.zeros(self.map_size, dtype=int)
            self.bot_map = np.zeros(self.map_size, dtype=int)
            for y in range(self.map_size[0]):
                line = lines[3+y]
                x = 0
                for t in line.split(',')[:-1]:
                    if t == 'x':
                        self.terrain_map[y][x] = False
                    x += 1
            for y in range(self.map_size[0]):
                line = lines[self.map_size[0]+3+y]
                x = 0
                for r in line.split(',')[:-1]:
                    self.resource_map[y][x] = int(r)
                    x += 1
            self.r = 0
            self.b = 0
            for line in lines[self.map_size[0]*2+3:]:
                
                x,y = tuple(map(int,line.split()))
                self.spawn_bot(Location(x,y),BotType("Basic"),Team(True))
                if self.symmetry == "ROTATIONAL":
                    self.spawn_bot(Location(self.map_size[1]-x-1,self.map_size[0]-y-1),BotType("Basic"),Team(False))
                elif self.symmetry == "VERTICAL":
                    self.spawn_bot(Location(x,self.map_size[0]-y-1),BotType("Basic"),Team(False))
                else:
                    self.spawn_bot(Location(self.map_size[1]-x-1,y),BotType("Basic"),Team(False))

        if os.path.exists(self.replay_name_file):
            os.remove(self.replay_name_file)
        with open(self.replay_name_file, "x") as f:
            f.write(str(self.map_size[0]) + "," + str(self.map_size[1]) + "\n")
            for t in self.terrain_map.flatten():
                if t:
                    f.write("1")
                else:
                    f.write("0")
            f.write("\n")

    def run(self):
        while not self.run_one_round():
            pass
        round_data = RoundData(self.bots, self.terrain_map, self.resource_map)
        with open(self.replay_name_file, "a") as f:
            round_data.add_to_file(f)
        if self.r == 0:
            print("BLUE WINS BY DESTRUCTION")
        elif self.b == 0:
            print("RED WINS BY DESTRUCTION")
        elif self.r > self.b:
            print("RED WINS BY MAJORITY")
        elif self.b > self.r:
            print("BLUE WINS BY MAJORITY")
        else:
            if random.choice([True, False]):
                print("RED WINS BY TIEBREAKER")
            else:
                print("BLUE WINS BY TIEBREAKER")

    # Return true if the game is done
    def run_one_round(self) -> bool:
        self.red_resources += PASSIVE_INCOME
        self.blue_resources += PASSIVE_INCOME
        round_data = RoundData(self.bots, self.terrain_map, self.resource_map)
        with open(self.replay_name_file, "a") as f:
            round_data.add_to_file(f)
        i = 0
        n = len(self.bot_order)
        while i < n:
            if self.bot_order[i] > -1:
                self.run_bot(self.bot_order[i])
            i += 1
        self.bot_order = [b for b in self.bot_order if b > -1]      

        #print(self.round, self.r, self.b)  
        self.round += 1
        #print(self.bot_order)
        
        return self.is_game_done()        

    # run() must be implemented for both bot modules
    def run_bot(self, id):
        from bot_controller import BotController
        if id not in self.bots:
            return
        bot = self.bots[id]
        if bot.team.team_id == True:
            self.red_mod.run(BotController(self,id))
        else:
            self.blue_mod.run(BotController(self,id))
        


    def is_game_done(self) -> bool:
        if self.round > MAX_GAME_LENGTH:
            return True
        if self.r == 0 or self.b == 0:
            return True
        return False


    def is_on_map(self, location : Location) -> bool:
        return location.x >= 0 and location.y >= 0 and location.x < self.map_size[1] and location.y < self.map_size[0]

    # TODO: Add constant
    def can_sense_location(self, curr_loc : Location, sense_loc : Location) -> bool:
        if curr_loc.distance_squared_to(sense_loc) > 10:
            return False
        if not self.is_on_map(sense_loc):
            return False
        return True

    def sense_location(self, curr_loc : Location, sense_loc : Location) -> LocationInfo:
        """
            Contains:
                - The Location (again)
                - Terrain information
                - Resource information
        """
        if not self.can_sense_bot_at_location(curr_loc, sense_loc):
            return None
        return LocationInfo(sense_loc, self.resource_map[sense_loc.y][sense_loc.x], self.terrain_map[sense_loc.y][sense_loc.x])

    def spawn_bot(self, location : Location, bot_type : BotType, team : Team):
        if not self.is_on_map(location):
            print(location.x, location.y, "Not on map")
            return
        new_bot = Bot(location, bot_type, team)
        if team.team_id == True:
            self.r += 1
        else:
            self.b += 1
        self.bot_map[location.y][location.x] = new_bot.id
        self.bots[new_bot.id] = new_bot
        self.bot_order.append(new_bot.id)

    def can_move(self, curr_loc : Location, new_loc : Location) -> bool:
        if not curr_loc.is_adjacent_to(new_loc):
            return False
        if not self.is_on_map(new_loc):
            return False
        if not self.terrain_map[new_loc.y][new_loc.x]:
            return False
        return self.bot_map[new_loc.y][new_loc.x] == 0
        

    def move_bot(self, bot_id : int, location : Location):
        if bot_id not in self.bots:
            return
        
        old_location = self.bots[bot_id].loc
        if not self.can_move(old_location, location):
            return

        self.bot_map[old_location.y][old_location.x] = 0
        self.bots[bot_id].loc = location
        self.bot_map[location.y][location.x] = bot_id

    def despawn_bot(self, bot_id : int):
        if bot_id not in self.bots:
            return
        location = self.bots[bot_id].loc
        self.bot_map[location.y][location.x] = 0
        self.bot_order[self.bot_order.index(bot_id)] = -1
        if self.bots[bot_id].team.team_id == True:
            self.r -= 1
        else:
            self.b -= 1
        del self.bots[bot_id]

    # TODO: Add constant
    def can_sense_bot_at_location(self, curr_loc : Location, sense_loc : Location) -> bool:
        if curr_loc.distance_squared_to(sense_loc) > 10:
            return False
        if not self.is_on_map(sense_loc):
            return False
        return True
    
    def sense_bot_at_location(self, curr_loc : Location, sense_loc : Location) -> BotInfo:
        if not self.can_sense_bot_at_location(curr_loc, sense_loc):
            return None
        id = self.bot_map[sense_loc.y][sense_loc.x]
        if id == 0:
            return None
        bot = self.bots[id]
        return BotInfo(bot.id, bot.loc, bot.type, bot.hp, bot.team)

    # TODO: Add constant
    def can_attack(self, curr_loc : Location, attack_loc : Location) -> bool:
        if curr_loc.distance_squared_to(attack_loc) > 10:
            return False
        if not self.is_on_map(attack_loc):
            return False
        return True
    
    # TODO: Add constant
    # Returns true if the attack happens
    def attack(self, curr_loc : Location, attack_loc : Location) -> bool:
        if not self.can_attack(curr_loc, attack_loc):
            return False
        id = self.bot_map[attack_loc.y][attack_loc.x] 
        if id > 0:
            target = self.bots[id]
            target.hp -= 1
            if target.hp <= 0:
                self.despawn_bot(id)
        return True        

    # TODO: Add constant
    def get_locations_within_radius(self, loc : Location, radius : int) -> list[Location]:
        locs = []
        x_min = max(0, loc.x-3)
        x_max = min(self.map_size[1]-1, loc.x+3)
        y_min = max(0, loc.y-3)
        y_max = min(self.map_size[0]-1, loc.y+3)
        for x in range(x_min,x_max+1):
            for y in range(y_min, y_max+1):
                new_loc = Location(x,y)
                if loc.is_within_distance_squared(new_loc, radius):
                    locs.append(Location(x,y))
        return locs

    # TODO: Add constant
    def sense_bots(self, curr_loc : Location, curr_id : int, radius : int = -1) -> list[BotInfo]:
        bots = []
        if radius == -1:
            radius = 10
        if radius < 0 or radius > 10:
            return bots
        locs = self.get_locations_within_radius(curr_loc, radius)
        for loc in locs:
            id = self.bot_map[loc.y][loc.x]
            if id > 0 and id != curr_id:
                bot = self.bots[id]
                bots.append(BotInfo(bot.id, bot.loc, bot.type, bot.hp, bot.team))
        return bots

    def sense_bots(self, curr_loc : Location, curr_id : int, team : Team, radius : int = -1) -> list[BotInfo]:
        bots = []
        if radius == -1:
            radius = 10
        if radius < 0 or radius > 10:
            return bots
        locs = self.get_locations_within_radius(curr_loc, radius)
        for loc in locs:
            id = self.bot_map[loc.y][loc.x]
            if id > 0 and id != curr_id:
                bot = self.bots[id]
                if bot.team == team:
                    bots.append(BotInfo(bot.id, bot.loc, bot.type, bot.hp, bot.team))
        return bots            

    # TODO: Add constant
    def can_take_resources(self, curr_loc : Location, sense_loc : Location) -> bool:
        if curr_loc.distance_squared_to(sense_loc) > 10:
            return False
        if not self.is_on_map(sense_loc):
            return False
        return True
    
    def take_resources(self, curr_loc : Location, sense_loc : Location, team : Team):
        if not self.can_take_resources(curr_loc, sense_loc):
            return
        if self.resource_map[sense_loc.y][sense_loc.x] > 0:
            self.resource_map[sense_loc.y][sense_loc.x] -= 1
            if team.team_id:
                self.red_resources += 1
            else:
                self.blue_resources += 1

    def get_resources(self, team : Team) -> int:
        if team.team_id:
            return self.red_resources
        else:
            return self.blue_resources

    def can_build_bot(self, curr_loc : Location, build_loc : Location, type : BotType, team : Team):
        if curr_loc.is_adjacent_to(build_loc) and self.is_on_map(build_loc) and self.get_resources(team) >= type.get_cost():
            if self.terrain_map[build_loc.y][build_loc.x] and self.bot_map[build_loc.y][build_loc.x] == 0:
                return True
        return False
    
    def build_bot(self, curr_loc : Location, build_loc : Location, type : BotType, team : Team):
        if not self.can_build_bot(curr_loc, build_loc, type, team):
            return
        self.spawn_bot(build_loc,type,team)
        if team.team_id:
            self.red_resources -= type.get_cost()
        else:
            self.blue_resources -= type.get_cost()