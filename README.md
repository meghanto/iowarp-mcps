# IoWarp MCPs

## Overview

This project implements a **Scientific Model Context Protocol (MCP) Server** using **FastAPI** and **JSON-RPC 2.0**. The server simulates various scientific computing capabilities and allows **AI agents** and **Large Language Models (LLMs)** to interact with tools and data sources in a standardized way.

## Implemented MCP Capabilities

The following capabilities have been implemented:

| Capability | Type | Description |
|---|---|---|
| `Adios` | Data | Reads data from different file types using the ADIOS2 engine. |
| `Arxiv` | Data | Fetches recent research papers from the Arxiv API. |
| `ChronoLog` | External System | Provides tools to log and retrieve data from a ChronoLog server. |
| `Compression` | Tool | Simulates file compression using Python's `gzip` module. |
| `HDF5` | Data | Lists `.hdf5` files from a specified local directory. |
| `Jarvis` | Tool | Manages the full lifecycle of data-centric pipelines. |
| `Node_Hardware` | Tool | Reports the number of CPU cores on the current system. |
| `Pandas` | Data | Loads and filters data from a CSV file using the `pandas` library. |
| `Parallel_Sort`| Tool | Simulates sorting a large text file and returns the sorted result. |
| `Parquet` | Data | Reads a specific column from a Parquet file using `pyarrow`. |
| `Plot` | Tool | Generates a plot from a local CSV file using `pandas` and `matplotlib`. |
| `Slurm` | Tool | Simulates Slurm-like job submission and returns a fake job ID. |

---

## Installation

First, clone the repository and set up a virtual environment:

- Clone the repository:
    ```bash
   git clone https://github.com/iowarp/scientific-mcps.git
   cd scientific-mcps
   ```
- Install uv:
    ```bash
    pip install uv
    ```
- Create and activate environment using uv:
    ```bash
    uv venv mcp-server
    mcp-server\Scripts\activate     #On Windows
    source mcp-server/bin/activate  #On macOS/Linux
    ```

You can install all MCPs at once or select them individually.

**To install all MCPs:**
```bash
# This installs all dependencies listed in the pyproject.toml
uv pip install --requirement pyproject.toml
```

**To install individual or multiple MCPs:**

| MCP | Installation Code (`uv pip install ...`) | Documentation |
|---|---|---|
| `Adios` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Adios"` | [docs](./Adios/README.md) |
| `Arxiv` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Arxiv"` | [docs](./Arxiv/README.md) |
| `ChronoLog` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Chronolog"` | [docs](./Chronolog/README.md) |
| `Compression` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Compression"` | [docs](./Compression/README.md) |
| `HDF5` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=HDF5"` | [docs](./HDF5/README.md) |
| `Jarvis` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Jarvis"` | [docs](./Jarvis/README.md) |
| `Node_Hardware` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Node_Hardware"` | [docs](./Node_Hardware/README.md) |
| `Pandas` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Pandas"` | [docs](./Pandas/README.md) |
| `Parallel_Sort` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Parallel_Sort"`| [docs](./Parallel_Sort/README.md) |
| `Parquet` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=parquet"` | [docs](./parquet/README.md) |
| `Plot` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Plot"` | [docs](./Plot/README.md) |
| `Slurm` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Slurm"` | [docs](./Slurm/README.md) |

> **Tip**: You can install multiple MCPs in a single command by listing them one after another (e.g., `uv pip install "adios-mcp..." "arxiv-mcp..."`).

---

## Running the Universal Client (`wrp_chat_factory`)

This repository includes a universal client, `bin/wrp_chat_factory.py`, that allows you to interact with any MCP server using natural language. It supports multiple LLM providers (Gemini, OpenAI, Claude, Ollama).

1.  **Install Client Dependencies:**
    ```bash
    # From the root directory
    uv pip install -r bin/requirements.txt
    ```
2.  **Configure API Keys:**
    Create a `.env` file in the [bin](bin) directory and add your API keys. See the client's [documentation](bin/README.md) for details.

3.  **Run the Client:**
    ```bash
    # Example: Connect to the Jarvis server using the Ollama provider
    python bin/wrp_chat_factory.py --provider ollama --servers=Jarvis
    ```

> For detailed setup instructions, provider-specific examples, and troubleshooting, please see the **[client's official documentation](./bin/README.md)**.

---
## Project Structure

```
scientific-mcps/
├── Adios/
├── Arxiv/
├── Chronolog/
├── Compression/
├── HDF5/
├── Jarvis/
├── Node_Hardware/
├── Pandas/
├── Parallel_Sort/
├── parquet/
├── Plot/
├── Slurm/
├── bin/
│   ├── wrp_chat_factory.py
│   ├── README.md
│   ├── instructions.md
│   └── ...
└── ...
```

## Usage

To run any MCP server directly or learn more about its specific capabilities, navigate into its directory and follow the instructions in its local `README.md`.