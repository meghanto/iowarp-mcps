# UNDER DEVELOPMENT. THIS SCRIPT IS NOT READY FOR USE.
# Objectives:   
# 1. Create a script that can be used to chat with multiple MCP servers parallelly.
# 2. Can chat with servers using Gemini or ollama.

import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Optional
import argparse
from pathlib import Path
import sys

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client with API key
client = genai.Client(api_key=GEMINI_API_KEY)


def find_server_py(server_name: str) -> str:
    """
    Recursively find server.py for a given server name in the repo.
    Looks under <repo_root>/<server_name>/src/ for any server.py.
    """
    repo_root = Path(__file__).resolve().parent.parent
    server_src = repo_root / server_name / "src"
    if not server_src.exists():
        raise FileNotFoundError(f"src directory not found for {server_name} at {server_src}")
    matches = list(server_src.rglob("server.py"))
    if not matches:
        raise FileNotFoundError(f"Could not find server.py for {server_name} under {server_src}")
    return str(matches[0])


class MCPClient:
    """Handles connection and communication with an MCP server."""
    def __init__(self, server_name: str):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.server_name = server_name
        self.reader = None
        self.writer = None
        self._cleanup_lock = asyncio.Lock()
        self._process = None

    async def connect(self, server_script: str):
        print(f"Starting server with stdio: {server_script}")
        command = sys.executable
        args = [server_script]
        params = StdioServerParameters(command=command, args=args, env=os.environ)
        
        # Store the reader and writer for cleanup
        self.reader, self.writer = await self.exit_stack.enter_async_context(
            stdio_client(params)
        )
        
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.reader, self.writer)
        )
        await self.session.initialize()
        tools = await self.session.list_tools()
        print(f"\nConnected to {self.server_name}. Tools available:")
        for t in tools.tools:
            print(f" - {t.name}: {t.description}")

    async def process_query(self, query: str) -> dict:
        try:
            resp_tools = await self.session.list_tools()
            tool_descs = []
            for t in resp_tools.tools:
                tool_descs.append({
                    "name": t.name,
                    "description": t.description,
                    "parameters": {
                        "type": t.inputSchema.get("type", "object"),
                        "properties": {
                            k: {"type": v.get("type", "string"), "description": v.get("description", "")}
                            for k, v in t.inputSchema.get("properties", {}).items()
                        },
                        "required": t.inputSchema.get("required", [])
                    }
                })
            tools_schema = types.Tool(function_declarations=tool_descs)
            config = types.GenerateContentConfig(tools=[tools_schema])
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[query],
                config=config,
            )
            um = response.usage_metadata
            prompt_tokens = um.prompt_token_count
            completion_tokens = um.candidates_token_count
            final_parts = []
            for cand in response.candidates:
                parts = getattr(cand.content, 'parts', None)
                if parts:
                    for part in parts:
                        if getattr(part, 'function_call', None):
                            name = part.function_call.name
                            raw = part.function_call.args
                            args = json.loads(raw) if isinstance(raw, str) else raw
                            print(f"[{self.server_name}] Calling tool {name} with args {args}")
                            tr = await self.session.call_tool(name, args)
                            raw_txt = tr.content[0].text
                            final_parts.append(f"[Called {name}: {raw_txt}]")
                        elif getattr(part, 'text', None):
                            final_parts.append(part.text)
                else:
                    txt = getattr(cand.content, 'text', '')
                    if txt:
                        final_parts.append(txt)
            return {
                "text": "\n".join(final_parts).strip(),
                "usage_metadata": {
                    "prompt_token_count": prompt_tokens,
                    "response_token_count": completion_tokens
                }
            }
        except Exception as e:
            return {
                "text": f"Error processing query: {str(e)}",
                "usage_metadata": {"prompt_token_count": 0, "response_token_count": 0}
            }

    async def cleanup(self):
        async with self._cleanup_lock:
            try:
                if self.session:
                    # Close the session's reader and writer
                    if hasattr(self.session, 'reader') and self.session.reader:
                        self.session.reader.close()
                    if hasattr(self.session, 'writer') and self.session.writer:
                        self.session.writer.close()
                    self.session = None
                
                if self.exit_stack:
                    try:
                        await self.exit_stack.aclose()
                    except Exception as e:
                        print(f"Warning: Error closing exit stack for {self.server_name}: {str(e)}")
                    self.exit_stack = None
            except Exception as e:
                print(f"Error cleaning up {self.server_name}: {str(e)}")


async def async_main(server_names):
    clients = {}
    try:
        # Create and connect to all servers
        for server_name in server_names:
            print(f"\n=== Connecting to {server_name} ===")
            server_py = find_server_py(server_name)
            client = MCPClient(server_name)
            await client.connect(server_py)
            clients[server_name] = client

        print("\nMCP Client Started! (type 'quit' to exit)")
        print("Available servers:", ", ".join(clients.keys()))
        print("To query a specific server, prefix your query with the server name, e.g.:")
        print("HDF5: list all files")
        print("Jarvis: list all pipelines")
        
        while True:
            try:
                q = input("\nQuery: ").strip()
                if q.lower() in ('quit', 'exit'):
                    break

                # Check if query is for a specific server
                server_query = None
                for server_name in clients:
                    if q.startswith(f"{server_name}:"):
                        server_query = (server_name, q[len(server_name)+1:].strip())
                        break

                if server_query:
                    server_name, query = server_query
                    out = await clients[server_name].process_query(query)
                    print(f"\n[{server_name}]")
                    print(out["text"])
                    um = out["usage_metadata"]
                    total = um["prompt_token_count"] + um["response_token_count"]
                    print(f"[Tokens: {total} (prompt {um['prompt_token_count']}, response {um['response_token_count']})]")
                else:
                    # Process query on all servers
                    results = await asyncio.gather(
                        *(client.process_query(q) for client in clients.values()),
                        return_exceptions=True
                    )
                    for server_name, result in zip(clients.keys(), results):
                        print(f"\n[{server_name}]")
                        if isinstance(result, Exception):
                            print(f"Error: {str(result)}")
                        else:
                            print(result["text"])
                            um = result["usage_metadata"]
                            total = um["prompt_token_count"] + um["response_token_count"]
                            print(f"[Tokens: {total} (prompt {um['prompt_token_count']}, response {um['response_token_count']})]")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error processing query: {str(e)}")

    finally:
        # Cleanup all clients
        cleanup_tasks = []
        for client in clients.values():
            cleanup_tasks.append(asyncio.create_task(client.cleanup()))
        
        if cleanup_tasks:
            try:
                # Wait for all cleanup tasks with a timeout
                done, pending = await asyncio.wait(cleanup_tasks, timeout=5.0)
                
                # Cancel any pending tasks
                for task in pending:
                    task.cancel()
                
                # Wait for cancelled tasks to complete
                if pending:
                    await asyncio.wait(pending, timeout=1.0)
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--servers",
        required=True,
        help="Comma-separated list of server names (e.g. HDF5,Arxiv)"
    )
    args = parser.parse_args()
    server_names = [name.strip() for name in args.servers.split(",")]
    
    try:
        asyncio.run(async_main(server_names))
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()