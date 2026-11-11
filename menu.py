from storage import filter_servers_by_environment
from storage import add_server
from storage import remove_server
from storage import find_server
from checks import check_server_status
from checks import check_all_server_status
from storage import export_csv
from presentation import print_formatted_servers
from ask import ask_environment
from ask import ask_non_empty

def menu_filter_servers_by_environment(servers):
    environment = ask_environment()
    print_formatted_servers(filter_servers_by_environment(servers, environment))

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
    print(f"Added: {name}.")

def menu_remove_server(servers):
    name = ask_non_empty("Enter name of the server you'd like to delete: ")
    server = find_server(servers, name)
    if server is None:
        return
    if server["environment"] == "production":
        answer = input(f"'{name}' is a production server. Type 'yes' to confirm: ").strip().lower()
        if answer != "yes":
            print("Cancelled deletion.")
            return
    remove_server(servers, name)
    print(f"Removed '{name}'. ")

def menu_check_server_by_name(servers):
    name = ask_non_empty("Enter name of the server you'd like to check: ")
    server = find_server(servers, name)
    if server is None:
        return
    check_server_status(server, servers)
    print_formatted_servers([server])

def menu_export_csv_by_name(servers):
    name = ask_non_empty("Enter name of the server to export: ")
    server = find_server(servers, name)
    if server is None:
        return
    export_csv([server])

def run_menu(servers):
    options = {
        "1": ("Show all servers", print_formatted_servers),
        "2": ("Show servers in an environment", menu_filter_servers_by_environment),
        "3": ("Add servers", menu_add_server),
        "4": ("Remove server by name", menu_remove_server),
        "5": ("Check server by name", menu_check_server_by_name),
        "6": ("Check all servers", check_all_server_status),
        "7": ("Export csv all servers", export_csv),
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
    
    