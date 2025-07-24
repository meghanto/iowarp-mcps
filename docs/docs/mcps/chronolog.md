---
title: Chronolog MCP
description: "ChronoLog MCP is a comprehensive Model Context Protocol (MCP) server that integrates with ChronoLog, a scalable, high-performance distributed shared log store. This server enables Language Learning Models (LLMs) to capture, manage, and retrieve conversational interactions in a structured format w..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Chronolog"
  icon="⏰"
  category="Data Processing"
  description="ChronoLog MCP is a comprehensive Model Context Protocol (MCP) server that integrates with ChronoLog, a scalable, high-performance distributed shared log store. This server enables Language Learning Models (LLMs) to capture, manage, and retrieve conversational interactions in a structured format with enterprise-grade logging capabilities and real-time event processing."
  version="1.0.0"
  actions={["start_chronolog", "record_interaction", "stop_chronolog", "retrieve_interaction"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={["distributed logging", "chronolog", "event logging", "session management", "context sharing", "real-time", "model context protocol", "scientific data", "conversational ai", "high-performance", "shared log", "multi-client", "historical retrieval", "enterprise logging"]}
  license="MIT"
>

## Installation

### Requirements

- Python 3.11 or higher
- [py_chronolog_client](https://github.com/grc-iit/ChronoLog) Python package
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- ChronoLog deployment (see [setup guide](https://github.com/iowarp/scientific-mcps/blob/main/Chronolog/docs/Chronolog_setup.md))

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "chronolog-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "chronolog"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in VS Code</b></summary>

Add this to your VS Code MCP config file. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

```json
"mcp": {
  "servers": {
    "chronolog-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "chronolog"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add chronolog-mcp -- uvx iowarp-mcps chronolog
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "chronolog-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "chronolog"]
    }
  }
}
```

</details>

<details>
<summary><b>Manual Setup</b></summary>

**Linux/macOS:**
```bash
CLONE_DIR=$(pwd)
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Chronolog run chronolog-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Chronolog run chronolog-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Chronolog run chronolog-mcp --help
```

</details>

## Available Tools


### `start_chronolog`

Connects to ChronoLog, creates a chronicle, and acquires a story handle for logging interactions.

**Usage Example:**
```python
# Use start_chronolog function
result = start_chronolog()
print(result)
```


### `record_interaction`

Logs user messages and LLM responses to the active story with structured event formatting.

**Usage Example:**
```python
# Use record_interaction function
result = record_interaction()
print(result)
```


### `stop_chronolog`

Releases the story handle and cleanly disconnects from ChronoLog system.

**Usage Example:**
```python
# Use stop_chronolog function
result = stop_chronolog()
print(result)
```


### `retrieve_interaction`

Extracts logged records from specified chronicle and story, generates timestamped output files with filtering options.

**Usage Example:**
```python
# Use retrieve_interaction function
result = retrieve_interaction()
print(result)
```


## Examples

### 1. Session Logging and Analysis
```
Start logging our conversation, then after we discuss machine learning concepts, retrieve the interaction history for analysis.
```

**Tools called:**
- `start_chronolog` - Initialize logging session
- `record_interaction` - Log conversation events  
- `retrieve_interaction` - Generate interaction history

This prompt will:
- Use `start_chronolog` to create a new chronicle and story
- Automatically log interactions using `record_interaction`
- Extract conversation history using `retrieve_interaction`
- Provide structured session analysis

### 2. Multi-Session Context Sharing
```
Connect to the research chronicle and retrieve yesterday's discussion about neural networks to continue our conversation.
```

**Tools called:**
- `start_chronolog` - Connect to existing chronicle
- `retrieve_interaction` - Fetch historical interactions

This prompt will:
- Connect to existing research chronicle using `start_chronolog`
- Retrieve previous session data using `retrieve_interaction`
- Enable context continuation across sessions
- Support multi-client collaborative workflows

### 3. Structured Event Documentation
```
Begin recording our software design discussion, ensuring all architectural decisions and code examples are captured for future reference.
```

**Tools called:**
- `start_chronolog` - Begin structured logging
- `record_interaction` - Capture design decisions
- `stop_chronolog` - Complete session

This prompt will:
- Initialize structured event logging using `start_chronolog`
- Capture all conversation elements using `record_interaction`
- Maintain detailed architectural documentation
- Provide clean session termination using `stop_chronolog`

</MCPDetail>
