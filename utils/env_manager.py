import os
import sys

def list_env_vars():
    return dict(os.environ)

def get_env_var(key: str):
    return os.environ.get(key)

def set_env_var(key: str, value: str):
    os.environ[key] = value
    return True

def remove_env_var(key: str):
    if key in os.environ:
        del os.environ[key]
        return True
    return False