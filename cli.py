import argparse
import sys
from storage import filter_servers_by_environment, find_server
from checks import check_all_server_status
from checks import check_server_status
from presentation import print_formatted_servers
from storage import export_csv

def build_parser():
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--verbose', '-v', action='store_true', help='Gives more detailed information')

    parser = argparse.ArgumentParser(
        prog = 'server-inventorytool',
        parents = [parent],
    )

    parser.add_argument(
        '--list_all',
        '-l',
        help = "Show all servers",
        action = 'store_true'
    )

    parser.add_argument(
        '--environment',
        '-env',
        help = "Show servers with a specific environment",
        choices = ["development", "test", "production"],
        const="",
        metavar="NAME",
        nargs="?"
    )

    parser.add_argument(
        '--check_all',
        '-ca',
        help = "Check status for all servers", 
        action="store_true"
    )

    parser.add_argument(
        "--check",
        '-cs',
        help="Check status for one specific server",
        metavar="NAME"
    )

    parser.add_argument(
        '--export_all',
        '-e',
        help='Export all servers to csv',
        action='store_true'
    )
    return parser

def parse_args():
    parser = build_parser()
    args = parser.parse_args()
    if args.environment and not args.list_all:
        parser.error("--environment requires --list-all")
    return args

def has_action(args):
    return any([args.list_all, args.check, args.check_all, args.export_all])


def run_args(args, servers):
    if args.list_all and not args.environment:
        print_formatted_servers(servers)
        return 0

    if args.list_all and args.environment:    
        targets = filter_servers_by_environment(servers, args.environment)
        print_formatted_servers(targets)
        return 0

    if args.check_all:
        check_all_server_status(servers)
        print_formatted_servers(servers)
        return 1 if any(server["status"] == "down" for server in servers) else 0

    if args.check:
        server = find_server(servers, args.check)
        if server is None:
            return 1
        check_server_status(server, servers)
        print_formatted_servers([server])
        return 1 if server["status"] == "down" else 0

    if args.export_all:
        export_csv(servers)
        return 0






