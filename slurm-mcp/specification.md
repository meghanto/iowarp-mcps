# Assignment Objective
The primary goal of this assignment is to gain practical experience with:
1. Understanding the core concepts of the Model Context Protocol (MCP).
2. Implementing a basic MCP server using Python and standard web/RPC frameworks.
3. Exposing diverse scientific functionalities (data access, tool execution) via the MCP
interface.
4. Utilizing modern Python development practices, including dependency management with
uv and testing with pytest.

# Target MCP Implementation: 
Implement the logic within your server to handle requests related to these capabilities.

# MCP Capabilities:
● Slurm: Accept parameters like script path and core count, perhaps use
subprocess to echo a message like "Job submitted", and return a mock
job ID.
Features
• Basic sbatch submission
• Echo params & parse job ID
• JobContext data model

Slurm "Submit run_analysis.sh using 8 cores" Job scheduler subprocess to echo submission, return mock Job ID
# Technical Requirements:

● Language: Python (version 3.10 or higher recommended).
● Dependency Management: Use uv (from Astral) for creating virtual environments and
managing dependencies. All dependencies must be listed in a pyproject.toml file.
● Testing: Implement unit tests for your chosen MCP resource/tool handlers using
pytest. Tests should cover basic success cases and at least one error/edge case per
implemented MCP capability.
● Server: Implement using python_mcp_sdk.md specification where you find Python implementation of the Model Context Protocol (MCP)
● Code Quality: Write clear, well-commented, and reasonably modular Python code.
Follow PEP 8 guidelines.
● Project Structure: Adhere to the following basic structure:
your-repo-name/
├── pyproject.toml # Project metadata and dependenciesa
├── README.md # Explanation, setup, run instructions
├── src/ # Your server source codea
│ ├── __init__.py
│ ├── server.py # Main server application setup (use python_mcp_sdk.md)
│ ├── mcp_handlers.py # Logic for handling MCP requests
│ └── capabilities/ # Modules for each implemented capability (optional structure)
│ ├── __init__.py
│ └── slurm_handler.py
└── tests/ # Pytest tests
├── __init__.py
├── test_mcp_handlers.py
└── test_capabilities.py # Or specific test files per capability
