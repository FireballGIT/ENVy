import platform
import psutil
import socket

def get_os_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def get_cpu_info():
    return {
        "physical_count": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(interval=1)
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent
    }


def get_disk_info():
    disks = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except PermissionError:
            continue
    return disks

def get_hostname():
    return socket.gethostname()

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "Unknown"