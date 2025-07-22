import json
import asyncio
import sys
import os
import yaml
from contextlib import AsyncExitStack
from pathlib import Path
from typing import List, Optional, Dict, Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from .providers.base import BaseLLM, ToolDef

def discover_plugins() -> Dict[str, Dict[str, Any]]:
    """
    Discovers all available plugins by scanning for plugin.yaml files.
    Returns a dictionary mapping plugin names to their metadata.
    """
    plugins = {}
    repo_root = Path(__file__).resolve().parent.parent.parent

    # Search in the main directory (which includes examples via rglob)
    search_paths = [repo_root]

    for search_root in search_paths:
        if not search_root.exists():
            continue

        # Find all plugin.yaml files
        for plugin_file in search_root.rglob("plugin.yaml"):
            try:
                with open(plugin_file, 'r') as f:
                    plugin_data = yaml.safe_load(f)

                # Validate required fields
                required_fields = ['name', 'description', 'server_path']
                if not all(field in plugin_data for field in required_fields):
                    print(f"Warning: Invalid plugin.yaml at {plugin_file}: missing required fields", file=sys.stderr)
                    continue

                # Check for duplicate plugin names
                if plugin_data['name'] in plugins:
                    print(f"Warning: Duplicate plugin name '{plugin_data['name']}' found at {plugin_file}, skipping", file=sys.stderr)
                    continue

                # Make server_path absolute relative to plugin directory
                plugin_dir = plugin_file.parent
                server_path = plugin_dir / plugin_data['server_path']

                # Check if server executable exists
                if not server_path.exists():
                    print(f"Warning: Server executable not found for plugin {plugin_data['name']}: {server_path}", file=sys.stderr)
                    continue

                plugin_data['server_path'] = str(server_path)
                plugin_data['plugin_dir'] = str(plugin_dir)
                plugins[plugin_data['name']] = plugin_data

            except Exception as e:
                print(f"Warning: Failed to load plugin.yaml at {plugin_file}: {e}", file=sys.stderr)
                continue

    return plugins


def find_server(plugin_name: str, plugins: Dict[str, Dict[str, Any]]) -> str:
    """
    Finds the server executable for a given plugin name using pre-discovered plugins.
    """
    if plugin_name not in plugins:
        raise FileNotFoundError(f"Plugin '{plugin_name}' not found")

    return plugins[plugin_name]['server_path']


class MCPManager:
    """
    Manages the connection and interaction with a single MCP server.
    """
    def __init__(self, llm_adapter: BaseLLM, verbose: bool = False):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm = llm_adapter
        self.tools: List[ToolDef] = []
        self.verbose = verbose

    async def connect(self, server_script: str):
        print(f"Starting server with stdio: {server_script}" if self.verbose else "")
        params = StdioServerParameters(command=sys.executable, args=[server_script], env=os.environ)
        reader, writer = await self.exit_stack.enter_async_context(stdio_client(params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(reader, writer))

        await self.session.initialize()
        tool_list = await self.session.list_tools()

        self.tools = [
            ToolDef(
                name=t.name,
                description=t.description,
                input_schema=t.inputSchema,
            )
            for t in tool_list.tools
        ]
        print("\nConnected. Tools available:\n")
        for tool in self.tools:
            print(f" * {tool.name}: {tool.description}")

    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        try:
            llm_reply = await self.llm.chat(messages, self.tools)

            if llm_reply.tool_calls:
                tool_results = []
                verbose_parts = []

                for tool_call in llm_reply.tool_calls:
                    name, args = tool_call["name"], tool_call["args"]
                    if self.verbose:
                        verbose_parts.append(f"[Calling tool {name} with args {args}]")

                    try:
                        tr = await self.session.call_tool(name, args)
                        raw_txt = tr.content[0].text if tr.content else "No content returned"

                        is_error = False
                        try:
                            parsed = json.loads(raw_txt)
                            if isinstance(parsed, dict) and (parsed.get("isError") or "error" in parsed):
                                is_error = True
                        except Exception:
                            pass

                        if self.verbose:
                            verbose_parts.append(f"[Called {name}: {raw_txt}]")

                        if is_error:
                            tool_results.append("Error: Incorrect filepath or argument passed.")
                        else:
                            tool_results.append(raw_txt)

                    except Exception as e:
                        error_msg = f"Error calling {name}: {e}"
                        tool_results.append(error_msg)
                        if self.verbose:
                            verbose_parts.append(f"[{error_msg}]")

                # Combine all tool results for LLM processing
                combined_results = "\n".join(tool_results)

                # Create a new message with the original query and tool results
                followup_messages = [
                    {"role": "user", "content": f"Original query: {query}\n\nTool results: {combined_results}\n\nPlease provide a clear, natural language response to the original query based on these tool results."}
                ]

                # Get LLM to process the results into natural language (no tools needed)
                final_reply = await self.llm.chat(followup_messages, [])

                if self.verbose:
                    # Show verbose info first, then the natural language output
                    verbose_output = "\n".join(verbose_parts)
                    return f"{verbose_output}\nOutput: {final_reply.text}"
                else:
                    return f"Output: {final_reply.text}"
            else:
                return llm_reply.text

        except Exception as e:
            return f"Error during LLM processing: {e}"

    async def chat_loop(self):
        print(f"\nMCP Client Started! (type 'quit' to exit)")
        try:
            while True:
                q = input("\nQuery: ").strip()
                if q.lower() in ('quit', 'exit'):
                    break
                response_text = await self.process_query(q)
                print(f"\n{response_text}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
        finally:
            await self.cleanup()

    async def cleanup(self):
        await self.exit_stack.aclose() 