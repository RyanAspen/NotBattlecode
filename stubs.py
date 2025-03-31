from engine.utility import BotInfo, Direction, LocationInfo, ResourceInfo, Team, Location, BotType


def get_round_number() -> int:
    """
    Returns the current round number
    """
    pass

def get_map_size() -> tuple[int, int]:
    """
    Returns a tuple for the height and width of the current map
    """
    pass

def get_id() -> int:
    """
    Returns the unique identifier for this bot
    """
    pass

def get_team() -> Team:
    """
    Returns this bot's team
    """
    pass

def get_location() -> Location:
    """
    Returns this bot's current location
    """
    pass

def get_hp() -> int:
    """
    Returns this bot's current hp
    """
    pass

def get_type() -> BotType:
    """
    Returns this bot's type
    """
    pass

def get_team_resources() -> int:
    """
    Returns the total amount of resources that this bot's
    team has.
    """
    pass

def is_on_map(location : Location) -> bool:
    """
    Returns true if the given location is on the map, or false
    if the location is outside the map.
    """
    pass

def can_sense_location(location : Location) -> bool:
    """
    Returns true if the bot can sense the given location, or false
    if the location cannot be sensed by the bot.
    """
    pass

def sense_location(location : Location) -> LocationInfo:
    """
    Returns information about the location if it can be sensed.
    Return None if the location cannot be sensed.
    """
    pass

def is_action_ready() -> bool:
    """
    Returns true if the bot can act, or false otherwise.
    """
    pass

def is_movement_ready() -> bool:
    """
    Returns true if the bot can move, or false otherwise.
    """
    pass

def can_sense_bot_at_location(location : Location) -> bool:
    """
    Returns true if the bot can sense information about other bots at
    the given location, or false if the location cannot be sensed.
    """
    pass

def sense_bot_at_location(location : Location) -> BotInfo:
    """
    Returns information about the bot at the given location, if a bot is present.
    Returns None if no bot is present or the location cannot be sensed.
    """
    pass

def sense_bots_in_range(team : Team, r : int = -1) -> list[BotInfo]:
    """
    Returns a list of information entries about bots that can be sensed that are
    on the given team and are within r squared units of the current bot. If r = -1, r
    is ignored.
    """
    pass

def can_attack(location : Location) -> bool:
    """
    Returns true if the bot can attack the given location, or false otherwise.
    """
    pass

def attack(location : Location):
    """
    Attack the given location if possible.
    """
    pass

def can_move(dir : Direction) -> bool:
    """
    Returns true if the bot can move in the given direction, or false otherwise.
    """
    pass

def move(dir : Direction):
    """
    Move in the given direction if possible
    """
    pass

def can_take_resources(location : Location) -> bool:
    """
    Returns true if the bot can attempt to take resources from the given location,
    or false otherwise.
    """
    pass

def take_resources(location : Location):
    """
    Attempt to take resources from the given location if possible.
    """
    pass

def can_build_bot(location : Location, type : BotType) -> bool:
    """
    Returns true if the bot can create another bot of the given type in the
    given location, or false otherwise.
    """
    pass

def build_bot(location : Location, type : BotType):
    """
    Build a bot of the given type in the given location if possible.
    """
    pass

def can_read_comms(i : int) -> bool:
    """
    Returns true if the bot can read the given index in the communications array,
    or false otherwise
    """
    pass

def read_comms(i : int) -> int:
    """
    Returns the value stored in the given index in the communcations array.
    Returns None if the given index cannot be read.
    """
    pass

def can_write_comms(i : int, val : int) -> bool:
    """
    Returns true if the bot can write the given val at 
    the given index in the communications array, or false otherwise
    """
    pass

def write_comms(i : int, val : int):
    """
    Write the given val into the given index in the communcations array
    if possible.
    """
    pass

def get_resources(r : int = -1) -> list[ResourceInfo]:
    """
    Returns a list of information entries about all the resources
    the bot can currently sense.
    """
    pass

def set_indicator_string(s : str):
    """
    Set the value of the bot's indicator string, used for debugging.
    """
    pass

def disintegrate():
    """
    Destroy this bot.
    """
    pass

def resign():
    """
    Forfeit the round.
    """
    pass