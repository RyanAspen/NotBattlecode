import numpy as np

class RoundData:

    def __init__(self, bots, terrain_map, resource_map):
        self.bots = bots
        self.terrain_map = terrain_map
        self.resource_map = resource_map

    def add_to_file(self, f):
        for r in self.resource_map.flatten():
            f.write(str(r) + ",")
        f.write("\n")
        f.write(str(len(self.bots)) + "\n")
        for bot_string in [str(x) for x in list(self.bots.values())]:
            f.write(bot_string + "\n")
