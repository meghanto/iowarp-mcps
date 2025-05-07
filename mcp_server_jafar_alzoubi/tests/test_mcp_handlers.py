import pytest
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)

def test_list_resources():
    response = client.post("/mcp", json={"jsonrpc": "2.0", "method": "mcp/listResources", "id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert isinstance(data["result"], list)
    assert "hdf5_storage" in [r["id"] for r in data["result"]]

def test_list_tools():
    response = client.post("/mcp", json={"jsonrpc": "2.0", "method": "mcp/listTools", "id": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert isinstance(data["result"], list)
    assert "slurm_scheduler" in [t["id"] for t in data["result"]]

def test_invalid_method():
    response = client.post("/mcp", json={"jsonrpc": "2.0", "method": "invalid.method", "id": 3})
    assert response.status_code == 200
    data = response.json()
    assert data["error"]["code"] == -32601
