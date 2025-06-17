#!/bin/env python3
"""
A provider-agnostic command-line gateway for Multi-provider Control Protocol (MCP)
servers.

This script acts as a universal client that can connect to various MCP servers
(like Jarvis, HDF5, etc.) and use different Large Language Models (LLMs) as a
backend to translate natural language queries into MCP tool calls. It supports
multiple LLM providers through a factory pattern, allowing for easy extension.
"""
import sys 
import argparse
import asyncio
import json
import os
from abc import ABC, abstractmethod
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# --- Conditional Imports for LLM Providers ---
# Each provider's SDK is imported in a try-except block. This makes the
# dependencies optional; the script will only fail if the user tries to use a
# provider whose SDK is not installed.
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

try:
    import ollama
    from ollama import Client as OllamaClient
except ImportError:
    ollama = None

try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None


# --- Helper for Import Errors ---

def _raise_import_error(package_name: str):
    """
    Provides a detailed error message for missing optional dependencies.
    
    This function is called when an LLM provider's SDK fails to import. It
    prints detailed debug information to help the user resolve environment issues,
    such as which Python interpreter is being used and where it's looking for packages.
    """
    msg = (
        f"The '{package_name}' package is not installed, but it is required for this provider. "
        f"Please run 'pip install {package_name}'.\n\n"
        f"--- DEBUG INFO ---\n"
        f"The script is running with this Python interpreter: {sys.executable}\n"
        f"It is looking for packages in: {sys.path}\n"
        f"--------------------\n"
        f"If the interpreter path is not inside your '.venv' directory, please run the script using the full path to the virtual environment's python, like this:\n"
        f"On Windows: .\\.venv\\Scripts\\python.exe bin/wrp_chat_factory.py ...\n"
        f"On macOS/Linux: ./.venv/bin/python bin/wrp_chat_factory.py ..."
    )
    raise ImportError(msg)


# --- Data Structures ---
# These NamedTuples define standardized data structures for internal use, ensuring
# consistency in how data is passed between different parts of the application.

class LLMReply(NamedTuple):
    """A standard format for the response from any LLM adapter."""
    text: str
    tool_calls: Optional[List[Dict[str, Any]]] = None

class ToolDef(NamedTuple):
    """A standard format for representing an MCP tool's definition."""
    name: str
    description: str
    input_schema: Dict[str, Any]


# --- Base LLM Adapter ---

class BaseLLM(ABC):
    """
    Abstract Base Class for LLM provider adapters.
    
    This class defines the common interface that all provider-specific adapters
    must implement. This allows the main application logic to interact with any
    LLM provider in a consistent, predictable way.
    """
    @abstractmethod
    async def chat(
        self, messages: List[Dict[str, str]], tools: List[ToolDef]
    ) -> LLMReply:
        """Sends a query to the LLM and returns a standardized reply."""
        ...


# --- Concrete LLM Adapters ---

