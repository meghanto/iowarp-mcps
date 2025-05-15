import pytest
from src.server import app

@pytest.fixture
def client():
  app.config["TESTING"] = True
  with app.test_client() as client:
    yield client

"""
HDF5 tests
"""

def test_handle_hdf5(client):
  response = client.post("/mcp/callTool", json={
    "jsonrpc": "2.0",
    "method": "callTool",
    "params": {
      "tool": "hdf5_files",
      "arguments": {
        "path": "./mock_hdf5/a",
        "file_extension": "hdf5"
      }
    },
    "id": 2
  })
  
  assert response.status_code == 200 # check if server gave a response
  json_data = response.get_json()

  # check if there are results
  assert "result" in json_data 
  assert "file_results" in json_data["result"]

  # check if it returned all the files ending in hdf5
  assert "mock_3.hdf5" in json_data["result"]["file_results"] and "mock_4.hdf5" in json_data["result"]["file_results"]
  assert "mock.txt" not in json_data["result"]["file_results"] # check to ensure it doesn't list any other file types
 
# edge case test for hdf5
def test_handle_hdf5_edge(client):
  # invalid path given
  response = client.post("/mcp/callTool", json={
    "jsonrpc": "2.0",
    "method": "callTool",
    "params": {
      "tool": "hdf5_files",
      "arguments": {
        "path": "./mock_hdf5/c",
        "file_extension": "hdf5"
      }
    },
    "id": 2
  })
  
  assert response.status_code == 200
  json_data = response.get_json()
  assert "result" in json_data
  assert "file_results" in json_data["result"]
  # ensure nothing is returned if invalid path is given but doesn't break
  assert json_data["result"]["file_results"] == []

"""
Slurm tests
"""
# slurm test
def test_handle_slurm(client):
  response = client.post("/mcp/callTool", json={
    "jsonrpc": "2.0", 
    "method": "callTool", 
    "id": "5",
    "params": {
        "tool": "slurm_job_submission",
        "arguments": {
            "script_path": "run_analysis.sh",
            "cores": 5
        }
    }
})
  
  # check if there is valid response
  assert response.status_code == 200
  json_data = response.get_json()

  # check if results isn't empty
  assert "result" in json_data

  # check if subprocess ran echo and returned message
  assert "job_id" in json_data["result"] and "submission_output" in json_data["result"]
  assert "Submitted run_analysis.sh using 5 cores" in json_data["result"]["submission_output"]
  assert json_data["result"]["job_id"] is not None
 
# edge case for slurm
def test_handle_slurm_edge(client):
  # edge case, no argument is given
  response = client.post("/mcp/callTool", json={
    "jsonrpc": "2.0", 
    "method": "callTool", 
    "id": "5",
    "params": {
        "tool": "slurm_job_submission",
        "arguments": {}
    }
  })
  
  # check if there is valid response
  assert response.status_code == 200
  json_data = response.get_json()

  # check if results isn't empty
  assert "result" in json_data

  # check if subprocess ran echo and returned message
  assert "job_id" in json_data["result"] and "submission_output" in json_data["result"]

  # check to see that it runs default script and core if no parameters are given
  assert "Submitted fake_script.sh using 1 cores" in json_data["result"]["submission_output"]
  assert json_data["result"]["job_id"] is not None
 
def test_invalid_tool(client):
  # edge case, no argument is given
  response = client.post("/mcp/callTool", json={
    "jsonrpc": "2.0", 
    "method": "callTool", 
    "id": "5",
    "params": {
        "tool": "invalidTool",
        "arguments": {}
    }
  })
  
  json_data = response.get_json()
  assert "error" in json_data
  assert json_data["error"]["code"] == -32601 # ensure it returns invalid method code
  assert json_data["error"]["message"] == "Tool not found"