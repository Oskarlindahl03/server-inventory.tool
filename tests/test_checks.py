import checks

def make_server():
    return {"name": "web01", "address": "example.com", "environment": "prod",
            "role": "web", "status": "unknown", "last_checked": ""}

def test_status_is_up_when_ping_succeeds(monkeypatch):
    monkeypatch.setattr(checks, "ping_server", lambda address: True)
    server = make_server()
    checks.check_server_status(server)
    assert server["status"] == "up"
    assert server["last_checked"] != ""

def test_status_is_down_when_ping_fails(monkeypatch):
    monkeypatch.setattr(checks, "ping_server", lambda address: False)
    server = make_server()
    checks.check_server_status(server)
    assert server["status"] == "down"



    