class GeminiLLM(BaseLLM):
    """Adapter for Google's Gemini models."""
    def __init__(self, model_name: str = "gemini-1.5-flash", **kwargs):
        """Initializes the synchronous Gemini client."""
        if not genai:
            _raise_import_error("google-generativeai")
        
        load_dotenv()
        api_key_value = os.getenv("GEMINI_API_KEY")
        if not api_key_value:
            raise ValueError("GEMINI_API_KEY not found in environment variables or .env file.")

        self.client = genai.Client(api_key=api_key_value)
        self.model_name = model_name
        
    async def chat(
        self, messages: List[Dict[str, str]], tools: List[ToolDef]
    ) -> LLMReply:
        """
        Sends a query to the Gemini API.
        
        It formats the tools and query, runs the synchronous SDK call in a separate
        thread to avoid blocking the asyncio event loop, and then parses the
        response to extract text and tool calls.
        """
        query = messages[-1]["content"]
        
        tool_descs = []
        for t in tools:
            parameters = {
                "type": t.input_schema.get("type", "object"),
                "properties": {
                    k: {"type": v.get("type", "string"), "description": v.get("description", "")}
                    for k, v in t.input_schema.get("properties", {}).items()
                },
                "required": t.input_schema.get("required", []),
            }
            tool_descs.append({
                "name": t.name,
                "description": t.description,
                "parameters": parameters,
            })
        
        tools_schema = types.Tool(function_declarations=tool_descs)
        config = types.GenerateContentConfig(tools=[tools_schema])

        # Use asyncio.to_thread to run the synchronous SDK call in an async context.
        response = await asyncio.to_thread(
            self.client.models.generate_content,
            model=self.model_name,
            contents=[query],
            config=config,
        )

        text_parts = []
        tool_calls = []
        # Parse the response to extract text and function calls.
        for cand in response.candidates:
            if parts := getattr(cand.content, 'parts', None):
                for part in parts:
                    if fc := getattr(part, 'function_call', None):
                        # The arguments can be a string that needs JSON parsing.
                        raw_args = fc.args
                        args = json.loads(raw_args) if isinstance(raw_args, str) else dict(raw_args)
                        tool_calls.append({"name": fc.name, "args": args})
                    elif txt := getattr(part, 'text', None):
                        text_parts.append(txt)

        return LLMReply(text="\n".join(text_parts).strip(), tool_calls=tool_calls)


class OllamaLLM(BaseLLM):
    """Adapter for local models running via Ollama."""
    def __init__(self, model_name: str = "llama2", host: Optional[str] = None, **kwargs):
        """Initializes the synchronous Ollama client."""
        if not ollama:
            _raise_import_error("ollama")
        
        host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = OllamaClient(host=host)
        self.model_name = model_name

    async def chat(
        self, messages: List[Dict[str, str]], tools: List[ToolDef]
    ) -> LLMReply:
        """
        Sends a query to the local Ollama model.
        
        This method constructs a detailed system prompt to instruct the model on how
        to format tool calls. It then runs the synchronous chat call in a thread
        and manually parses the text response for tool call directives.
        """
        
        # Create a system prompt to instruct the model on how to use tools.
        system_prompt = (
            "You are a helpful assistant with access to MCP (Machine Control Protocol) tools.\n"
            "IMPORTANT INSTRUCTIONS:\n"
            "1. When asked to perform an action, USE THE APPROPRIATE TOOL.\n"
            "2. Your response for a tool call MUST be in this exact format, with no other text:\n"
            "TOOL: <tool_name>\n"
            "ARGS: <json_args>\n\n"
        )
        for t in tools:
            system_prompt += f"- {t.name}: {t.description}\n"
            if t.input_schema.get("properties"):
                system_prompt += "  Parameters:\n"
                for param_name, param_info in t.input_schema.get("properties", {}).items():
                    required = "required" if param_name in t.input_schema.get("required", []) else "optional"
                    system_prompt += f"    - {param_name} ({required}): {param_info.get('description', '')}\n"
        
        # Prepend the system prompt to the message history.
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        # Run the synchronous SDK call in a thread.
        response = await asyncio.to_thread(
            self.client.chat,
            model=self.model_name,
            messages=full_messages,
        )
        content = response["message"]["content"]
        
        # Manually parse the text response for tool calls in the "TOOL:"/"ARGS:" format.
        if "TOOL:" in content:
            try:
                tool_lines = content.split("\n")
                tool_name = None
                tool_args = {}
                for line in tool_lines:
                    if line.startswith("TOOL:"):
                        tool_name = line.replace("TOOL:", "").strip()
                    elif line.startswith("ARGS:"):
                        args_str = line.replace("ARGS:", "").strip()
                        tool_args = json.loads(args_str)
                
                if tool_name:
                    return LLMReply(text="", tool_calls=[{"name": tool_name, "args": tool_args}])

            except (json.JSONDecodeError, KeyError, Exception):
                # If parsing fails, fall through and return the raw text.
                pass

        return LLMReply(text=content, tool_calls=None)


