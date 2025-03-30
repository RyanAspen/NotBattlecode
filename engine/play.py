from code_container import CodeContainer
from map import Map
import sys

class RunGameArgs:
    player1_dir: str
    player2_dir: str
    player1_name: str  # Visual team name, not player path
    player2_name: str
    map_dir: str
    map_names: str  # Comma separated
    out_dir: str
    out_name: str | None
    show_indicators: bool
    debug: bool
    instrument: bool

def run_game(args: RunGameArgs):
    container_a = CodeContainer.create_from_directory(args.player1_dir, args.instrument)
    container_b = CodeContainer.create_from_directory(args.player2_dir, args.instrument)

    for map_name in args.map_names.split(","):
        map = Map(map_name, container_a, container_b, args.player1_name, args.player2_name)
        map.run()
    sys.exit("Success")
    

args = RunGameArgs()
args.player1_dir = "competition/nothing"
args.player2_dir = "competition/smarter_grey_goo"
args.player1_name = "NOTHING"
args.player2_name = "BETTER GREY GOO"
args.map_dir = "maps"
args.map_names = "smiles,test3"
args.out_dir = "replays"
args.show_indicators = False
args.instrument = True
args.debug = False

run_game(args)