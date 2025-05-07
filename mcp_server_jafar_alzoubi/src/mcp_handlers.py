import uuid
import subprocess
import os
import glob  
from fastapi import APIRouter
from typing import Dict, Any
from pathlib import Path
from .models import JSONRPCResponse

MOCK_DATA_DIR = "mock_hdf5_data"  # Mock directory for storing .h5 files

router = APIRouter()


@router.post("/listResources")
async def list_resources():
    # Mocked response for the example
    return {
        "jsonrpc": "2.0",
        "result": ["resource1", "resource2", "resource3"],
        "id": 1
    }

@router.post("/callTool")
async def call_tool(params: dict):
    tool_name = params.get("tool_name")
    script_path = params.get("script_path")
    core_count = params.get("core_count")
    # Mocked response for the example
    return {
        "jsonrpc": "2.0",
        "result": f"Job submitted to {tool_name} with script {script_path} on {core_count} cores",
        "id": 2
    }

@router.post("/jsonrpc")
async def json_rpc(request: dict):
    return await handle_request(request)

# Handle incoming JSON RPC request
async def handle_request(params: Dict[str, Any]):
    required_params = ["action"]
    if not all(p in params for p in required_params):
        return JSONRPCResponse(
            error={"code": -32602, "message": "Action parameter required"}
        ).dict()
    
    action = params["action"]
    
    try:
        if action == "list":
            return await _handle_list(params)
        elif action == "read":
            return await _handle_read(params)
        elif action == "metadata":
            return await _handle_metadata(params)
        elif action == "submitJob":
            return await _handle_job_submission(params)
        else:
            return JSONRPCResponse(
                error={"code": -32602, "message": "Invalid action"}
            ).dict()
    except Exception as e:
        return JSONRPCResponse(
            error={"code": -32000, "message": str(e)}
        ).dict()

# Handle listing files based on pattern and path
async def _handle_list(params: Dict[str, Any]):
    path = params.get("path", "")
    pattern = params.get("pattern", "*.h5")
    
    # Create mock directory structure if it doesn't exist
    os.makedirs(MOCK_DATA_DIR, exist_ok=True)
    mock_files = [
        "simulation_run_123.h5",
        "experiment_data_456.h5",
        "results/analysis_output.h5"
    ]
    for f in mock_files:
        Path(os.path.join(MOCK_DATA_DIR, f)).touch()  # Create mock files
    
    # Find matching files
    search_path = os.path.join(MOCK_DATA_DIR, path, pattern)
    files = glob.glob(search_path)
    
    return {
        "files": [os.path.relpath(f, MOCK_DATA_DIR) for f in files],
        "count": len(files),
        "metadata": {
            "searchPath": search_path,
            "pattern": pattern
        }
    }

# Handle reading a specific dataset from an HDF5 file (mocked)
async def _handle_read(params: Dict[str, Any]):
    file_path = params.get("filePath")
    dataset = params.get("dataset")
    
    if not file_path or not dataset:
        raise ValueError("Both filePath and dataset parameters are required")
    
    full_path = os.path.join(MOCK_DATA_DIR, file_path)
    
    # Simulate reading from an HDF5 file
    return {
        "dataset": dataset,
        "data": {
            "shape": [100, 100],
            "dtype": "float32",
            "sample_values": [0.1, 0.5, 0.9]
        },
        "metadata": {
            "units": "Kelvin",
            "description": "Simulated temperature data",
            "file": file_path
        }
    }

# Handle metadata for a specific file
async def _handle_metadata(params: Dict[str, Any]):
    file_path = params.get("filePath")
    if not file_path:
        raise ValueError("filePath parameter is required")
    
    return {
        "file": file_path,
        "metadata": {
            "format": "HDF5",
            "version": "1.10",
            "created": "2023-01-01T00:00:00Z",
            "size": "1.2GB"
        }
    }

# Handle job submission request
async def _handle_job_submission(params: Dict[str, Any]):
    required_params = ["script", "cores"]
    if not all(p in params for p in required_params):
        return JSONRPCResponse(
            error={"code": -32602, "message": f"Required parameters: {', '.join(required_params)}"}
        ).dict()
    
    try:
        script_path = params["script"]
        cores = params["cores"]
        memory = params.get("memory", "4GB")
        job_name = params.get("jobName", "mcp_job")
        
        # Validate inputs
        if not os.path.exists(script_path):
            raise ValueError(f"Script file not found: {script_path}")
        if not isinstance(cores, int) or cores < 1:
            raise ValueError("Cores must be a positive integer")
        
        # Simulate job submission
        job_id = str(uuid.uuid4())
        mock_command = [
            "sbatch",
            f"--job-name={job_name}",
            f"--ntasks={cores}",
            f"--mem={memory}",
            script_path
        ]
        
        # Simulate job submission (mock)
        # result = subprocess.run(mock_command, capture_output=True, text=True)
        
        return {
            "jobId": job_id,
            "status": "PENDING",
            "command": " ".join(mock_command),
            "submissionTime": "2023-01-01T12:00:00Z",
            "metadata": {
                "estimatedStart": "2023-01-01T12:05:00Z",
                "queue": "normal",
                "allocatedNodes": []
            }
        }
    except Exception as e:
        return JSONRPCResponse(
            error={"code": -32000, "message": str(e)}
        ).dict()