class OpenAILLM(BaseLLM):
    """Adapter for OpenAI models like GPT-4."""
    def __init__(self, model_name: str = "gpt-4-turbo", **kwargs):
        """Initializes the asynchronous OpenAI client."""
        if not openai:
            _raise_import_error("openai")
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or .env file.")
        
        # This implementation uses the Async client.
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model_name = model_name

    async def chat(
        self, messages: List[Dict[str, str]], tools: List[ToolDef]
    ) -> LLMReply:
        """
        Sends a query to the OpenAI API.
        
        It formats tools into the JSON structure expected by the OpenAI API,
        makes the API call, and parses the response for tool calls.
        """
        tool_descs = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.input_schema,
                },
            }
            for t in tools
        ]

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tool_descs if tool_descs else None,
        )
        
        reply = response.choices[0].message
        tool_calls = []
        if reply.tool_calls:
            for tc in reply.tool_calls:
                tool_calls.append({
                    "name": tc.function.name,
                    "args": json.loads(tc.function.arguments)
                })

        return LLMReply(text=reply.content or "", tool_calls=tool_calls)


class ClaudeLLM(BaseLLM):
    """Adapter for Anthropic's Claude models."""
    def __init__(self, model_name: str = "claude-3-haiku-20240307", **kwargs):
        """Initializes the asynchronous Anthropic client."""
        if not anthropic:
            _raise_import_error("anthropic")

        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables or .env file.")

        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model_name = model_name

    async def chat(
        self, messages: List[Dict[str, str]], tools: List[ToolDef]
    ) -> LLMReply:
        """
        Sends a query to the Anthropic API.
        
        It separates the system prompt as required by the Claude API, formats the
        tools, makes the API call, and iterates through the response blocks to
        separate text from tool usage.
        """
        # Claude requires the system prompt to be a top-level parameter.
        system_prompt = "You are a helpful assistant."
        user_messages = [m for m in messages if m["role"] != "system"]
        
        tool_descs = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.input_schema,
            }
            for t in tools
        ]

        response = await self.client.messages.create(
            model=self.model_name,
            max_tokens=2048,
            system=system_prompt,
            messages=user_messages,
            tools=tool_descs if tool_descs else None,
        )
        
        text_content = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_content += block.text
            elif block.type == "tool_use":
                tool_calls.append({"name": block.name, "args": block.input})

        return LLMReply(text=text_content.strip(), tool_calls=tool_calls)


# --- LLM Factory ---

# The registry maps a provider name (used in the CLI) to its adapter class.
# This makes it easy to add new providers without changing the main script logic.
PROVIDER_REGISTRY = {
    "gemini": GeminiLLM,
    "ollama": OllamaLLM,
    "openai": OpenAILLM,
    "claude": ClaudeLLM,
}


# --- MCP Interaction ---

def find_server_py(server_name: str) -> str:
    """
    Locates the main server.py script for a given MCP server name.
    
    It searches in common directory structures (<repo>/<server_name>/src/ and
    <repo>/<server_name>/) to find the executable script.
    """
    repo_root = Path(__file__).resolve().parent.parent
    for search_path in [repo_root / server_name / "src", repo_root / server_name]:
        if search_path.exists():
            matches = list(search_path.rglob("server.py"))
            if matches:
                return str(matches[0])
    raise FileNotFoundError(f"Could not find server.py for {server_name}")


