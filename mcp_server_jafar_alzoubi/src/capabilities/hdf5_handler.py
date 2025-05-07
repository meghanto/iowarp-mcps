import os
import glob
from typing import Dict, Any
from pathlib import Path
from ..models import JSONRPCResponse

MOCK_DATA_DIR = Path("mock_hdf5_data")

async def handle_request(params: Dict[str, Any]) -> Dict[str, Any]:
    if "action" not in params:
        return JSONRPCResponse(
            error={"code": -32602, "message": "Missing 'action' parameter"}
        ).dict()

    action = params["action"]

    try:
        if action == "list":
            return await _handle_list(params)
        elif action == "read":
            return await _handle_read(params)
        elif action == "metadata":
            return await _handle_metadata(params)
        else:
            return JSONRPCResponse(
                error={"code": -32601, "message": f"Unknown action: {action}"}
            ).dict()
    except Exception as e:
        return JSONRPCResponse(
            error={"code": -32000, "message": str(e)}
        ).dict()

async def _handle_list(params: Dict[str, Any]) -> Dict[str, Any]:
    pattern = params.get("pattern", "*.h5")
    subdir = params.get("path", "")
    search_path = MOCK_DATA_DIR / subdir

    # Ensure mock directory exists
    MOCK_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create mock files if missing
    mock_files = [
        MOCK_DATA_DIR / "simulation_run_123.h5",
        MOCK_DATA_DIR / "experiment_data_456.h5",
        MOCK_DATA_DIR / "results" / "analysis_output.h5"
    ]
    for file_path in mock_files:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)

    # Perform glob search
    full_pattern = str(search_path / pattern)
    matched_files = glob.glob(full_pattern, recursive=True)

    relative_files = [
        str(Path(f).relative_to(MOCK_DATA_DIR)) for f in matched_files
    ]

    return {
        "files": relative_files,
        "count": len(relative_files),
        "context": {
            "path": subdir,
            "pattern": pattern,
            "searchPath": full_pattern
        }
    }

async def _handle_read(params: Dict[str, Any]) -> Dict[str, Any]:
    file_path = params.get("filePath")
    dataset = params.get("dataset")

    if not file_path or not dataset:
        raise ValueError("Both 'filePath' and 'dataset' are required.")

    # Full path resolution
    full_path = MOCK_DATA_DIR / file_path

    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Simulated HDF5 read
    return {
        "dataset": dataset,
        "data": {
            "shape": [100, 100],
            "dtype": "float32",
            "sampleValues": [0.1, 0.5, 0.9]
        },
        "context": {
            "file": file_path,
            "units": "Kelvin",
            "description": "Simulated temperature data"
        }
    }

async def _handle_metadata(params: Dict[str, Any]) -> Dict[str, Any]:
    file_path = params.get("filePath")
    if not file_path:
        raise ValueError("Missing 'filePath' parameter.")

    full_path = MOCK_DATA_DIR / file_path
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Simulated metadata
    return {
        "file": file_path,
        "metadata": {
            "format": "HDF5",
            "version": "1.10",
            "created": "2023-01-01T00:00:00Z",
            "size": "1.2GB"
        }
    }
