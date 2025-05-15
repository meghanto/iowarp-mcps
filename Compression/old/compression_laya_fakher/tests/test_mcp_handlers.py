from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)


def test_list_resources():
    response = client.post("/mcp", json={"jsonrpc": "2.0", "method": "mcp/listResources", "id": 1})
    assert response.status_code == 200
    resources = response.json()["result"]
    assert any(r["name"] == "hdf5" for r in resources)


def test_invalid_method():
    response = client.post("/mcp", json={"jsonrpc": "2.0", "method": "mcp/unknown", "id": 2})
    assert response.status_code == 200
    assert "error" in response.json()


def test_list_tools():
    response = client.post("/mcp", json={"jsonrpc": "2.0", "method": "mcp/listTools", "id": 12})
    assert response.status_code == 200
    tools = response.json()["result"]
    assert isinstance(tools, list)
    assert any(t["name"] == "slurm" for t in tools)
