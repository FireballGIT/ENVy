import os
from datetime import datetime
from config import LOG_DIR

LOG_FILE = os.path.join(LOG_DIR, "envy.log")

def write_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%D %H:%M:%S")
    line = f"[{timestamp}] {message}"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def read_logs():
    if not os.path.exists(LOG_FILE):
        return ""
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()

def clear_logs():
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
        return True
    return False