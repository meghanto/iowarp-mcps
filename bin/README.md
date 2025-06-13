# WRP_CHAT: Scientific MCP Client

`wrp_chat` is a universal command-line client for interacting with any Model Context Protocol (MCP) server in the scientific-mcps suite. It supports two LLM backends:
1. Google Gemini (via `wrp_chat.py`)
2. Ollama (via `wrp_chat_ollama.py`)

---

## Setup

### For Gemini Backend

1. **Install dependencies** (from the root of the repo):
   ```bash
    uv pip install "git+https://github.com/iowarp/scientific-mcps.git@main"
   ```

2. **Create a `.env` file** in the root directory with your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### For Ollama Backend

1. **Install Ollama**:
   - Visit [Ollama's website](https://ollama.ai/) to download and install Ollama for your platform
   - For Windows users: Install WSL2 first, then install Ollama through WSL2

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Using Gemini Backend

To start the client and connect to one or more MCP servers:

```bash
python3 bin/wrp_chat.py --servers=HDF5,Arxiv,Jarvis
```

### Using Ollama Backend

To start the client with Ollama:

```bash
python3 bin/wrp_chat_ollama.py --servers=HDF5,Arxiv,Jarvis
```

By default, it uses the `llama2` model, but you can specify a different model:

```bash
python3 bin/wrp_chat_ollama.py --servers=Jarvis --model=codellama
```

For both clients:
- The `--servers` argument is a comma-separated list of MCP server names (matching the subdirectory names in the repo).
- The client will automatically locate each server's `server.py` under `<ServerName>/src/server.py`.

### Example

```bash
python3 bin/wrp_chat_ollama.py --servers=Jarvis
```

You will see:
```
=== Connecting to Jarvis ===
Starting server with stdio: /path/to/scientific-mcps/Jarvis/src/server.py
Connected. Tools available:
 - create_pipeline: Create a new Jarvis-CD pipeline environment.
 - run_pipeline: Execute a Jarvis-CD pipeline end-to-end.
 ...
MCP Client Started! (type 'quit' to exit)

Query: Initialize jarvis with config, private and shared dir as './jarvis-pipelines'
[...response...]
```

---

## Environment Variables

- `GEMINI_API_KEY` (required for Gemini backend): Your Google Gemini API key for LLM-powered queries.
- No API key required for Ollama backend.

---

## End-to-End Example: Using Jarvis MCP

1. **Start the client** (using either backend):
   ```bash
   bin/wrp_chat --servers=Jarvis
   # OR
   bin/wrp_chat_ollama --servers=Jarvis
   ```
2. **Interact with Jarvis:**
   ```
   Query: Initialize jarvis with config, private and shared dir as './jarvis-pipelines'
   Query: create a pipeline called ior_test and append package ior to it
   Query: show the configuration of ior in ior_test
   Query: update the nprocs to 8 for package ior in pipeline ior_test
   Query: Build environment for pipeline ior_test
   Query: select the pipeline ior_test and run it
   ```

---

## Notes
- You can connect to multiple servers at once by listing them in `--servers` (e.g. `--servers=HDF5,Arxiv,Jarvis`).
- The client will print available tools for each server on connect.
- Type `quit` or `exit` to leave the chat loop.
- For more details on each MCP, see the respective subdirectory's README.
- When using Ollama backend, ensure the Ollama service is running before starting the client. 