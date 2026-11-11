# Server Inventory Tool

Server Inventory Tool is a command-line application for keeping a small inventory of servers. It stores server records in JSON, checks availability with `ping`, and exports CSV reports. Use the interactive menu or run an action directly from the command line.

## Requirements

- Python 3
- The `ping` command for server checks. macOS and Linux use `ping -c`; network rules may block ping requests.

The application uses only Python's standard library. `pytest` is needed only to run the tests.

## Run the application

Run commands from the project directory. Start the interactive menu with:

```sh
python3 main.py
```

The menu can show all servers or filter by environment, add and remove servers, check one or all servers, and export all servers or one server to CSV.

To see command-line options:

```sh
python3 main.py --help
```

Available command-line examples:

```sh
python3 main.py --list_all
python3 main.py --list_all --environment production
python3 main.py --check web01
python3 main.py --check_all
python3 main.py --export_all
```

Environment values are `development`, `test`, and `production`. A server check updates its status to `up` or `down` and records the check time. `--check` and `--check_all` return exit code `1` when a checked server is down; checking a server that does not exist also returns `1`. Successful checks and other successful commands return `0`.

## Data and reports

The optional `config.json` file configures the data file and report directory:

```json
{
	"data_file": "servers.json",
	"reports_directory": "reports"
}
```

The data-file setting follows this precedence order: the `DATAFILE` environment variable, then `data_file` in `config.json`, then the default `servers.json`. The report directory comes from `reports_directory` in `config.json`, or defaults to `reports` when the setting or config file is missing. Paths are relative to the project directory unless an absolute path is provided.

For example, set `DATAFILE` to override the value in `config.json` on macOS or Linux:

```sh
export DATAFILE="/path/to/my-servers.json"
python3 main.py
```

If the selected data file does not exist, the application starts with an empty inventory. New servers begin with status `unknown` and an empty last-checked value. Each record contains:

- `name`: unique server name
- `address`: hostname or IP address used by `ping`
- `environment`: `development`, `test`, or `production`
- `role`: the server's purpose
- `status`: `up`, `down`, or `unknown`
- `last_checked`: date and time of the most recent check

CSV reports are created in the configured report directory. Filenames use the format `servers_YYYY-MM-DD_HHMM.csv`. The directory is created automatically.

## Project structure

- `main.py`: loads data and starts the menu or CLI action
- `cli.py`: defines and handles command-line arguments
- `menu.py`: interactive text menu
- `storage.py`: JSON persistence, server lookup and CSV export
- `config.json`: data-file and report-directory settings
- `checks.py`: ping checks and status updates
- `presentation.py`: formatted server output
- `ask.py`: input helpers for the menu
- `servers.json`: default inventory data file
- `tests/`: automated tests
- `reports/`: generated CSV reports

## Run the tests

With `pytest` installed, run the test suite from the project directory:

```sh
python3 -m pytest -q
```
