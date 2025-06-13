#!/bin/env python3
import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Optional, NamedTuple
import argparse
from pathlib import Path
import sys

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import ollama
from ollama import Client as OllamaClient

class ExecutionParams(NamedTuple):
    raw: bool
    stats: bool
    seed: Optional[int] = None
    temperature: Optional[float] = None

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
    """Handles connection and communication with an MCP server using Ollama as the LLM backend."""
    def __init__(self, model_name='llama2'):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.ollama_client = OllamaClient(host='http://localhost:11434')
        self.model_name = model_name
        self.available_tools = {}

    async def connect(self, server_script: str):
        """Connect to the MCP server and initialize the session."""
        print(f"Starting server with stdio: {server_script}")
        command = sys.executable
        args = [server_script]
        params = StdioServerParameters(command=command, args=args, env=os.environ)
        reader, writer = await self.exit_stack.enter_async_context(
            stdio_client(params)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(reader, writer)
        )
        await self.session.initialize()
        tools = await self.session.list_tools()
        print("Connected. Tools available:")
        for t in tools.tools:
            print(f" - {t.name}: {t.description}")
            self.available_tools[t.name] = t

    async def process_query(self, query: str) -> dict:
        """Process a user query using Ollama and handle any tool calls."""
        if not self.available_tools:
            return {"text": "No tools available. Please ensure connection is established.", "usage_metadata": {}}

        # Create a system prompt that describes the available tools
        system_prompt = (
            "You are a helpful assistant with access to MCP (Machine Control Protocol) tools. "
            "IMPORTANT INSTRUCTIONS:\n"
            "1. When asked to perform an action (like listing, creating, or showing something), USE THE APPROPRIATE TOOL.\n"
            "2. DO NOT just list or describe the tools - actually use them.\n"
            "3. For general questions or greetings, respond conversationally without using tools.\n\n"
            "To use a tool, your response must be in this exact format:\n"
            "TOOL: <tool_name>\nARGS: <json_args>\n\n"
        )
        
        for name, tool in self.available_tools.items():
            system_prompt += f"\n- {name}: {tool.description}"
            if tool.inputSchema.get("properties"):
                system_prompt += "\n  Parameters:"
                for param_name, param_info in tool.inputSchema.get("properties", {}).items():
                    required = "required" if param_name in tool.inputSchema.get("required", []) else "optional"
                    system_prompt += f"\n    - {param_name} ({required}): {param_info.get('description', '')}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        try:
            response = self.ollama_client.chat(
                model=self.model_name,
                messages=messages
            )
            
            content = response.message.content
            final_parts = []
            
            # Check if the response contains a tool call
            if "TOOL:" in content:
                try:
                    # Parse tool call
                    tool_lines = content.split("\n")
                    tool_name = None
                    tool_args = {}
                    
                    for line in tool_lines:
                        if line.startswith("TOOL:"):
                            tool_name = line.replace("TOOL:", "").strip()
                        elif line.startswith("ARGS:"):
                            args_str = line.replace("ARGS:", "").strip()
                            tool_args = json.loads(args_str)
                    
                    if tool_name and tool_name in self.available_tools:
                        print(f"[Calling tool {tool_name} with args {tool_args}]")
                        tr = await self.session.call_tool(tool_name, tool_args)
                        raw_txt = tr.content[0].text
                        final_parts.append(f"[Called {tool_name}: {raw_txt}]")
                    else:
                        final_parts.append(content)
                except (json.JSONDecodeError, KeyError, Exception) as e:
                    # If there's any error parsing the tool call, treat it as regular text
                    final_parts.append(content)
            else:
                final_parts.append(content)
            
            return {
                "text": "\n".join(final_parts).strip(),
                "usage_metadata": {
                    "prompt_token_count": 0,
                    "response_token_count": 0
                }
            }
            
        except Exception as e:
            return {
                "text": f"Error: {str(e)}",
                "usage_metadata": {
                    "prompt_token_count": 0,
                    "response_token_count": 0
                }
            }

    async def chat_loop(self):
        """Main chat loop for interacting with the user."""
        print(f"MCP Client Started with {self.model_name}! (type 'quit' to exit)")
        try:
            while True:
                q = input("\nQuery: ").strip()
                if q.lower() in ('quit', 'exit'):
                    break
                out = await self.process_query(q)
                print(f"\n{out['text']}")
        except KeyboardInterrupt:
            print("\nReceived interrupt signal, cleaning up...")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources."""
        if self.exit_stack:
            try:
                await self.exit_stack.aclose()
            except Exception:
                pass  # Ignore cleanup errors

async def async_main(server_names, model_name):
    """Main async function to handle multiple server connections."""
    for server_name in server_names:
        print(f"\n=== Connecting to {server_name} ===")
        server_py = find_server_py(server_name)
        client = MCPClient(model_name=model_name)
        try:
            await client.connect(server_py)
            await client.chat_loop()
        finally:
            await client.cleanup()

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="MCP Client using Ollama for local LLM support")
    parser.add_argument(
        "--servers",
        required=True,
        help="Comma-separated list of server names (e.g. HDF5,Arxiv)"
    )
    parser.add_argument(
        "--model",
        default="llama2",
        help="Name of the Ollama model to use (default: llama2)"
    )
    args = parser.parse_args()
    server_names = [name.strip() for name in args.servers.split(",")]
    asyncio.run(async_main(server_names, args.model))

if __name__ == "__main__":
    main() 