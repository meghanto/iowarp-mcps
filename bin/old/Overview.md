### **overview\.md**

````markdown
# wrp_chat_factory – Local-First Overview

## 1. Purpose  
`wrp_chat_factory` is a **lightweight, provider-agnostic command-line gateway** that turns an everyday prompt into a series of **MCP tool invocations**.  
It ships with thin adapters for Gemini, OpenAI / ChatGPT, Claude, and local Ollama LLMs, yet lets you slot in any future provider with a ~50-line class.

---

## 2. Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI as python bin/wrp_chat_factory
    participant LLM as LLM Adapter
    participant Router as Tool Router
    participant MCP as MCP Client
    User->>CLI: "create pipeline my_pipeline…"
    CLI->>LLM: prompt + tool schema
    LLM-->>LLM: chooses function calls
    LLM->>Router: [{name:"create_pipeline", …}]
    Router->>MCP: exec via stdio
    MCP-->>Router: ok
    Router->>User: ✔ pipeline created
````

---

## 3. Layered Design

| Layer                            | Main Class                      | Notes                                                                                           |
| -------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------- |
| **CLI** (`bin/wrp_chat_factory`) | `main()`                        | Parses `--provider` & `--servers` flags (mirrors existing `wrp_chat.py` / `wrp_chat_ollama.py`) |
| **Session**                      | `SessionState`                  | Tracks messages, token counts                                                                   |
| **LLM Adapter**                  | `BaseLLM` + concrete subclasses | Strategy pattern; each subclass wraps a vendor SDK                                              |
| **Tool Router**                  | `ToolRegistry`, `ToolRouter`    | Validates and dispatches tool calls                                                             |
| **MCP Client**                   | `MCPClient`                     | Re-uses proven stdio connector from the reference scripts                                       |
| **Config Loader**                | `ConfigLoader`                  | Pulls secrets & model names from `.env` / `config.yaml`                                         |
| **Logging**                      | `logger`                        | JSONL with latency & token cost                                                                 |

---

## 4. Key OOP Touches

```python
class BaseLLM(ABC):
    async def chat(self, messages: list[dict], tools: list[ToolDef]) -> LLMReply: ...

class GeminiLLM(BaseLLM): ...
class OpenAILLM(BaseLLM): ...
class OllamaLLM(BaseLLM): ...
```

* **Factory registry** picks the adapter at runtime:
  `llm = REGISTRY[cfg.provider](cfg)`

* **MCPClient** stays blissfully ignorant of which model produced the tool call—exactly as in your working Ollama/Gemini clients.

---

## 5. CLI Contract

```bash
python bin/wrp_chat_factory \
       --provider {gemini|openai|claude|ollama} \
       --servers  JarvisServer,Hdf5Server
```

*Multiple servers* are accepted as a comma-separated list; each is auto-resolved to its `server.py`, following the helper already proven in `wrp_chat.py` .

---

## 6. Extending the System

| Add…                | Steps                                                                            |
| ------------------- | -------------------------------------------------------------------------------- |
| **A new provider**  | ① subclass `BaseLLM`; ② add to `REGISTRY`; ③ document env vars.                  |
| **A new MCP tool**  | Decorate a coroutine with `@mcp.tool` in the target `server.py`; restart client. |
| **A new transport** | Implement `IMCPTransport` (e.g., gRPC) and swap via `MCP_TRANSPORT` env var.     |

---

## 7. Roadmap

1. **Batch mode** (`--file prompts.txt`)
2. **Auto-retry with back-off** on rate limits
3. **Token budgeting** per session
4. **Optional Docker images** once the local flow is rock-solid

````

---

### **instructions.md**

```markdown
# wrp_chat_factory – Local-First Instructions
_(Generated from overview.md – keep both in sync.)_

---

## 1. Setup (No Docker)

```bash
# 1 – clone repo
git clone https://github.com/your-org/wrp_chat_factory.git
cd wrp_chat_factory

# 2 – create venv
python -m venv .venv && source .venv/bin/activate

# 3 – install core deps + your provider extras
pip install -e ".[gemini]"      # or [openai], [ollama], ...

# 4 – add secrets
cp .env.template .env
# edit: GEMINI_API_KEY=...  OPENAI_API_KEY=...  OLLAMA_HOST=http://localhost:11434

# 5 – start an MCP server (stdio transport)
python path/to/JarvisServer/src/server.py
# repeat for any additional servers you listed

# 6 – run the chat factory 🎉
python bin/wrp_chat_factory \
       --provider gemini \
       --servers  JarvisServer
````

You’ll see a list of available tools pulled from the server:

```
Connected. Tools available:
 * create_pipeline : Create a new Jarvis-CD pipeline environment
 * append_pkg      : Append a package to a pipeline
 ...
Query:
```

Try:

```
create a pipeline called "my_pipeline" and append a package called ior
```

The adapter will emit two lines like `[Called create_pipeline: ...]`, `[Called append_pkg: ...]`, confirming success.

---

## 2. CLI Flags

| Flag         | Description                                                           |
| ------------ | --------------------------------------------------------------------- |
| `--provider` | `gemini`, `openai`, `claude`, `ollama`, …                             |
| `--servers`  | Comma-separated list of MCP server names (`JarvisServer,Hdf5Server`). |

Internally this maps each name to `*/src/server.py` via the exact same helper used in the working scripts .

Optional flags (adapter-specific) can be passed after `--`, e.g.:

```bash
python bin/wrp_chat_factory --provider ollama --servers JarvisServer -- --model llama3
```

---

## 3. Adding Providers

1. **Create** `wrp_chat_factory/adapters/foo_llm.py`:

   ```python
   class FooLLM(BaseLLM):
       async def chat(self, messages, tools):
           # call FooAI REST → normalise reply
   ```

2. **Register**:

   ```python
   from .foo_llm import FooLLM
   REGISTRY["foo"] = FooLLM
   ```

3. **Document** new env vars in `.env.template`.

*No other code changes required.*

---

## 4. Extending MCP Tools (Local)

```python
# in JarvisServer/src/server.py
@mcp.tool(name="export_pipeline",
          description="Export pipeline as tar.gz")
async def export_pipeline_tool(pipeline_id: str, dest: str) -> dict:
    ...
```

Restart both the server and factory; the new tool appears automatically.

---

## 5. Testing

```bash
pytest -q                   # unit tests mock LLM
pytest -m integration -q    # spins up real server via stdio
```

---

## 6. (Optional) Docker Later

Once local flow feels good, bootstrap containers with:

```bash
docker compose up --build
```

…but **ignore this until you’re happy running locally**.

---

## 7. Troubleshooting

| Issue                      | Fix                                                             |
| -------------------------- | --------------------------------------------------------------- |
| `ENV var XXX not set`      | Fill it in `.env`.                                              |
| `Could not find server.py` | Verify `--servers` names and folder layout.                     |
| Model hangs                | Provider throttling – lower `--max-tokens` or switch to Ollama. |
| No tools listed            | Make sure server is running and using *stdio* transport.        |

---

Happy hacking 🚀

```

---

Copy each fenced block into its separate file (`overview.md`, `instructions.md`) and you’re set!
```
