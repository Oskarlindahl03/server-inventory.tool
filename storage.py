import os
import json
import csv
from pathlib import Path
from datetime import datetime

DATAFILE = os.environ.get("DATAFILE", "servers.json")

def load_servers():
    """Load the list of servers from the JSON file."""
    if not os.path.exists(DATAFILE):
        return []
    with open(DATAFILE, "r") as f:
        return json.load(f)
    
def save_servers(servers):
    """Save the list of servers to the JSON file."""
    with open(DATAFILE, "w") as f:
        json.dump(servers, f, indent=4)

def export_csv(servers):
    """Writes the list of servers to a CSV file and returns the path."""
    if not servers:
        return "No servers to export."
    folder = Path("reports")
    folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    file_path = folder / f"servers_{timestamp}.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=servers[0].keys())
        writer.writeheader()
        writer.writerows(servers)
    return file_path




