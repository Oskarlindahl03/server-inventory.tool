import checks

def make_server():
    return {"name": "web01", "address": "example.com", "environment": "prod",
            "role": "web", "status": "unknown", "last_checked": ""}

def test_status_is_up_when_ping_succeeds(monkeypatch):
    monkeypatch.setattr(checks, "ping_server", lambda address: True)
    monkeypatch.setattr(checks, "save_servers", lambda servers: None)
    server = make_server()
    checks.check_server_status(server, [server])
    assert server["status"] == "up"
    assert server["last_checked"] != ""

def test_status_is_down_when_ping_fails(monkeypatch):
    monkeypatch.setattr(checks, "ping_server", lambda address: False)
    monkeypatch.setattr(checks, "save_servers", lambda servers: None)
    server = make_server()
    checks.check_server_status(server, [server])
    assert server["status"] == "down"
    assert server["last_checked"] != ""


def test_ping_server_returns_false_when_subprocess_returns_non_zero(monkeypatch):
    class Result:
        returncode = 1

    monkeypatch.setattr(checks.subprocess, "run", lambda *args, **kwargs: Result())
    assert checks.ping_server("example.com") is False


def test_check_server_status_calls_save_servers_with_servers_list(monkeypatch):
    server = make_server()
    saved = []
    monkeypatch.setattr(checks, "ping_server", lambda address: True)
    monkeypatch.setattr(checks, "save_servers", lambda servers: saved.append(list(servers)))

    checks.check_server_status(server, [server])

    assert saved == [[server]]
    assert server["status"] == "up"
