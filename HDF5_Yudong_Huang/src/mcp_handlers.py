# src/mcp_handlers.py

from typing import Dict, Any
import subprocess
import random
import pathlib
import os

def handle_mcp_request(data: Dict[str, Any]) -> Dict[str, Any]:
    response = {
        "jsonrpc": "2.0",
        "id": data.get("id")
    }

    if data.get("jsonrpc") != "2.0":
        response["error"] = _make_error(-32600, "Invalid JSON-RPC version")
        return response

    method = data.get("method")
    params = data.get("params", {})

    if method == "mcp/listResources":
        response["result"] = handle_list_resources()
    elif method == "mcp/callTool":
        try:
            response["result"] = handle_call_tool(params)
        except Exception as e:
            response["error"] = _make_error(-32000, f"Tool error: {str(e)}")
    else:
        response["error"] = _make_error(-32601, f"Method '{method}' not found")

    return response


def handle_list_resources() -> list:
    return [
        {
            "name": "SimHDF5Files",
            "type": "filesystem",
            "path": "./mock_data/hdf5"
        },
        {
            "name": "MockArxivFetcher",
            "type": "external-api",
            "endpoint": "arxiv.org"
        },
        {
            "name": "CompressionUtility",
            "type": "tool",
            "description": "Simulates compressing log files using gzip"
        },
        {
            "name": "ParallelFSProjectDir",
            "type": "parallel-fs",
            "path": "/pfs/project_x"
        }
    ]



def handle_call_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    tool_name = params.get("tool")
    tool_params = params.get("params", {})

    if tool_name == "slurm":
        return _simulate_slurm_tool(tool_params)
    elif tool_name == "hdf5":
        return _simulate_hdf5_tool(tool_params)
    else:
        raise ValueError(f"Unsupported tool '{tool_name}'")


def _simulate_slurm_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates Slurm job submission.
    Example parameters:
      { "script": "run.sh", "cores": 4 }
    """
    script = params.get("script", "unnamed.sh")
    cores = params.get("cores", 1)

    # Simulate printed message and generate fake job_id
    job_id = random.randint(10000, 99999)
    message = f"Job '{script}' submitted using {cores} core(s)."
    print(f"[Slurm] {message} -> Job ID: {job_id}")

    return {
        "status": "success",
        "job_id": job_id,
        "message": message
    }


def _simulate_hdf5_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates searching for HDF5 file paths.
    Example parameters:
      { "pattern": "./mock_data/hdf5/**/*.hdf5" }
    """
    pattern = params.get("pattern")
    if not pattern:
        raise ValueError("Missing 'pattern' in hdf5 params")

    # Split the path into base directory and glob pattern
    pattern_path = pathlib.Path(pattern)
    parts = pattern_path.parts

    # Find the first part containing a wildcard
    for i, part in enumerate(parts):
        if "*" in part or "?" in part:
            base_dir = pathlib.Path(*parts[:i])
            glob_pattern = str(pathlib.Path(*parts[i:]))
            break
    else:
        # No wildcard found, raise error
        raise ValueError("Pattern must contain a glob expression like *.hdf5")

    base_dir = base_dir.resolve()
    if not base_dir.exists():
        raise ValueError(f"Base path does not exist: {base_dir}")

    matched_files = [str(p.resolve()) for p in base_dir.glob(glob_pattern)]

    print(f"[HDF5] Matching from '{base_dir}' with pattern '{glob_pattern}': {len(matched_files)} file(s)")

    return {
        "status": "success",
        "pattern": pattern,
        "matches": matched_files
    }



def _make_error(code: int, message: str) -> Dict[str, Any]:
    return {
        "code": code,
        "message": message
    }
