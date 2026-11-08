import os

from storage import is_valid_environment
from storage import load_servers
from storage import filter_servers_by_environment
from storage import add_server
from storage import save_servers
from storage import remove_server
from storage import find_server_or_report
from checks import check_server_status
from checks import check_all_server_status
from storage import export_csv


SERVER_COLUMNS = ["name", "address", "environment", "role", "status", "last_checked"]

def print_all_servers(servers):
    if not servers:
        print("No servers found.")
        return
    print("".join(f"{column.upper():<20}" for column in SERVER_COLUMNS))
    for server in servers:
        print("".join(f"{server[column]:<20}" for column in SERVER_COLUMNS))
    

def menu_show_all(servers):
    print_all_servers(servers)

def ask_environment():
    while True:
        environment = input("Environment (development/test/production): ").strip().lower()
        if is_valid_environment(environment):
            return environment
        print("Invalid environment.")

def menu_filter_servers_by_environment(servers):
    environment = ask_environment()
    print_all_servers(filter_servers_by_environment(servers, environment))

def ask_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty")

def menu_add_server(servers):
    name = ask_non_empty("Name:" )
    address = ask_non_empty("Adress: ")
    environment = ask_environment()
    role = ask_non_empty("Role: ")

    try:
        add_server(servers, name, address, environment, role)
    except ValueError as error:
        print(error)
        return

    save_servers(servers)

    print(f"Added: {name}.")

def menu_remove_server(servers):
    name = ask_non_empty("Enter name of the server you'd like to delete: ")
    server = find_server_or_report(servers, name)
    if server is None:
        return

    if server["environment"] == "production":
        answer = input(f"'{name}' is a production server. Type 'yes' to confirm: ").strip().lower()
    if answer != "yes":
        print("Cancelled deletion.")
        return

    remove_server(servers, name)
    save_servers(servers)
    print(f"Removed '{name}'. ")

def menu_check_server_by_name(servers):
    name = ask_non_empty("Enter name of the server you'd like to check: ")
    server = find_server_or_report(servers, name)
    if server is None:
        return None
    check_server_status(server)
    save_servers(servers)
    print_all_servers([server])

def menu_check_servers(servers):
    if servers is None:
        return
    check_all_server_status(servers)
    save_servers(servers)
    print_all_servers(servers)

def menu_export_csv_all_servers(servers):
    if servers is None:
        return
    path = export_csv(servers)
    print(f"Exported to: {os.path.dirname(path)}")

def menu_export_csv_by_name(servers):
    name = ask_non_empty("Enter name of the server you'd like to export: ")
    server = find_server_or_report(servers, name)
    if server is None:
        return
    path = export_csv([server])
    print(f"Exported to: {os.path.dirname(path)}")

    

def run_menu():
    servers = load_servers()

    options = {
        "1": ("Show all servers", menu_show_all),
        "2": ("Show servers in an environment", menu_filter_servers_by_environment),
        "3": ("Add servers", menu_add_server),
        "4": ("Remove server by name", menu_remove_server),
        "5": ("Check server by name", menu_check_server_by_name),
        "6": ("Check all servers", menu_check_servers),
        "7": ("Export csv all servers", menu_export_csv_all_servers),
        "8": ("Export csv by name", menu_export_csv_by_name)
    }

    while True:
        print("\n ==== Server inventory ====")
        for key, (text, _) in options.items():
            print(f"{key}, {text}")
        print("0. Exit")

        choice = input("choice:" ).strip()

        if choice == "0":
            break
        if choice in options:
            options[choice][1](servers)
        else:
            print("invalid choice. Try again")
    
    