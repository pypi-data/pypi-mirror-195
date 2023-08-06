from typing import Union
from shulker.functions.base_functions import *
import re

############ SAY ############

def meta_say(text: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"say {text}")
    return instructions

def say(text: str) -> Union[bool, str]:
    """This function sends a message in the chat"""
    check_output_channel()
    
    instructions = meta_say(text)
    
    for line in instructions["list"]:
        status = post(line)

######## BAN & KICK ########

def meta_ban(target: str, reason: str) -> dict:
    instructions = {"list": []}
    if reason is None:
        reason = ""
    instructions["list"].append(f"ban {target} {reason}")
    return instructions

def meta_banlist(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"banlist {option}")
    return instructions

def ban(target: str, reason: Union[str, None]) -> Union[bool, str]:
    """This function bans a player"""
    check_output_channel()
    
    instructions = meta_ban(target, reason)
    
    for line in instructions["list"]:
        status = post(line)
 
def ban_ip(target: str, reason: str) -> Union[bool, str]:
    """This function bans an IP"""
    check_output_channel()
    
    instructions = meta_ban(target, reason)
    
    for line in instructions["list"]:
        status = post(line)
        
def banlist(option: str) -> Union[bool, str]:
    """This functions fetches the banlist"""
    check_output_channel()
    
    instructions = meta_banlist(option)
    
    for line in instructions["list"]:
        status = post(line)

def meta_kick(target: str, reason: str) -> dict:
    instructions = {"list": []}
    if reason is None:
        reason = ""
    instructions["list"].append(f"kick {target} {reason}")
    return instructions

def kick(target: str, reason: Union[str, None]) -> Union[bool, str]:
    """This function kicks a player"""
    check_output_channel()
    
    instructions = meta_kick(target, reason)
    
    for line in instructions["list"]:
        status = post(line)

############ OP ############

def meta_op(target: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"op {target}")
    return instructions

def meta_deop(target: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"deop {target}")
    return instructions

def op(target: str) -> Union[bool, str]:
    """This function gives an operator status to a player"""
    check_output_channel()
    
    instructions = meta_op(target)
    
    for line in instructions["list"]:
        status = post(line)
        
def deop(target: str) -> Union[bool, str]:
    """This function removes an operator status from a player"""
    check_output_channel()
    
    instructions = meta_deop(target)
    
    for line in instructions["list"]:
        status = post(line)
        
############# SEED #############

def meta_seed() -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"seed")
    return instructions

def seed() -> Union[bool, str]:
    """This function fetches the seed of the world"""
    check_output_channel()
    
    instructions = meta_seed()
    
    for line in instructions["list"]:
        status = post(line)
    
    seed = re.match(r"Seed: \[(-{0,1}(\d+))\]", status)
    return seed.group(1)

############# DIFFICULTY #############

def meta_set_difficulty(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"difficulty {option}")
    return instructions

def meta_get_difficulty() -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"difficulty")
    return instructions

def set_difficulty(option: str) -> Union[bool, str]:
    """This function sets the difficulty of the world"""
    check_output_channel()
    
    instructions = meta_set_difficulty(option)
    
    for line in instructions["list"]:
        status = post(line)
        
def get_difficulty() -> Union[bool, str]:
    """This function fetches the difficulty of the world"""
    check_output_channel()
    
    instructions = meta_get_difficulty()
    
    for line in instructions["list"]:
        status = post(line)
    
    difficulty = re.match(r"The difficulty is (\w+)", status)
    return difficulty.group(1)


########### WEATHER ###########

def meta_weather(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"weather {option}")
    return instructions

def weather(option: str) -> Union[bool, str]:
    """This function sets the weather of the world
    Options: clear, rain, thunder"""
    
    check_output_channel()
    
    instructions = meta_weather(option)
    
    for line in instructions["list"]:
        status = post(line)