import storage

SERVER = {"namn": "web01", "adress": "example.com", "miljo": "prod",
          "roll": "webbserver", "status": "unknown", "senast_kontrollerad": ""}

def test_load_returns_empty_list_when_file_does_not_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATAFILE", str(tmp_path / "nonexistent.json"))
    assert storage.load_servers() == []
def test_save_and_load_servers(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATAFILE", str(tmp_path / "servers.json"))
    storage.save_servers([SERVER])
    assert storage.load_servers() == [SERVER]
def test_export_csv_creates_file_with_header(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATAFILE", str(tmp_path / "servers.json"))
    storage.save_servers([SERVER])
    servers = storage.load_servers()
    csv_path = storage.export_csv(servers)
    assert csv_path.exists()
    with open(csv_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "namn,adress,miljo,roll,status,senast_kontrollerad" in content