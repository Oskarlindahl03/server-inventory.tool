SERVER_COLUMNS = ["name", "address", "environment", "role", "status", "last_checked"]

def print_formatted_servers(servers):
    print("".join(f"{column.upper():<20}" for column in SERVER_COLUMNS))
    for server in servers:
        print("".join(f"{server[column]:<20}" for column in SERVER_COLUMNS))