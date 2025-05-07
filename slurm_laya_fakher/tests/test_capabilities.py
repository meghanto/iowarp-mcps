from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)


def test_hdf5_tool():
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {"tool": "hdf5", "path": "./data/*.hdf5"},
        "id": 3
    })
    assert response.status_code == 200
    assert "files" in response.json()["result"]


def test_slurm_tool():
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {"tool": "slurm", "script": "run.sh", "cores": 4},
        "id": 4
    })
    assert response.status_code == 200
    assert "job_id" in response.json()["result"]


def test_arxiv_valid_query():
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {"tool": "arxiv", "query": "cs.AI", "max_results": 2},
        "id": 8
    })
    assert response.status_code == 200
    assert "papers" in response.json()["result"]


def test_arxiv_invalid_query():
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {"tool": "arxiv", "query": ""},
        "id": 9
    })
    assert response.status_code == 200
    assert "papers" in response.json()["result"] or "error" in response.json()


def test_compression_invalid_path():
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {"tool": "compression", "filename": "nonexistent_file.txt"},
        "id": 10
    })
    assert response.status_code == 200
    assert "error" in response.json()


def test_compression_valid_file(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Hello MCP!")

    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {"tool": "compression", "filename": str(test_file)},
        "id": 11
    })
    assert response.status_code == 200
    assert "File compressed" in response.json()["result"]["message"]


def test_plot_valid_csv(tmp_path):
    # Create a small CSV file
    test_csv = tmp_path / "test_data.csv"
    test_csv.write_text("A,B\n1,2\n2,4\n3,6")

    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {
            "tool": "plot",
            "filename": str(test_csv),
            "x_column": "A",
            "y_column": "B"
        },
        "id": 7
    })
    assert response.status_code == 200
    assert "Plot saved" in response.json()["result"]["message"]
