# mcp-server

By: Zack Chaffee A20478873

A server implementing Model Coupling Protocol (MCP) capabilities for HDF5 file operations and Slurm job management.

## Features

### HDF5 file operations:
  - Read datasets
  - List file contents

### Slurm job management:
  - Submit jobs
  - Check job status

### Node Hardware Operations
- Get CPU information
- Get memory information
- Get disk information
- Get comprehensive system information

### Compression Operations
- Compress string data with gzip or zlib
- Compress files with gzip or zlib
- Decompress data

# Initialization

Once you clone this reponsitory cd into it 

After this hwe will create a virtual enviornment and install all dependincies:
```
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
uv pip install -e ".[test]"
```

# Running

To startup the server run:
```
python -m src.server
```

This will autoclocate the server at http://localhost:8000.

## Endpoints
- `POST /mcp`: Main endpoint for MCP requests
- `GET /health`: Health check endpoint

## Examples:
```python
import httpx

async with httpx.AsyncClient() as client:
    # Read a dataset
    response = await client.post("http://localhost:8000/mcp", json={
        "capability": "hdf5",
        "action": "read_dataset",
        "parameters": {
            "file_path": "/path/to/data.h5",
            "dataset_path": "/path/to/dataset"
        }
    })
    
    # List contents
    response = await client.post("http://localhost:8000/mcp", json={
        "capability": "hdf5",
        "action": "list_contents",
        "parameters": {
            "file_path": "/path/to/data.h5",
            "group_path": "/"
        }
    })
```

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "mcp/listTools", 
    "params": {}, 
    "id": "1"
  }'
```

# Testing
For testing rung: 
```
pytest
```

For tests with coverage:
```
pytest --cov=src
```
