import io
from contextlib import redirect_stdout

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


def test_menu_filter_servers_by_environment_uses_selected_environment(monkeypatch):
    filtered = [{"name": "web01", "environment": "production"}]
    captured = []
    monkeypatch.setattr(menu, "ask_environment", lambda: "production")
    monkeypatch.setattr(menu, "filter_servers_by_environment", lambda servers, environment: filtered)
    monkeypatch.setattr(menu, "print_formatted_servers", lambda servers: captured.append(list(servers)))

    menu.menu_filter_servers_by_environment([{"name": "web01", "environment": "production"}])

    assert captured == [filtered]


def test_menu_add_server_prints_added_message(monkeypatch):
    server_list = []
    monkeypatch.setattr(menu, "ask_non_empty", lambda prompt: {"Name:": "db01", "Adress: ": "10.0.0.2", "Role: ": "db"}[prompt])
    monkeypatch.setattr(menu, "ask_environment", lambda: "development")
    monkeypatch.setattr(menu, "add_server", lambda servers, name, address, environment, role: server_list.append({
        "name": name,
        "address": address,
        "environment": environment,
        "role": role,
    }))

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        menu.menu_add_server(server_list)

    assert server_list == [{"name": "db01", "address": "10.0.0.2", "environment": "development", "role": "db"}]
    assert "Added: db01." in buffer.getvalue()


def test_menu_add_server_handles_value_error(monkeypatch):
    monkeypatch.setattr(menu, "ask_non_empty", lambda prompt: {"Name:": "bad", "Adress: ": "10.0.0.3", "Role: ": "api"}[prompt])
    monkeypatch.setattr(menu, "ask_environment", lambda: "production")
    monkeypatch.setattr(menu, "add_server", lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("bad name")))

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        menu.menu_add_server([])

    assert "bad name" in buffer.getvalue()


def test_menu_check_server_by_name_checks_selected_server(monkeypatch):
    server = make_server()
    called = []
    monkeypatch.setattr(menu, "ask_non_empty", lambda prompt: "web01")
    monkeypatch.setattr(menu, "find_server", lambda servers, name: server)
    monkeypatch.setattr(menu, "check_server_status", lambda item, items: called.append((item, list(items))))
    monkeypatch.setattr(menu, "print_formatted_servers", lambda items: called.append(items))

    menu.menu_check_server_by_name([server])

    assert called[0][0] == server
    assert called[1] == [server]


def test_menu_remove_server_cancels_for_production_server(monkeypatch):
    server = {"name": "web01", "address": "example.com", "environment": "production", "role": "web", "status": "up", "last_checked": "2026-11-10 10:00"}
    responses = iter(["web01", "no"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))
    monkeypatch.setattr(menu, "find_server", lambda servers, name: server)

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        menu.menu_remove_server([server])

    assert "Cancelled deletion." in buffer.getvalue()
    assert [item["name"] for item in [server]] == ["web01"]


def test_menu_export_csv_by_name_exports_selected_server(monkeypatch):
    server = make_server()
    exported = []
    monkeypatch.setattr(menu, "ask_non_empty", lambda prompt: "web01")
    monkeypatch.setattr(menu, "find_server", lambda servers, name: server)
    monkeypatch.setattr(menu, "export_csv", lambda items: exported.append(list(items)))

    menu.menu_export_csv_by_name([server])

    assert exported == [[server]]