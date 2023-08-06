from typing import Union
from shulker.functions.base_functions import *
from shulker.components.Coordinates import Coordinates
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

def meta_pardon(target: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"pardon {target}")
    return instructions

def meta_pardon_ip(target: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"pardon-ip {target}")
    return instructions

def pardon(target: str) -> Union[bool, str]:
    """This function unbans a player"""
    check_output_channel()
    
    instructions = meta_pardon(target)
    
    for line in instructions["list"]:
        status = post(line)

def pardon_ip(target: str) -> Union[bool, str]:
    """This function unbans an IP"""
    check_output_channel()
    
    instructions = meta_pardon_ip(target)
    
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
        
########### MSG ###########

def meta_msg(target: str, message: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"msg {target} {message}")
    return instructions

def msg(target: str, message: str) -> Union[bool, str]:
    """This function sends a private message to a player"""
    
    check_output_channel()
    
    instructions = meta_msg(target, message)
    
    for line in instructions["list"]:
        status = post(line)

########### GAMEMODE ###########

def meta_default_gamemode(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"defaultgamemode {option}")
    return instructions

def meta_gamemode(target: str, option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"gamemode {option} {target}")
    return instructions

def gamemode(target: str, option: str) -> Union[bool, str]:
    """This function sets the gamemode of a player
    Available options: survival, creative, adventure, spectator"""
    
    check_output_channel()
    
    instructions = meta_gamemode(target, option)
    
    for line in instructions["list"]:
        status = post(line)
        
def default_gamemode(option: str) -> Union[bool, str]:
    """This function sets the default gamemode of the world
    Available options: survival, creative, adventure, spectator"""
    
    check_output_channel()
    
    instructions = meta_default_gamemode(option)
    
    for line in instructions["list"]:
        status = post(line)

########### TIME ###########

def meta_query_time(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"time query {option}")
    return instructions

def query_time(option: str = "day") -> Union[bool, str]:
    """This function fetches the time of the world
    Available options: day, daytime, gametime"""
    
    check_output_channel()
    
    instructions = meta_query_time(option)
    
    for line in instructions["list"]:
        status = post(line)
        
    time = re.match(r"The time is (\d+)", status)
    return time.group(1)

def meta_add_time(value: int, option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"time add {value}{option}")
    return instructions

def add_time(value: int, option: str = "tick") -> Union[bool, str]:
    """This function adds time to the world
    Available options: day, second, tick"""
    
    check_output_channel()
    
    option = option[0]
    
    instructions = meta_add_time(value, option)
    
    for line in instructions["list"]:
        status = post(line)
        
def meta_set_time(value: int, option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"time set {value}{option}")
    return instructions

def set_time(value: int, option: str = "tick") -> Union[bool, str]:
    """This function sets the time of the world
    Available options: day, second, tick"""
    
    check_output_channel()
    
    option = option[0]
    
    instructions = meta_set_time(value, option)
    
    for line in instructions["list"]:
        status = post(line)
        
def meta_time(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"time set {option}")
    return instructions

def time(option: str) -> Union[bool, str]:
    """This function sets the time of the world
    Available options: day, midnight, night, noon"""
    
    check_output_channel()
    
    instructions = meta_time(option)
    
    for line in instructions["list"]:
        status = post(line)
        
########### EXPERIENCE ###########

def meta_xp_query(target: str, option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"xp query {target} {option}")
    return instructions

def xp_query(target: str, option: str) -> Union[bool, str]:
    """This function fetches the experience of a player
    Available options: levels, points"""
    
    check_output_channel()
    
    instructions = meta_xp_query(target, option)
    
    for line in instructions["list"]:
        status = post(line)
    
    xp = re.findall(r"(\d+) experience " + option, status)
    return xp[0]

########### WHITELIST ###########

def meta_get_whitelist() -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"whitelist list")
    return instructions

def get_whitelist() -> Union[bool, str]:
    """This function fetches the whitelist of the world"""
    
    check_output_channel()
    
    instructions = meta_get_whitelist()
    
    for line in instructions["list"]:
        status = post(line)[:-4]
        
    whitelist = status.split("players: ")[1].split(", ")
    return whitelist

def meta_toggle_whitelist(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"whitelist {option}")
    return instructions

def toggle_whitelist(option: str) -> Union[bool, str]:
    """This function toggles the whitelist of the world
    Available options: on, off"""
    
    check_output_channel()
    
    instructions = meta_toggle_whitelist(option)
    
    for line in instructions["list"]:
        status = post(line)
        
def meta_reload_whitelist() -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"whitelist reload")
    return instructions

