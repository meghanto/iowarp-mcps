# `wrp_chat_factory` – Instructions

This document provides detailed instructions on how to set up, run, test, and extend the `wrp_chat_factory`, a provider-agnostic command-line gateway for MCP tool invocations.

For a quick overview, see the main [README.md](./README.md).
For specific command examples, see the [example.md](./example.md) file.

---

## 1. Setup

Follow these steps to get the chat factory running on your local machine.

### Step 1: Clone the Repository
```bash
# Replace with your repository's URL if it's different
git clone https://github.com/iowarp/scientific-mcps.git
cd scientfic-mcps
```

### Step 2: Create and Activate a Virtual Environment
Using a virtual environment is strongly recommended to avoid package conflicts.
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies
Install all the required dependencies at once using the `requirements.txt` file located in the `bin` directory.

This file includes the core libraries and the Python SDKs for all supported LLM providers (Gemini, OpenAI, Claude, and Ollama).

```bash
# Install all dependencies from the requirements file
pip install -r bin/requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root of the project to store your API keys.

```bash
# This command creates an empty .env file
# On Windows:
copy NUL .env
# On macOS/Linux:
touch .env
```

Edit the `.env` file to add your credentials. Only the variables for the providers you use are needed.
```ini
# For Google Gemini
GEMINI_API_KEY="your-gemini-api-key"

# For OpenAI
OPENAI_API_KEY="your-openai-api-key"

# For Anthropic Claude
ANTHROPIC_API_KEY="your-anthropic-api-key"

# For a local Ollama instance
OLLAMA_HOST="http://localhost:11434"
```

---

## 2. Usage

To run the factory, execute the script from your terminal while your virtual environment is active. Specify a provider and the server(s) you want to connect to.

The script will automatically find and start the required server process(es) for you in the background.

**Provider: `gemini`**
```bash
python bin/wrp_chat_factory.py --provider gemini --servers Jarvis
```

**Provider: `openai`**
```bash
python bin/wrp_chat_factory.py --provider openai --servers Jarvis
```

**Provider: `claude`**
```bash
python bin/wrp_chat_factory.py --provider claude --servers Jarvis
```

**Provider: `ollama`**
```bash
python bin/wrp_chat_factory.py --provider ollama --servers Jarvis
```

---

## 3. Advanced Usage

### Provider-Specific Arguments
You can pass arguments directly to an LLM adapter by placing them after a `--` separator. This is most commonly used to specify a model.

**Example:** Use the `llama3` model with Ollama.
```bash
python bin/wrp_chat_factory.py --provider ollama --servers Jarvis -- --model=llama3
```

### Connecting to Multiple Servers
You can connect to multiple MCP servers in a single session by providing a comma-separated list.

```bash
python bin/wrp_chat_factory.py --provider gemini --servers=Jarvis,HDF5,Slurm
```
The factory will connect to each server sequentially.

---

## 4. Testing & Development

### Adding a New Provider
1.  **Implement the Adapter**: In `wrp_chat_factory.py`, create a new class that inherits from `BaseLLM`. It must implement the `async def chat(...)` method.
2.  **Register the Adapter**: Add your new class to the `PROVIDER_REGISTRY` dictionary.
3.  **Document Env Vars**: If your new provider requires API keys, add them to this document and the main `README.md`.

### Testing
*The project must be configured with a testing framework (like `pytest`) for these commands to work.*
```bash
# Run fast unit tests (these should mock LLM calls and servers)
pytest -q

# Run slower integration tests (these may require live MCP servers)
pytest -m integration -q
```

---

## 5. Troubleshooting

| Issue                      | Fix                                                                                             |
|----------------------------|-------------------------------------------------------------------------------------------------|
| `ImportError: ... not found` | Ensure you have installed the required Python package for your provider inside your virtual environment (see Step 1.3). |
| `ValueError: ... not set`  | Verify that the correct API key is set in your `.env` file and the file is in the project root.      |
| `FileNotFoundError`        | Check that the `--servers` names are correct and that the corresponding `server.py` file exists.    |
| `Connection closed`        | The MCP server likely crashed on startup. Run the server script directly (`python path/to/server.py`) to see the error message. |
| No tools listed            | Check that the MCP server is running correctly and that it uses the `stdio` transport.          |
| Model hangs or errors      | This could be a provider-side issue (e.g., rate limiting). Try again, use a different model, or switch to another provider. | 