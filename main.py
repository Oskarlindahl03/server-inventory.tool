import sys
import cli
from storage import load_servers
from menu import run_menu   

def main():
    args = cli.parse_args()
    servers = load_servers()

    if not cli.has_action(args):
        run_menu(servers)
        return 0
    return cli.run_args(args, servers)

if __name__ == "__main__":
    sys.exit(main())
    