def reload_whitelist() -> Union[bool, str]:
    """This function reloads the whitelist of the world"""
    
    check_output_channel()
    
    instructions = meta_reload_whitelist()
    
    for line in instructions["list"]:
        status = post(line)
        
def meta_update_whitelist(option: str, target: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"whitelist {option} {target}")
    return instructions

def update_whitelist(option: str, target: str) -> Union[bool, str]:
    """This function updates the whitelist of the world
    Available options: add, remove"""
    
    check_output_channel()
    
    instructions = meta_update_whitelist(option, target)
    
    for line in instructions["list"]:
        status = post(line)
        
############ ADMIN ############

def meta_stop() -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"stop")
    return instructions

def stop() -> Union[bool, str]:
    """This function stops the server"""
    
    check_output_channel()
    
    instructions = meta_stop()
    
    for line in instructions["list"]:
        status = post(line)
        
def meta_save_all() -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"save-all")
    return instructions

def save_all() -> Union[bool, str]:
    """This function saves the world"""
    
    check_output_channel()
    
    instructions = meta_save_all()
    
    for line in instructions["list"]:
        status = post(line)
        
def meta_toggle_save(option: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"save-{option}")
    return instructions

def toggle_save(option: str) -> Union[bool, str]:
    """This function toggles the auto-save of the world
    Available options: on, off"""
    
    check_output_channel()
    
    instructions = meta_toggle_save(option)
    
    for line in instructions["list"]:
        status = post(line)
        
############# HELP #############

def meta_help(value: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"help {value}")
    return instructions

def parse_help(prepender = ""):
    
    instructions = meta_help(prepender)
    
    for line in instructions["list"]:
        data = post(line)
        
    # Remove all \x1b[.. color code from the status
    data = re.sub(r"\x1b\[[0-9;]*m", "", data)
    
    print(data)
    # Find the number of help pages
    nb_pages = re.findall(r" \(\d+/(\d+)\)", data)
    
    if nb_pages:
        nb_pages = nb_pages[0]
    elif " Help: " in data and not nb_pages:
        nb_pages = 1
    else:
        raise Exception("No help found")
        
    help_cmds = {}
    for page in range(1, int(nb_pages) + 1):
                
        instructions = meta_help(prepender + str(page))
        
        for line in instructions["list"]:
            data = post(line)
            
        data = re.sub(r"\x1b\[[0-9;]*m", "", data)
        lines = data.splitlines()[(1 if page > 1 else 2):]
        
        for line in lines:
            if not line.startswith("/") and ":" not in line:
                continue
            splitted = line.split(": ")
            command = splitted[0]
            value = splitted[1]
            help_cmds[command] = value
    
    return help_cmds

def help(value: str = "") -> Union[bool, dict]:
    """This function fetches the help of the world"""
    
    check_output_channel()

    cmds = parse_help(value)
    for key in cmds:
        if not key.startswith('/'):
            cmds[key] = parse_help(prepender=key + " ")
            
    return cmds

############# LIST #############

def meta_list_players(uuids: bool = False) -> dict:
    instructions = {"list": []}
    if uuids:
        uuids = "uuids"
    else:
        uuids = ""
    instructions["list"].append(f"list {uuids}")
    return instructions

def list_players(uuids: bool = False) -> Union[bool, str]:
    """This function fetches the list of players in the world
    If uuids is set to True it will be a list of uuids returned"""
    
    check_output_channel()
    
    instructions = meta_list_players(uuids)
    
    for line in instructions["list"]:
        status = post(line)
    
    # Remove all \x1b[.. color code from the status
    status = re.sub(r"\x1b\[[0-9;]*m", "", status)
    
    if uuids:
        players = status
    else:
        players = status.split("players online: ")[1].split(", ")
        
    return players

############# SPECTATE #############

def meta_spectate(target: str, player: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"spectate {target} {player}")
    return instructions

def spectate(target: str, player: str) -> Union[bool, str]:
    """This function makes the target spectates a player"""
    
    check_output_channel()
    
    instructions = meta_spectate(target, player)
    
    for line in instructions["list"]:
        status = post(line)
        
        
############# SET WORLD SPAWN #############

def meta_set_world_spawn(pos: Coordinates, yaw: int) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"setworldspawn {pos} {yaw}")
    return instructions

def set_world_spawn(pos: Union[Coordinates, tuple], yaw: int = 0) -> Union[bool, str]:
    """This function sets the world spawn"""
    
    check_output_channel()
    
    pos = format_arg(pos, Coordinates)

    instructions = meta_set_world_spawn(pos, yaw)
    
    for line in instructions["list"]:
        status = post(line)