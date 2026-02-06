APP_NAME = "ENVy"
APP_VERSION = "0.1.0"

THEME = {
    "background": "#1e1e1e",
    "sidebar": "#252525",
    "panel": "#2c2c2c",
    "text": "#3AFF99",
    "accent": "#3AFF99"
}

DEFAULT_SETTINGS = {
    "accent_colour": "#3AFF99",
    "dark_mode": True,
    "start_on_boot": False,
    "logs_enabled": True
}

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(DATA_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)