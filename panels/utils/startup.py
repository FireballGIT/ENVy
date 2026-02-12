import os
import sys

if sys.platform == "win32":
  import winreg

def list_startup_programs():
  if sys.platform != "win32":
    return {}

  programs = {}
  try:
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
      for i in range(0, winreg.QueryInfoKey(key)[1]):
        name, value, _ = winreg.EnumValue(key, i)
        programs[name] = value
  
  except Exception as e:
    programs["Error"] = str(e)

  return programs

def add_startup_program(name: str, exe_path: str):
  if sys.platform != "win32":
    return False, "Unsupported OS"

  try:
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
      winreg.SetValueEx(key, name, 0, winreg.REG_SZ, exe_path)
    return True, f"Added {name} to startup"
  except Exception as e:
    return False, f"Failed to add startup program: {e}"
