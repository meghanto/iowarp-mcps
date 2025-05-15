
# Scientific MCP Server

##  Project Description

This project implements a **Scientific Model Context Protocol (MCP) Server** using **FastAPI** and **JSON-RPC 2.0**. The server simulates various scientific computing capabilities and allows AI agents to interact with tools and data sources in a standardized way.


##  Implemented MCP Capabilities

The following capabilities have been implemented:

| Capability    | Type     | Description                                                              |
|---------------|----------|--------------------------------------------------------------------------|
| `plot`        | Tool     | Uses `pandas` and `matplotlib` to generate a plot from a local CSV file. |



## Setup Instructions (Using `uv`)


1. Create a virtual environment with `uv`:
   ```bash
   uv venv
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. (Optional) Generate a lockfile:
   ```bash
   uv lock
   ```
   

## How to Run the MCP Server
1. **Activate your virtual environment**:

```bash
.venv\Scripts\activate     #On Windows
source .venv/bin/activate  #On macOS/Linux
```
2. **Start the server using uvicorn**:
```
uvicorn src.server:app --reload
```
The MCP server will start on:
```
http://localhost:8000/mcp
```

You can send JSON-RPC POST requests to this endpoint using Postman, curl, or test clients.


## How to Run the Tests

1. **Activate the virtual environment**(created using `uv venv`):

```bash
.venv\Scripts\activate     #On Windows
source .venv/bin/activate  #On macOS/Linux
```

2. **Run all tests using `pytest`**:

```bash
pytest
```



## Additional MCP Methods (Bonus)

In addition to the required `mcp/listResources` and `mcp/callTool`, the following optional methods are implemented:

| Method              | Description                                 |
|---------------------|---------------------------------------------|
| `mcp/listTools`     | Lists tool-oriented capabilities only       |
| `mcp/listDataSources` | Lists data-oriented capabilities only    |

These are accessible via the same `/mcp` endpoint using the standard JSON-RPC 2.0 structure.

## Bonus Features Implemented (+10 Points)

The following bonus features are implemented as mentioned in the assignment:

- Implemented MCP capabilities  
    - `plot` (tool)

- Implemented robust error handling using JSON-RPC 2.0 error format  
  -  Standardized error codes:
    - `-32601` : method/tool not found
    - `-32602` : invalid or missing parameters
    - `-32000/-32001` : general internal errors

- Asynchronous logic in all capability handlers  
  - All capability functions are defined using `async def`
  - `plot` simulates async I/O with `await asyncio.sleep(...)`

##  Assumptions and Notes

- All tools are simulated. No real job scheduling or cloud file access occurs.
- Plotting is based on small local CSV files; files are created dynamically in tests.
- All handlers are asynchronous and return MCP-compliant JSON responses.
- Proper error responses are implemented for missing parameters or tool names.
- JSON-RPC error codes include: `-32601` (method not found), `-32602` (invalid params), and `-32000` (internal errors).

---

## Repository Structure

```
scientific-mcp-server/
├── pyproject.toml
├── README.md
├── src/
│   ├── server.py
│   ├── mcp_handlers.py
│   └── capabilities/
│       └── plot_handler.py
├── tests/
│   ├── test_mcp_handlers.py
│   └── test_capabilities.py
└── .gitignore
```

