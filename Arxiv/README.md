
# Scientific MCP Server

##  Implemented MCP Capabilities

The following capabilities have been implemented:

| Capability    | Type     | Description                                                              |
|---------------|----------|--------------------------------------------------------------------------|

| `arxiv`       | Data     | Fetches 3 recent research papers via the Arxiv API using `httpx`.        |


## Setup Instructions (Using `uv`)

1. Clone the repository:
   ```bash
   git clone https://github.com/iowarp/scientific-mcps.git
   cd arxiv
   ```

2. Create a virtual environment with `uv`:
   ```bash
   uv venv
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. (Optional) Generate a lockfile:
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

# MCP Capabilities

| Method              | Description                                 |
|---------------------|---------------------------------------------|
| `mcp/listTools`     | Lists tool-oriented capabilities only       |
| `mcp/listDataSources` | Lists data-oriented capabilities only    |

These are accessible via the same `/mcp` endpoint using the standard JSON-RPC 2.0 structure.

- Implemented MCP capabilities  
    - `arxiv` (data)

- Implemented robust error handling using JSON-RPC 2.0 error format  
  -  Standardized error codes:
    - `-32601` : method/tool not found
    - `-32602` : invalid or missing parameters
    - `-32000/-32001` : general internal errors

- Asynchronous logic in all capability handlers  
  - All capability functions are defined using `async def`
  - `arxiv` uses `httpx.AsyncClient()` for real API calls

##  Assumptions and Notes

- Arxiv responses are summarized and do not include full XML parsing.
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
│       ├── arxiv_handler.py
│    
├── tests/
│   ├── test_mcp_handlers.py
│   └── test_capabilities.py
└── .gitignore
```
