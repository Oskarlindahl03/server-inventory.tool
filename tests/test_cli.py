import cli


def make_servers():
    return [
        {"name": "web01", "address": "example.com", "environment": "production", "role": "web", "status": "up", "last_checked": "2026-11-10 10:00"},
        {"name": "db01", "address": "db.example.com", "environment": "development", "role": "db", "status": "down", "last_checked": "2026-11-10 10:05"},
    ]


def test_build_parser_accepts_list_all_and_environment():
    args = cli.build_parser().parse_args(["--list_all", "--environment", "production"])

    assert args.list_all is True
    assert args.environment == "production"


def test_parse_args_rejects_environment_without_list_all(monkeypatch):
    monkeypatch.setattr("sys.argv", ["server-tool", "--environment", "production"])
    try:
        cli.parse_args()
    except SystemExit:
        return
    raise AssertionError("parse_args should reject --environment without --list_all")


def test_has_action_detects_cli_actions():
    args = cli.build_parser().parse_args(["--check_all"])
    assert cli.has_action(args) is True

    args = cli.build_parser().parse_args([])
    assert cli.has_action(args) is False


def test_run_args_list_all_returns_zero_and_prints_servers(monkeypatch, capsys):
    servers = make_servers()
    args = cli.build_parser().parse_args(["--list_all"])

    result = cli.run_args(args, servers)
    out = capsys.readouterr().out

    assert result == 0
    assert "web01" in out
    assert "db01" in out


def test_run_args_check_returns_one_for_missing_server(monkeypatch):
    servers = make_servers()
    args = cli.build_parser().parse_args(["--check", "missing-server"])

    assert cli.run_args(args, servers) == 1


def test_run_args_export_all_calls_export_csv(monkeypatch):
    servers = make_servers()
    calls = []
    monkeypatch.setattr(cli, "export_csv", lambda items: calls.append(list(items)))

    args = cli.build_parser().parse_args(["--export_all"])
    result = cli.run_args(args, servers)

    assert result == 0
    assert calls == [servers]
