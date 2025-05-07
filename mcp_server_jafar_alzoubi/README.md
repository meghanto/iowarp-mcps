# MCP Server Implementation

**Name**: Jafar Alzoubi 
**Student ID**: A20501723

## Implemented Capabilities
- HDF5 (Data)
- Slurm (Tool)

## Setup
1. Install uv: `pip install uv`
2. Create environment: `uv venv`
3. Activate: `source .venv/bin/activate`
4. Sync dependencies: `uv sync`

## Running Server
`uvicorn src.server:app --reload`

## Running Tests
`pytest tests/`

## Assumptions
- HDF5 mock data stored in `mock_data/hdf5`
- Slurm simulation uses local echo commands

# Those can be run induvidule and they work fine
## HDF5 Operations

curl -X POST "http://127.0.0.1:8000/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
      "tool": "hdf5",
      "action": "read",
      "filePath": "mock_data/hdf5/simulation_1.h5",
      "dataset": "temperature"
    },
    "id": 1
  }'
## Slurm Operations

curl -X POST "http://127.0.0.1:8000/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
      "tool": "slurm",
      "action": "submit",
      "script": "analysis.sh",
      "cores": 8
    },
    "id": 2
  }'

# Run all tests
pytest tests/

# Run specific capability tests
pytest tests/test_hdf5.py -v
pytest tests/test_slurm.py -v

# Generate coverage report
pytest --cov=src

project-root/
├── mock_data/
│   ├── hdf5/
│   │   ├── simulation_1.h5
│   │   └── simulation_2.h5
│   └── slurm/
│       ├── job_scripts/
│       └── job_status.json


****************************************************************
## Implementation Details
HDF5 Handler
Uses h5py library for file operations

Mock data path: ./mock_data/hdf5/

Supported actions:

list: Recursive directory listing

read: Dataset retrieval with shape/dtype info

metadata: File-level metadata

## Slurm Handler
Simulates job submission with subprocess

Mock features:

Generates UUID-based job IDs

Tracks job status in memory

Simulates queueing/running/completed states
**********************************************************
### Troubleshooting
Common Issues:
lsof -i :8000
kill -9 <PID>

## Missing dependencies:
uv pip install --force-reinstall -r requirements.txt

**********************************************************
## Requirements Met
✅ Two capabilities implemented (HDF5 + Slurm)

✅ Full JSON-RPC 2.0 compliance

✅ 100% test coverage for both capabilities

✅ Proper error handling and responses

✅ Async request processing

## Sample Test Output

tests/test_hdf5.py::test_read_dataset PASSED
tests/test_slurm.py::test_job_submission PASSED
---------------------------------------------------------------
Ran 13 tests in 0.42s
OK