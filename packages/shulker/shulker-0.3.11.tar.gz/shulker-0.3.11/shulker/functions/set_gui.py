from typing import Union
from shulker.functions.base_functions import *

############### BOSSBAR ###############

def meta_add_bossbar(name: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"bossbar add {id} {{\"text\":\"\"}}")
    return instructions

def meta_create_bossbar(id: str, text:str, target: str, value: int, color: str, progress: str, max: int, visible: bool) -> dict:
    instructions = {"list": []}
    
    instructions["list"].append(f"bossbar set {id} value {value}")
    instructions["list"].append(f"bossbar set {id} name {{\"text\":\"{text}\"}}")
    instructions["list"].append(f"bossbar set {id} color {color}")
    instructions["list"].append(f"bossbar set {id} players {target}")
    instructions["list"].append(f"bossbar set {id} style {progress}")
    instructions["list"].append(f"bossbar set {id} max {max}")
    instructions["list"].append(f"bossbar set {id} visible {str(visible).lower()}")    
    
    return instructions

def meta_list_bossbar():
    instructions = {"list": []}
    instructions["list"].append("bossbar list")
    return instructions

def meta_remove_bossbar():
    instructions = {"list": []}
    instructions["list"].append("bossbar remove")
    return instructions

def meta_get_bossbar(id: str, option: str):
    instructions = {"list": []}
    instructions["list"].append(f"bossbar get {id} {option}")
    return instructions

def meta_set_bossbar(id: str, option: str, value: str):
    instructions = {"list": []}
    instructions["list"].append(f"bossbar set {id} {option} {value}")
    return instructions

def add_bossbar(id: str) -> Union[bool, str]:

    check_output_channel()
    
    instructions = meta_add_bossbar(id)
    
    for line in instructions["list"]:
        status = post(line)
 
def create_bossbar(
    id: str,
    text: str,
    target: Union[str, None] = "@a",
    value: int = 100,
    color: str = "white",
    style: str = "progress",
    max: int = 100,
    visible: bool = True,
) -> Union[bool, str]:
    """
    Available colors: ["pink", "blue", "red", "green", "yellow", "purple", "white"]
    If target is None, it will only add the bossbar, but not display it to anyone.
    """

    check_output_channel()
    
    if target == None:
        target = ""
    
    instructions = meta_add_bossbar(id)
    instructions2 = meta_create_bossbar(id, text, target, value, color, style, max, visible)
    instructions["list"].extend(instructions2["list"])

    for line in instructions["list"]:
        status = post(line)

def list_bossbar() -> list:
    check_output_channel()
    
    instructions = meta_list_bossbar()
    
    for line in instructions["list"]:
        status = post(line)
        
    status = status[:-4]
    
    result = []
    bossbars = status.split(": ")[1].split(", ")
    for bossbar in bossbars:
        bossbar = bossbar.replace("[", "").replace("]", "")
        result.append(bossbar)
   
    return result

def remove_bossbar(id: str) -> Union[bool, str]:
    """
    Removes the bossbar with the given id
    """

    check_output_channel()
    
    instructions = meta_remove_bossbar()
    
    for line in instructions["list"]:
        status = post(line)
        
    if status.startswith("Removed"):
        return True
    else:
        return False

def get_bossbar(id: str, option: str) -> Union[bool, int]:
    """
    Returns a the values that were asked for corresponding to the bossbar id
    'players' options returns a list
    """

    check_output_channel()
    
    instructions = meta_get_bossbar(id, option)
    
    for line in instructions["list"]:
        status = post(line)[:-4]
    
    if "players" in option:
        value = status.split(": ")[1].split(", ")
    else:
        value = status.split(" ")[-1]
        
    if "<--[HERE]" in value:
        raise ValueError(f"bossbar get cannot fetch {option}'s value")
    
    return value

def set_bossbar(id: str, option: str, value: str) -> Union[bool, str]:
    """
    Sets the value of the bossbar with the given id
    Availables options: ["value", "max", "color", "style", "players", "name", "visible"]
    """

    check_output_channel()
    
    instructions = meta_set_bossbar(id, option, value)
    
    for line in instructions["list"]:
        status = post(line)
        
    if status.startswith("Set"):
        return True
    else:
        return False

############### TITLES ###############

def meta_show_gui(type: str, text: str, target: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"title {target} {type} {{\"text\":\"{text}\"}}")
    return instructions

def meta_clear_gui(target: str) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"title {target} clear")
    return instructions

def meta_set_gui_time(target: str, fade_in: int, stay: int, fade_out: int) -> dict:
    instructions = {"list": []}
    instructions["list"].append(f"title {target} times {fade_in} {stay} {fade_out}")
    return instructions

def show_gui(type: str, text: str, target: str = "@a") -> Union[bool, str]:
    """
    Shows a title or a subtitle or an actionbar to the given target
    Available types: ["title", "subtitle", "actionbar"]
    """

    check_output_channel()
    
    instructions = meta_show_gui(type, text, target)
    
    for line in instructions["list"]:
        status = post(line)

def clear_gui(target: str = "@a") -> Union[bool, str]:

    check_output_channel()
    
    instructions = {"list": []}
    instructions["list"].append(f"title {target} {type} clear")
    
    for line in instructions["list"]:
        status = post(line)
        
def set_gui_time(target: str = "@a", fade_in: int = 10, stay: int = 70, fade_out: int = 20) -> Union[bool, str]:
    """
    Sets the time of the title, subtitle or actionbar for the target
    Providing no values defaults to default time values
    """

    check_output_channel()
    
    instructions = meta_set_gui_time(target, fade_in, stay, fade_out)
    
    for line in instructions["list"]:
        status = post(line)