class MCPClient:
    """
    Manages the connection and interaction with a single MCP server.
    """
    def __init__(self, llm_adapter: BaseLLM):
        """Initializes the client with a specific LLM adapter."""
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm = llm_adapter
        self.tools: List[ToolDef] = []

    async def connect(self, server_script: str):
        """
        Starts the MCP server as a subprocess and establishes a connection.
        
        This method uses the stdio_client to run the server script and connect
        to its standard input/output. It then initializes the MCP session and
        retrieves the list of available tools from the server.
        """
        print(f"Starting server with stdio: {server_script}")
        params = StdioServerParameters(command=sys.executable, args=[server_script], env=os.environ)
        reader, writer = await self.exit_stack.enter_async_context(stdio_client(params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(reader, writer))
        
        await self.session.initialize()
        tool_list = await self.session.list_tools()
        
        # Standardize the retrieved tools into the internal ToolDef format.
        self.tools = [
            ToolDef(
                name=t.name,
                description=t.description,
                input_schema=t.inputSchema,
            )
            for t in tool_list.tools
        ]
        print("\nConnected. Tools available:")
        for tool in self.tools:
            print(f" * {tool.name}: {tool.description}")

    async def process_query(self, query: str) -> str:
        """
        Processes a single user query.
        
        This is the core logic loop:
        1. Send the user's query to the configured LLM.
        2. If the LLM returns tool calls, execute them via the MCP session.
        3. If the LLM returns text, return the text directly.
        4. Aggregate and return the results.
        """
        messages = [{"role": "user", "content": query}]
        
        try:
            llm_reply = await self.llm.chat(messages, self.tools)
            
            if llm_reply.tool_calls:
                final_parts = []
                for tool_call in llm_reply.tool_calls:
                    name, args = tool_call["name"], tool_call["args"]
                    print(f"[Calling tool {name} with args {args}]")
                    try:
                        tr = await self.session.call_tool(name, args)
                        raw_txt = tr.content[0].text if tr.content else "No content returned"
                        final_parts.append(f"[Called {name}: {raw_txt}]")
                    except Exception as e:
                        final_parts.append(f"[Error calling {name}: {e}]")
                return "\n".join(final_parts)
            else:
                return llm_reply.text

        except Exception as e:
            return f"Error during LLM processing: {e}"

    async def chat_loop(self):
        """Runs the main interactive read-eval-print loop (REPL) for the user."""
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


# --- Main Execution ---

def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    """
    Parses command-line arguments.
    
    It separates the main arguments (`--provider`, `--servers`) from any
    provider-specific arguments that appear after a `--`.
    """
    parser = argparse.ArgumentParser(description="Provider-agnostic MCP chat client.")
    parser.add_argument(
        "--provider",
        required=True,
        choices=PROVIDER_REGISTRY.keys(),
        help="The LLM provider to use.",
    )
    parser.add_argument(
        "--servers",
        required=True,
        help="Comma-separated list of MCP server names (e.g., Jarvis,HDF5).",
    )
    # Capture all args after '--' for the provider
    return parser.parse_known_args()


def get_provider_kwargs(provider_args: List[str]) -> Dict[str, Any]:
    """
    Converts a list of provider-specific arguments into a keyword argument dict.
    Example: `--model=llama3` becomes `{'model': 'llama3'}`.
    """
    kwargs = {}
    for arg in provider_args:
        if arg.startswith("--"):
            key_value = arg[2:].split("=", 1)
            key = key_value[0].replace("-", "_")
            kwargs[key] = key_value[1] if len(key_value) > 1 else True
    return kwargs


async def async_main():
    """
    The main asynchronous entry point for the script.
    
    Orchestrates the entire process:
    1. Parses command-line arguments.
    2. Initializes the selected LLM provider adapter.
    3. Iterates through the requested servers, creating a client session for each.
    """
    args, provider_args = parse_args()
    
    provider_class = PROVIDER_REGISTRY.get(args.provider)
    if not provider_class:
        print(f"Error: Provider '{args.provider}' not found.")
        sys.exit(1)
        
    provider_kwargs = get_provider_kwargs(provider_args)
    
    try:
        llm_adapter = provider_class(**provider_kwargs)
    except (ImportError, ValueError) as e:
        print(f"Error initializing provider '{args.provider}': {e}")
        sys.exit(1)

    server_names = [name.strip() for name in args.servers.split(",")]
    
    # A simple loop to connect to servers sequentially. A more advanced version
    # might run these sessions in parallel.
    for server_name in server_names:
        print(f"\n=== Connecting to {server_name} ===")
        try:
            server_py = find_server_py(server_name)
            client = MCPClient(llm_adapter)
            await client.connect(server_py)
            await client.chat_loop()
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred with server {server_name}: {e}", file=sys.stderr)
        finally:
            # The script will exit after the first chat session ends.
            print(f"Session with {server_name} ended.")


if __name__ == "__main__":
    # Standard Python entry point.
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nClient interrupted. Exiting.") 