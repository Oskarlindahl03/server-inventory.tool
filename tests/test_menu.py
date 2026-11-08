import menu

def make_server():
    return {"name": "web01", "address": "example.com", "environment": "prod",
            "role": "web", "status": "unknown", "last_checked": ""}
#--- menu ---
def feed_inputs(monkeypatch, *answers):
    answers_iter = iter(answers)
    monkeypatch.settattr("builtins.input", lambda prompt = "": next(answers_iter))

def record_servers(monkeypatch):
    saves = []
    monkeypatch.settattr(menu, "save_servers", lambda servers: saves.append(len(servers)))
    return saves

#--- check --- 
def test_check_server_updates_and_saves(monkeypatch):
    
    saves = record_saves(monkeypatch)
    monkeypatch.setattr(menu, "check_server_status",
                        lambda server: server.update(status="up"))
    feed_inputs(monkeypatch, "web01")
    servers = make_servers()
 
    menu.menu_check_server_by_name(servers)
 
    assert servers[0]["status"] == "up"
    assert saves == [2]