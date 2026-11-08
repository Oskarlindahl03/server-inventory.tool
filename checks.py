import subprocess
from datetime import datetime

def ping_server(address):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", address],
            capture_output=True,
            timeout=5,
        ) 
    except subprocess.TimeoutExpired:
        return False
    return result.returncode == 0

def check_server_status(server):
    if ping_server(server["address"]):
        server["status"] = "up"
    else:
        server["status"] = "down"
    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")

def check_all_server_status(servers):
    for server in servers:
        check_server_status(server)
