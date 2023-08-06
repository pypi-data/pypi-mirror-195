import json
import os

from typing import Union

from shulker.components.BlockCoordinates import BlockCoordinates
from shulker.components.NBT import NBT
from shulker.components.Coordinates import Coordinates

from shulker.functions.base_functions import *


def meta_summon(entity: str, coords: BlockCoordinates, nbt_data: NBT) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"summon {entity} {coords} {nbt_data}")
    return instructions


def summon(
    entity: str,
    coords: Union[BlockCoordinates, Coordinates, tuple],
    nbt_data: Union[NBT, dict, str, None] = None
) -> Union[bool, str]:
    """
    Returns a bool that is set to True
    if no message was sent back by the game or the
    message itself if there was an issue

    Summons an entity
    """

    check_output_channel()
    
    entities = entity_list()
        
    if type(entity) is not str:
        raise TypeError(f"Expected type str, got {type(entity)}")
    elif entity.replace("minecraft:", "") not in entities:
        raise ValueError(f"Entity {entity} is not a valid entity")
    
    if nbt_data is not None:
        nbt_data = format_arg(nbt_data, NBT)
    else:
        nbt_data = ""

    coords = format_arg(coords, Coordinates)
        
    instructions = meta_summon(entity, coords, nbt_data)

    for line in instructions["list"]:
        status = post(line)
        print(line)
        
    return True if status.startswith("") else status
