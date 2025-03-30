from constants import *
from robot_runner import RobotRunner
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
        self.indicator_string = ""

        self.logs = []
        self.runner = None

    def __str__(self):
        s = str(self.id) + ","
        s += str(self.loc.x) + "," + str(self.loc.y) + ","
        s += self.type.type + ","
        s += str(self.hp) + ","
        s += str(self.team.team_id) + ","
        s += str(self.action_cooldown) + ","
        s += str(self.move_cooldown) + ","
        s += str(self.get_bytecode_used()) + ","
        s += str(self.indicator_string)
        return s

    def log(self, msg):
        self.logs.append(msg)

    def error(self, msg):
        self.logs.append(msg)

    def start(self, code, methods):
        self.runner = RobotRunner(code, methods, self.log, self.error, BYTECODE_LIMIT)

    def kill(self):
        self.runner.kill()

    def get_bytecode_limit(self) -> int:
        return self.runner.bytecode_limit

    def get_bytecode_left(self) -> int:
        return self.runner.bytecode
    
    def get_bytecode_used(self) -> int:
        return max(self.runner.bytecode_limit - self.runner.bytecode, 0)

    def get_bytecode_used(self):
        return max(self.get_bytecode_limit() - self.get_bytecode_left(), 0)

    def turn(self):
        self.process_beginning_of_turn()
        #print("Starting turn as ID =", self.id)
        self.runner.run()
        self.process_end_of_turn()

    def process_beginning_of_turn(self):
        self.move_cooldown = max(0, self.move_cooldown - 10)
        self.action_cooldown = max(0, self.action_cooldown - 10)
        self.indicator_string = ""

    def process_end_of_turn(self):
        self.indicator_string = ('{: <5}'.format(self.indicator_string))
        self.indicator_string = self.indicator_string[:20]