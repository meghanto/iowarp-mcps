# test/test_mcp_handlers.py

import sys
import os
import pathlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import pytest
from mcp_handlers import handle_mcp_request


# correct cases

def test_valid_list_resources():
    request = {
        "jsonrpc": "2.0",
        "method": "mcp/listResources",
        "params": {},
        "id": "rsc_1"
    }
    response = handle_mcp_request(request)
    print("\n[listResources OK]:", response)

    assert "result" in response
    assert isinstance(response["result"], list)
    assert len(response["result"]) >= 3


def test_valid_slurm_tool():
    request = {
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {
            "tool": "slurm",
            "params": {
                "script": "train.sh",
                "cores": 4
            }
        },
        "id": "slurm_1"
    }
    response = handle_mcp_request(request)
    print("\n[slurm OK]:", response)

    assert "result" in response
    assert response["result"]["status"] == "success"
    assert "job_id" in response["result"]


def test_valid_hdf5_tool(tmp_path):
    hdf5_dir = tmp_path / "mock_data" / "hdf5"
    hdf5_dir.mkdir(parents=True)
    (hdf5_dir / "a.hdf5").touch()
    (hdf5_dir / "b.hdf5").touch()

    pattern = str(hdf5_dir / "*.hdf5")

    request = {
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {
            "tool": "hdf5",
            "params": {
                "pattern": pattern
            }
        },
        "id": "hdf5_1"
    }
    response = handle_mcp_request(request)
    print("\n[hdf5 OK]:", response)

    assert "result" in response
    assert response["result"]["status"] == "success"
    assert len(response["result"]["matches"]) == 2


# wrong cases

def test_invalid_method_name():
    request = {
        "jsonrpc": "2.0",
        "method": "mcp/unknown",
        "params": {},
        "id": "fail_1"
    }
    response = handle_mcp_request(request)
    print("\n[method FAIL]:", response)

    assert "error" in response
    assert response["error"]["code"] == -32601


def test_invalid_slurm_missing_script():
    request = {
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {
            "tool": "slurm",
            "params": {
                # "script" is missing
                "cores": 2
            }
        },
        "id": "fail_2"
    }
    response = handle_mcp_request(request)
    print("\n[slurm param FAIL]:", response)

    assert "result" in response  # still success but using default script name
    assert response["result"]["status"] == "success"
    assert "job_id" in response["result"]


def test_invalid_hdf5_no_match():
    request = {
        "jsonrpc": "2.0",
        "method": "mcp/callTool",
        "params": {
            "tool": "hdf5",
            "params": {
                "pattern": "./nonexistent_dir/**/*.hdf5"
            }
        },
        "id": "fail_3"
    }
    response = handle_mcp_request(request)
    print("\n[hdf5 not found FAIL]:", response)

    assert "error" in response
    assert response["error"]["code"] == -32000
