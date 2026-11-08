import storage
import pytest

@pytest.fixture
def servers():
    return [
        {"name": "web01", "address": "example.com", "environment": "prod",
         "role": "web", "status": "unknown", "last_checked": ""},
        {"name": "dev01", "address": "localhost", "environment": "dev",
         "role": "dev", "status": "unknown", "last_checked": ""},
    ]

def test_load_returns_empty_list_when_file_does_not_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATAFILE", str(tmp_path / "nonexistent.json"))
    assert storage.load_servers() == []

def test_save_and_load_servers(tmp_path, monkeypatch, servers):
    monkeypatch.setattr(storage, "DATAFILE", str(tmp_path / "servers.json"))
    storage.save_servers([servers[0]])
    assert storage.load_servers() == [servers[0]]

def test_export_csv_creates_file_with_header(tmp_path, monkeypatch, servers):
    monkeypatch.setattr(storage, "DATAFILE", str(tmp_path / "servers.json"))
    monkeypatch.chdir(tmp_path)
    path = storage.export_csv(servers)
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "name,address,environment,role,status,last_checked"
    assert len(lines) == 3
    

# --- is_valid_environment tests ---

def test_valid_environment_is_accepted():
    for env in storage.VALID_ENVIRONMENTS:
        assert storage.is_valid_environment(env) is True

def test_invalid_environment_is_rejected():
    assert storage.is_valid_environment("invalid_env") is False


# --- find_server tests ---

def test_find_existing_server(servers):
    server = storage.find_server(servers, "web01")
    assert server is not None
    assert server["name"] == "web01"

def test_find_nonexistent_server(servers):
    assert storage.find_server(servers, "nonexistent") is None


# --- add_server tests ---

def test_add_server_appends_with_defaults(servers):
    storage.add_server(servers, "db01", "127.0.0.1", "prod", "database")
 
    assert len(servers) == 3
    new = servers[-1]
    assert new["name"] == "db01"
    assert new["status"] == "unknown"
    assert new["last_checked"] == ""

 
def test_add_duplicate_name_raises_and_leaves_list_unchanged(servers):
    with pytest.raises(ValueError):
        storage.add_server(servers, "web01", "1.2.3.4", "prod", "webserver")
    assert len(servers) == 2
 
 
def test_add_invalid_environment_raises_and_leaves_list_unchanged(servers):
    with pytest.raises(ValueError):
        storage.add_server(servers, "new01", "1.2.3.4", "staging", "webserver")
    assert len(servers) == 2
 
 
def test_add_empty_name_raises(servers):
    with pytest.raises(ValueError):
        storage.add_server(servers, "", "1.2.3.4", "prod", "webserver")


# --- remove_server ---
 
def test_remove_existing_server(servers):
    assert storage.remove_server(servers, "web01") is True
    assert [s["name"] for s in servers] == ["dev01"]
 
 
def test_remove_missing_server_returns_false(servers):
    assert storage.remove_server(servers, "nope") is False
    assert len(servers) == 2

# --- filter_servers_by_environment ---
 
def test_filter_returns_only_matching_servers(servers):
    result = storage.filter_servers_by_environment(servers, "prod")
    assert [s["name"] for s in result] == ["web01"]
 
 
def test_filter_with_no_match_returns_empty_list(servers):
    assert storage.filter_servers_by_environment(servers, "test") == []
    