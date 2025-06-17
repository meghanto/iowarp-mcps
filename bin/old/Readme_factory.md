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
```

You'll see a list of available tools pulled from the server:

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

…but **ignore this until you're happy running locally**.

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