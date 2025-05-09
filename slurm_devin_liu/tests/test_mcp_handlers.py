import pytest
from src.server import app

@pytest.fixture
def client():
  app.config["TESTING"] = True
  with app.test_client() as client:
    yield client

"""
test if server endpoints work by testing on list resources
test to make sure listResources returns hdf5_files and slurm_job_submission as available resources
"""
def test_mcp_listResources(client):
  response = client.post("/mcp/listResources", json={
    "jsonrpc": "2.0",
    "method": "listResources",
    "params": {},
    "id": 2
  })

  assert response.status_code == 200
  json_data = response.get_json()
  assert "result" in json_data
  assert "resources" in json_data["result"]
  assert any(r["name"] == "hdf5_files" for r in json_data["result"]["resources"]) and any(r["name"] == "slurm_job_submission" for r in json_data["result"]["resources"])

# handler edge case test
def test_mcp_edge(client):
  # no method given in body
  response = client.post("/mcp/listResources", json={
    "jsonrpc": "2.0",
    "params": {},
    "id": 2
  })

  json_data = response.get_json()
  assert "error" in json_data
  assert json_data["error"]["code"] == -32600 # ensure it returns invalid json code
  assert json_data["error"]["message"] == "Invalid Request"