import platform
import psutil

def get_cpu_details():
  return {
    "processor": platform.processor(),
    "architecture": platform.machine(),
    "physical_cores": psutil.cpu_count(logical=False),
    "logical_cores": psutil.cpu_count(logical=True),
    "usage_percent": psutil.cpu_percent(interval=1)
  }

def get_memory_details():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent
    }
  
def get_disk_details():
    disks = []

    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "filesystem": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except PermissionError:
            continue

    return disks

def get_system_summary():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "node": platform.node()
    }
