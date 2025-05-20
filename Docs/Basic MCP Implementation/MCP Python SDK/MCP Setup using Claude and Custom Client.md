# MCP Setup using Claude and Custom Client

## Building an MCP Server

- Once you have setup uv
    - Create a new uv project
        
        ```powershell
        uv init mcp-py-2
        cd mcp-py-2
        ```
        
    - Create virtual environment and activate it
        
        ```powershell
        uv venv
        source .venv/bin/activate  # On Windows: .venv\\\\Scripts\\\\activate
        ```
        
    - Install dependencies
        
        ```powershell
        uv add "mcp[cli]" httpx
        ```
        
    - Create a new python file in newly created project root directory.
        
        ```python
        from typing import Any
        import httpx
        from mcp.server.fastmcp import FastMCP
        
        # Initialize FastMCP server
        mcp = FastMCP("weather")
        
        # Constants
        NWS_API_BASE = "<https://api.weather.gov>"
        USER_AGENT = "weather-app/1.0"
        
        async def make_nws_request(url: str) -> dict[str, Any] | None:
            """Make a request to the NWS API with proper error handling."""
            headers = {
                "User-Agent": USER_AGENT,
                "Accept": "application/geo+json"
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, headers=headers, timeout=30.0)
                    response.raise_for_status()
                    return response.json()
                except Exception:
                    return None
        
        def format_alert(feature: dict) -> str:
            """Format an alert feature into a readable string."""
            props = feature["properties"]
            return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
        """
        
        @mcp.tool()
        async def get_alerts(state: str) -> str:
            """Get weather alerts for a US state.
        
            Args:
                state: Two-letter US state code (e.g., CA, NY)
            """
            url = f"{NWS_API_BASE}/alerts/active/area/{state}"
            data = await make_nws_request(url)
        
            if not data or "features" not in data:
                return "Unable to fetch alerts or no alerts found."
        
            if not data["features"]:
                return "No active alerts for this state."
        
            alerts = [format_alert(feature) for feature in data["features"]]
            return "\\\\n---\\\\n".join(alerts)
        
        @mcp.tool()
        async def get_forecast(latitude: float, longitude: float) -> str:
            """Get weather forecast for a location.
        
            Args:
                latitude: Latitude of the location
                longitude: Longitude of the location
            """
            # First get the forecast grid endpoint
            points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
            points_data = await make_nws_request(points_url)
        
            if not points_data:
                return "Unable to fetch forecast data for this location."
        
            # Get the forecast URL from the points response
            forecast_url = points_data["properties"]["forecast"]
            forecast_data = await make_nws_request(forecast_url)
        
            if not forecast_data:
                return "Unable to fetch detailed forecast."
        
            # Format the periods into a readable forecast
            periods = forecast_data["properties"]["periods"]
            forecasts = []
            for period in periods[:5]:  # Only show next 5 periods
                forecast = f"""
        {period['name']}: Temperature: {period['temperature']}°{period['temperatureUnit']}
        Wind: {period['windSpeed']} {period['windDirection']}
        Forecast: {period['detailedForecast']}
        """
                forecasts.append(forecast)
        
            return "\\\\n---\\\\n".join(forecasts)
        
        if __name__ == "__main__":
            # Initialize and run the server
            mcp.run(transport='stdio')
        ```
        
    - Run the above script
        
        ```bash
        uv run weather.py
        ```
        

# **Connecting to Claude for Desktop**

### Step 1: Install Claude for Desktop

- Link: https://claude.ai/download

### Step 2: Configure Claude for Desktop

- Open your Claude for Desktop App configuration in a text editor: ( Shortcut key: ctrl+Comma)
    
    ![image.png](./assets/image%2013.png)
    
    - Go to developer tab
        
        ![image.png](./assets/image%2014.png)
        
    - Edit claude_desktop_config.json file
        
        ```bash
        {
          "mcpServers": {
            "weather": {
              "command": "uv",
              "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/PROJECT NAME",
                "run",
                "FILE_CREATED.PY"
              ]
            }
          }
        }
        ```
        

make sure to:

- Use the absolute path to your server directory
- Ensure the command matches your environment (e.g., `uv` or the full path to `uv`)

### Step 3: Restart Claude for Desktop

After saving the configuration, restart Claude for Desktop completely.

### Step 4: Test Your Server

Look for the hammer icon in the bottom right corner of the Claude for Desktop input box. Clicking it should show your server's tools.

![image.png](./assets/image%2015.png)

![image.png](./assets/image%2016.png)

You can now ask Claude questions like:

- "What's the weather in Chicago?"
- "What are the active weather alerts in Chicago?"
    
    ![image.png](./assets/image%2017.png)
    
    ![image.png](./assets/image%2018.png)
    
    ![image.png](./assets/image%2019.png)
    

# **Building a Custom MCP Client for Claude MCP Servers**

### Step 1: Set Up the Client Project

```bash
# Create project directory
uv init mcp-client
cd mcp-client

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\\\\Scripts\\\\activate

# Install required packages
uv add mcp anthropic python-dotenv

# Create our main file
touch client.py
```

### Step 2: Set Up Your API Key

Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=<your key here>
```

### Step 3: Implement the Client

Here's a basic client implementation (in `client.py`):

```python
import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp.client.stdio import ClientSession, StdioServerParameters, stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (py or js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')

        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(command=command, args=[server_script_path], env=None)

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\\\\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.input_schema
        } for tool in response.tools]

        # Initial Claude API call
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        # Process response and handle tool calls
        final_text = []
        assistant_message_content = []

        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                assistant_message_content.append(content)

                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result
                        }
                    ]
                })

                # Get next response from Claude
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages,
                    tools=available_tools
                )

                final_text.append(response.content[0].text)

        return "\\\\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\\\\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\\\\nQuery: ").strip()
                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\\\\n" + response)
            except Exception as e:
                print(f"\\\\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()

    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

Step 4: Run the Client

To use your client with your weather server:

```bash
uv run client.py /path/to/weather.py
```

## Citation

https://apidog.com/blog/mcp-servers-explained/#building-a-custom-mcp-client-for-claude-mcp-servers

https://claude.ai/download