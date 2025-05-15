from pathlib import Path


async def handle_hdf5(params, req_id):
    path_pattern = params.get("path", "./data/*.hdf5")
    matched_files = [str(p) for p in Path().glob(path_pattern)]
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "files": matched_files,
            "context": {"type": "hdf5", "pattern": path_pattern}
        }
    }
