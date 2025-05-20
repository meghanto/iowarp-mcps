## Detailed Explanation of `client.py`

The `client.py` script is an asynchronous client implementation that interacts with an MCP (Modular Command Processor) server. It integrates Google's Gemini AI to process natural language queries and execute server tools when needed. Below is a comprehensive breakdown of its components and workflows.

---

### **1. Initialization \& Configuration**

```python
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from google.genai import types
import json
from dotenv import load_dotenv
import os 

load_dotenv()  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=GEMINI_API_KEY)
```

- **Environment Setup**: Loads environment variables from `.env` file, specifically the `GEMINI_API_KEY` for AI integration.
- **Gemini Client**: Initializes Google's Generative AI client with the API key.
- **Async Infrastructure**: Uses `asyncio` and `AsyncExitStack` for managing asynchronous connections.

---

### **2. Core Class: `MCPClient`**

#### **a. Initialization**

```python
class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.gemini = client
```

- **Session Management**: Maintains a `ClientSession` object for server communication.
- **Resource Handling**: Uses `AsyncExitStack` for clean resource cleanup.
- **AI Integration**: Stores the Gemini client as `self.gemini`.

---

### **3. Key Methods**

#### **a. `connect_to_server()`**

```python
async def connect_to_server(self, server_script_path: str):
    # Validation and parameter setup
    command = "python" if is_python else "node"
    server_params = StdioServerParameters(command=command, args=[server_script_path])
    
    # Connection establishment
    stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
    self.session = await self.exit_stack.enter_async_context(ClientSession(...))
    
    # Tool discovery
    response = await self.session.list_tools()
    print("Connected with tools:", [tool.name for tool in response.tools])
```

- **Server Validation**: Ensures server script is either `.py` (Python) or `.js` (Node.js).
- **Transport Setup**: Creates stdio-based communication channel.
- **Tool Enumeration**: Lists available server tools after connection.


#### **b. `process_query()`**

```python
async def process_query(self, query: str) -&gt; str:
    messages = [{"role": "user", "content": query}]
    
    # Tool schema construction
    available_tools = types.Tool(function_declarations=[...])
    config = types.GenerateContentConfig(tools=[available_tools])
    
    # AI processing
    response = self.gemini.models.generate_content(
        model="gemini-2.0-flash", 
        contents=[query],
        config=config
    )
    
    # Response handling
    for candidate in response.candidates:
        for part in content.parts:
            if function_call := part.function_call:
                # Tool execution
                result = await self.session.call_tool(function_call.name, function_call.args)
                # Result processing
                list_result = json.loads(...)['text']
                messages.append({"role": "user", "content": list_result})
```

- **AI Integration**: Uses Gemini 2.0 Flash model for query processing.
- **Dynamic Tool Handling**:
    - Constructs tool schema from server metadata
    - Detects function calls in AI responses
    - Executes tools through `call_tool()`
- **Context Management**: Maintains conversation history in `messages`.


#### **c. `chat_loop()`**

```python
async def chat_loop(self):
    while True:
        query = input("Query: ").strip()
        if query.lower() == 'quit': break
        response = await self.process_query(query)
        print(response)
```

- **REPL Interface**: Implements Read-Eval-Print Loop for interactive usage.
- **Exit Handling**: Breaks loop on `quit` command.

---

### **4. Execution Flow**

```python
async def main():
    client = MCPClient()
    await client.connect_to_server(sys.argv[^1])
    await client.chat_loop()

if __name__ == "__main__":
    asyncio.run(main())
```

- **Argument Handling**: Requires server script path as command-line argument.
- **Lifecycle Management**:

1. Server connection
2. Interactive chat loop
3. Clean resource cleanup

---

### **5. Key Features**

| Component | Description |
| :-- | :-- |
| AI Integration | Uses Gemini 2.0 Flash model for natural language understanding |
| Dynamic Tool Use | Automatically detects and executes server tools based on AI recommendations |
| Secure Connection | Stdio transport ensures isolated communication with server processes |
| Context Awareness | Maintains conversation history for multi-turn interactions |
| Error Handling | Gracefully captures and displays errors during tool execution |

---

### **6. Workflow Diagram**

```
User Input → Gemini Processing → Tool Detection → Server Execution → Result Integration → Output
```

1. **Input**: User enters natural language query
2. **AI Analysis**: Gemini determines if tool usage is required
3. **Tool Execution**: Client calls appropriate server tool with parsed parameters
4. **Result Integration**: Tool outputs are fed back into conversation context
5. **Output Generation**: Final response combines AI text and tool results
