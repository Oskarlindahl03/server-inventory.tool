import os
import json
import csv
from pathlib import Path
from datetime import datetime

CONFIG_FILE = Path("config.json")
VALID_ENVIRONMENTS = ["production", "development", "test"]

def load_config(config_path=CONFIG_FILE):
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)

def get_datafile(config):
    return os.environ.get("DATAFILE", config.get("data_file", "servers.json"))

def get_report_directory(config):
    return Path(config.get("reports_directory", "reports"))

CONFIG = load_config()
DATAFILE = get_datafile(CONFIG)
REPORT_DIRECTORY = get_report_directory(CONFIG)

def load_servers():
    if not os.path.exists(DATAFILE):
        return []
    with open(DATAFILE, "r") as f:
        return json.load(f)
    
def save_servers(servers):
    with open(DATAFILE, "w", encoding="utf-8") as f:
        json.dump(servers, f, indent=4, ensure_ascii=False)

def export_csv(servers):
    if servers is None:
        return None
    fieldnames = servers[0].keys() if servers else [
        "name", "address", "environment", "role", "status", "last_checked"
    ]
    folder = REPORT_DIRECTORY
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    file_path = folder / f"servers_{timestamp}.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(servers)
    print(f"Exported to: {os.path.dirname(file_path)}")
    return file_path

def find_server(servers, name):
    for server in servers:
        if server["name"] == name:
            return server
    print(f"Server '{name}' doesn't exist.")
    return None

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
    save_servers(servers)

def remove_server(servers, name):
    server = find_server(servers, name)
    if server is None:
        return False
    servers.remove(server)
    save_servers(servers)
    return True

def filter_servers_by_environment(servers, environment):
    return [server for server in servers if server["environment"] == environment]

