import socket
import subprocess
import platform
import psutil

def get_hostname():
  return socket.gethostname()

def get_local_ip():
  try:
    return socket.gethostbyname(socket.gethostname())
  except:
    return "Unknown"

def list_interface():
  interfaces = {}
  addrs = psutil.net_if_addrs()
  for iface, addr_list in addrs.items():
    for addr in addr_list:
      if addr.family_name == 'AF_INET':
        interfaces[iface] = addr.address
  return interfaces

def ping(host: str, count: int = 4):
  param "-n" if platform.system().lower() == "windows" else "-c"
  try:
    result = subprocess.run(
      ["ping", param, str(count), host],
      capture_output=True,
      text=True
    )
    return result.stdout
  except Exception as e:
    return f"Ping failed: {e}"

def disconnect_interface(interface: str):
    if platform.system().lower() != "windows":
        return "Unsupported OS"

    try:
        subprocess.run(
            ["netsh", "interface", "set", "interface", interface, "admin=disable"],
            capture_output=True
        )
        return f"{interface} disabled."
    except Exception as e:
        return f"Failed to disable {interface}: {e}"
