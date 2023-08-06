from typing import Union
from shulker.functions.base_functions import *


def meta_say(text: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"say {text}")
    return instructions


def say(
    text: str,
) -> Union[bool, str]:
    """
    Returns a bool that is set to True
    if no message was sent back by the game or the
    message itself if there was an issue

    This function sends a message in the chat
    """

    check_output_channel()
    
    if type(text) is not str:
        raise TypeError(f"Expected type str, got {type(text)}")

    instructions = meta_say(text)

    for line in instructions["list"]:
        status = post(line)

    return True if status.startswith("") else status
