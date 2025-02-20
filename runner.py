from map import Map
import importlib.util
import os
import sys

RED_TEAM_CODE = "grey_goo"
BLUE_TEAM_CODE = "grey_goo"
MAP_NAME = "test3"

red_code_file_name = "competition/" + RED_TEAM_CODE + "/robot.py"
blue_code_file_name = "competition/" + BLUE_TEAM_CODE + "/robot.py"
if (not os.path.exists(red_code_file_name)) or (
    not os.path.exists(blue_code_file_name)
):
    raise ImportError("Code file(s) don't exist.")

red_spec = importlib.util.spec_from_file_location(
    "red_competitor_code", red_code_file_name
)
blue_spec = importlib.util.spec_from_file_location(
    "blue_competitor_code", blue_code_file_name
)
red_mod = importlib.util.module_from_spec(red_spec)
blue_mod = importlib.util.module_from_spec(blue_spec)
sys.modules["red_competitor_code"] = red_mod
sys.modules["blue_competitor_code"] = blue_mod
red_spec.loader.exec_module(red_mod)
blue_spec.loader.exec_module(blue_mod)



m = Map(MAP_NAME, red_mod, blue_mod, RED_TEAM_CODE, BLUE_TEAM_CODE)

m.run()
