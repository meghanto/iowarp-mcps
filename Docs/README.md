# Model Context Protocol (MCP)

## Overview

This subdirectory provides a understanding and basic implementation of the Model Context Protocol (MCP), a standardized interface for connecting AI applications with external tools and data sources. Designed to solve the MxN integration problem in AI systems, it offers:

## Navigate to 
- **[Architecture Deep Dive](<./MCP Deep Dive/>)**: for building understanding of MCPS, the technical specifications and protocol documentation
- **[Implementations](<./Basic MCP Implementation/>)**: for tutorials on building MCP servers/clients for filesystems, weather APIs, and other scenerios
- **[Python SDK Setup & Custom Client](<./Basic MCP Implementation/MCP Python SDK/>)**: for documentation on Python MCP SDK with CLI support and Claude Desktop integrations


## Features

**Core Protocol Features**

- JSON-RPC 2.0 communication with stateful connections
- Client-server architecture with capability negotiation
- Three server primitives: Tools, Resources, and Prompts

## Prerequisites

- Python 3.9+
- [UV package manager](https://github.com/astral-sh/uv)
- Docker (for IOWarp deployments)
- API Keys: [Gemini](https://ai.google.dev/) / [Claude Desktop](https://docs.anthropic.com/claude/docs)


## Installation

```bash
git clone https://github.com/aumsathwara/GRC_Aum.git
cd GRC_Aum
```

**Key Implementations Setup**

1. **FileSystem MCP**
```bash
cd "Basic MCP Implementation/FileSystem MCP"
uv add "mcp[cli]"
uv run server.py
```

2. **Python SDK**
```bash
cd "MCP Python SDK"
uv pip install -r requirements.txt
```


## Usage

**Basic Workflow**

1. Start MCP Server
```bash
uv run mcp dev "Basic MCP Implementation/FileSystem MCP/Server/server.py"
```

2. Connect via Client
```python
from mcp.client import ClientSession
session = ClientSession.connect("filesystem://localhost:8000")
```

3. Use MCP Inspector
```
http://localhost:8000/status
```

**Claude Desktop Integration**

```json
{
  "mcpServers": {
    "FileSystem": {
      "command": "uv",
      "args": ["run", "server.py"]
    }
  }
}
```


### Contributing
Contributions are welcomed through:

1. **New MCP Implementations**: Create servers for novel use cases
2. **Protocol Enhancements**: Improve error handling/security
3. **Documentation**: Expand tutorials and API references

**Process**

1. Fork repository
2. Create feature branch (`git checkout -b feature/feature-name`)
3. Commit changes
4. Push to branch
5. Open PR with detailed documentation

For major changes, please open an issue first to discuss proposed changes.
