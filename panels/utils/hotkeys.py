import keyboard
from typing import Callable, Dict

HOTKEYS: Dict[str, Callable] = {}

def add_hotkey(combo: str, action: Callable):
    if combo in HOTKEYS:
        remove_hotkey(combo)
    
    keyboard.add_hotkey(combo, action)
    HOTKEYS[combo] = action
    return True

def remove_hotkey(combo: str):
    if combo in HOTKEYS:
        keyboard.remove_hotkey(combo)
        del HOTKEYS[combo]
        return True
    return False

def list_hotkeys():
    return list(HOTKEYS.keys())

def clear_hotkeys():
    for combo in list(HOTKEYS.keys()):
        keyboard.remove_hotkey(combo)
    HOTKEYS.clear()