# PA4 (Scientific MCP Server)

## Author  
- **Name:** Haroon Gharwi
- **Student ID:** A20496551

## Introduction: 
This project implements a lightweight Scientific MCP Server based on the Model Context Protocol (MCP), a new standard protocol to connect the AI assistants to the systems where data lives. It is intrduced by [Anthropic](https://www.anthropic.com/news/model-context-protocol) that is designed to enable a structured communication between clients (such as LLMs) and computational tools through a standardized JSON-RPC 2.0 interface. 

The server is built using FastAPI and consists two main endpoints:

**/mcp/listResources:** Lists the available tools (capabilities) that the server provides.

**/mcp/callTool:** Allows client (such as AI agent) to invoke specific tools by sending method names and required parameters.




## Implemented MCP Capabilities  
In this project, I have integrated two core capabilities:
- **Pandas:** It is used as resource/tool for Data analysis. For this project guideline, I defined one calling method:  filtering the client shared csv data file based on the given column and threshold.
- **Matplotlib:** It is used as reource/tool for visualization. For this project guideline, I created two tools: Plotting columns from shared csv data file based on the given columns x and y and returning the generated plot image one a scatter and another tool as line plot.

## Environment Setup Instructions  
This project uses [**uv**](https://github.com/astral-sh/uv) as for fast Python package and environment management based on Rust. 


1. **Create a virtual environment using uv:**  
   ```bash
   uv venv
   ```

2. **Install all dependencies for this project from pyproject.toml:**  
   ```bash
   uv sync
   ```
   This will automatically install all necessary packages: FastAPI, Uvicorn, Pandas, Matplotlib, Pytest, etc.. with recommended versions
3. **Generate the lock file to freezes the exact versions of the installed dependencies:**  
   ```bash
   uv lock
   ```
## Running the MCP Server  

1. To start the server run the following on the terminal at the project directory:

```bash
uvicorn src.server:app --reload --port 8000
```
This will run the start a web server:
- Access the server at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- For more Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## Running the Tests

**Run all tests using pytest**:  
To run the 10 test cases, run the following on the terminal:
```bash
pytest -v
```
## Assumptions and Notes

- **Static Images Folder:**  
  Matplotlib generated plots are saved inside the `/images` directory.

- **JSON-RPC 2.0 Compliance:**  
  All client requests must adhere strictly to the JSON-RPC 2.0 specification.

- **Simple Error Handling:**  
  Server returns standard JSON-RPC errors for invalid or unknown methods.

- **Testing Limitations:**  
  Only basic functionality and error response tests are included.

- **Time Limitations and view resources:**  
  Since the MCP is intrduced in Nov 2024, there are limited resources avaliable on the internet about the full sturecture of MCP, Thersore, I added only four essential keys (jsonrpc, method, params, id). up to now, I did not find a clear guidance on how to include multiple tools/methods for each resource. If there is more time, I would include more reources/tools and bind them with the chatGPT 4 API using function calling approach to build a full agentic AI. 

---
