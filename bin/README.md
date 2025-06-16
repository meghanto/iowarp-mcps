# WRP_CHAT_FACTORY: Universal Scientific MCP Client

`wrp_chat_factory` is a lightweight, provider-agnostic command-line gateway that connects with scientific servers and turns everyday prompt into a series of MCP tool, resources invocations. It supports multiple LLM backends, including Gemini, Ollama, OpenAI, and Claude, through a single interface.

---

## Quick Start

### 1. Setup Environment

From the root of the repository, create a virtual environment and install the required packages.

```bash
# Create and activate a virtual environment
python -m venv .venv
# On Windows: .\.venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate

# Install all required dependencies from the requirements file
pip install -r bin/requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project's [bin](.) directory and add the necessary API keys for the providers you wish to use.

```ini
# .env file
GEMINI_API_KEY="your-gemini-api-key"
OPENAI_API_KEY="your-openai-api-key"
ANTHROPIC_API_KEY="your-anthropic-api-key"

# For a local Ollama instance (no key needed)
OLLAMA_HOST="http://localhost:11434"
```

### 3. Run the Client

Start the chat factory by specifying an LLM provider and the MCP server(s) you want to connect to.

```bash
# Example using the Gemini provider to connect to the Jarvis MCP
python bin/wrp_chat_factory.py --provider gemini --servers=Jarvis
```

For more detailed setup instructions, provider-specific configurations, and troubleshooting, please see the **[in-depth instructions](./instructions.md)**.

---

## Usage

The script requires two main arguments:

*   `--provider`: The LLM provider to use. Choices: `gemini`, `ollama`, `openai`, `claude`.
*   `--servers`: A comma-separated list of MCP server names (e.g., `HDF5,Jarvis`).

The client will automatically find the `server.py` file for each specified server.

### End-to-End Example: Using Jarvis MCP

This example demonstrates how to use the client to manage a Jarvis pipeline.

1.  **Start the client with your chosen provider:**
    ```bash
    python bin/wrp_chat_factory.py --provider ollama --servers=Jarvis
    ```

2.  **Interact with Jarvis using natural language:**
    ```
    Query: Initialize jarvis with config, private and shared dir as './jarvis-pipelines'
    [Calling tool jm_create_config with args {'config': './jarvis-pipelines', 'private': './jarvis-pipelines', 'shared': './jarvis-pipelines'}]
    [Called jm_create_config: {'status': 'success', 'msg': 'Created ./jarvis-pipelines'}]

    Query: create a pipeline called ior_test and append package ior to it
    [Calling tool create_pipeline with args {'pipeline_id': 'ior_test'}]
    [Called create_pipeline: {'status': 'success', 'pipeline_id': 'ior_test'}]
    [Calling tool append_pkg with args {'pkg_id': 'ior'}]
    [Called append_pkg: {'status': 'success', 'pkg_id': 'ior'}]

    Query: show the configuration of ior in ior_test
    ...
    ```

For more examples with each supported LLM provider, see the **[examples file](./example.md)**.

---

## Notes
- You can connect to multiple servers at once by listing them in `--servers` (e.g. `--servers=HDF5,Arxiv,Jarvis`).
- The client will print available tools for each server on connect.
- Type `quit` or `exit` to leave the chat loop.
- For more details on each MCP, see the respective subdirectory's README.
- When using Ollama backend, ensure the Ollama service is running before starting the client. 