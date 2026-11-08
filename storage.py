import os
import json
import csv
from pathlib import Path
from datetime import datetime

DATAFILE = os.environ.get("DATAFILE", "servers.json")
VALID_ENVIRONMENTS = ["production", "development", "test"]

def load_servers():
    if not os.path.exists(DATAFILE):
        return []
    with open(DATAFILE, "r") as f:
        return json.load(f)
    
def save_servers(servers):
    with open(DATAFILE, "w") as f:
        json.dump(servers, f, indent=4)

def export_csv(servers):
    if not servers:
        return None
    folder = Path("reports")
    folder.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    file_path = folder / f"servers_{timestamp}.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=servers[0].keys())
        writer.writeheader()
        writer.writerows(servers)
    return file_path

def find_server(servers, name):
    for server in servers:
        if server["name"] == name:
            return server
    return None

def find_server_or_report(servers, name):
    server = find_server(servers, name)
    if server is None:
        print(f"No server named '{name}'.")
    return server

def is_valid_environment(environment):
    return environment in VALID_ENVIRONMENTS


def add_server(servers, name, address, environment, role):
    if not name:
        raise ValueError("Server name cannot be empty.")
    if find_server(servers, name) is not None:
        raise ValueError(f"Server with name '{name}' already exists.")
    if not is_valid_environment(environment):
        raise ValueError(f"Invalid environment '{environment}'. Must be one of {VALID_ENVIRONMENTS}.")
    servers.append({
        "name": name,
        "address": address,
        "environment": environment,
        "role": role,
        "status": "unknown",
        "last_checked": "",
    })

def remove_server(servers, name):
    server = find_server(servers, name)
    if server is None:
        return False
    servers.remove(server)
    return True

def filter_servers_by_environment(servers, environment):
    return [server for server in servers if server["environment"] == environment]
