from storage import is_valid_environment

def ask_environment():
    while True:
        environment = input("Environment (development/test/production): ").strip().lower()
        if is_valid_environment(environment):
            return environment
        print("Invalid environment.")

def ask_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty")