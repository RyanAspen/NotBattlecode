class RoundData:

    def __init__(self, bots, terrain_map, resource_map):
        self.bots = bots
        self.terrain_map = terrain_map
        self.resource_map = resource_map
        self.attacks = []

    def add_attack(self, attack_loc, defend_loc):
        self.attacks.append((attack_loc, defend_loc))

    def add_to_file(self, f):
        for r in self.resource_map.flatten():
            f.write(str(r) + ",")
        f.write("\n")
        f.write(str(len(self.bots)) + "\n")
        for bot_string in [str(x) for x in list(self.bots.values())]:
            f.write(bot_string + "\n")
        f.write(str(len(self.attacks)) + "\n")
        for a_loc, d_loc in self.attacks:
            f.write(str(a_loc.x) + "," + str(a_loc.y) + "," + str(d_loc.x) + "," + str(d_loc.y) + "\n")
        
