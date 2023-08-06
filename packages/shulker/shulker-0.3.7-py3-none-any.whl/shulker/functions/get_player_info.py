import re
from typing import Union

from shulker.components.BlockCoordinates import BlockCoordinates
from shulker.components.Coordinates import Coordinates
from shulker.components.NBT import NBT

from shulker.functions.base_functions import *


def meta_get_player_info(pseudo: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"data get entity {pseudo}")
    return instructions


def get_player_info(
    pseudo: str,
) -> Union[bool, str]:
    """
    Returns the NBT data of the player
    """

    check_output_channel()
    
    if type(pseudo) is not str:
        raise TypeError(f"Expected type str, got {type(pseudo)}")

    instructions = meta_get_player_info(pseudo)

    for line in instructions["list"]:
        status = post(line)
        
    if status.startswith(f"{pseudo} has"):
        return NBT(status.split("data: ")[1])
    else:
        return False
    

def get_player_pos(
    pseudo: str,
    rounded: bool = True
) -> Union[bool, str]:
    """
    Returns the coordinates of the player if it is found
    False if it wasn't found or there's an issue
    """

    check_output_channel()
    
    if type(pseudo) is not str:
        raise TypeError(f"Expected type str, got {type(pseudo)}")

    instructions = meta_get_player_info(pseudo)

    for line in instructions["list"]:
        status = post(line)
        
    if status.startswith(f"{pseudo} has"):
        matches = re.findall(r"Pos: \[(.+?)\..+?, (.+?)\..+?, (.+?)\..+?\]", status)
        if len(matches) == 3:
            if rounded:
                return BlockCoordinates(*tuple(map(round, matches)))
            else:
                return Coordinates(*tuple(matches))
    else:
        return False
