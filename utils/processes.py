import psutil

def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def kill_process(pid: int):
    """
    Kill a process by PID.
    Returns True if successful, False otherwise.
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()  # Graceful first
        proc.wait(timeout=3)
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
        return False

def get_process_info(pid: int):
    """
    Return detailed info for a single process.
    """
    try:
        proc = psutil.Process(pid)
        return {
            "pid": proc.pid,
            "name": proc.name(),
            "exe": proc.exe(),
            "cmdline": proc.cmdline(),
            "username": proc.username(),
            "cpu_percent": proc.cpu_percent(interval=0.5),
            "memory_percent": proc.memory_percent(),
            "status": proc.status()
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None