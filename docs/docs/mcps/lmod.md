---
title: Lmod MCP
description: "Lmod MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to manage environment modules using the Lmod system. This server provides advanced module management capabilities, environment configuration tools, and HPC workflow support with seamless i..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Lmod"
  icon="📦"
  category="System Management"
  description="Lmod MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to manage environment modules using the Lmod system. This server provides advanced module management capabilities, environment configuration tools, and HPC workflow support with seamless integration with AI coding assistants."
  version="1.0.0"
  actions={["module_list", "module_avail", "module_show", "module_load", "module_unload", "module_swap", "module_spider", "module_save", "module_restore", "module_savelist"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={["lmod", "environment-modules", "module-management", "hpc", "scientific-computing", "supercomputing", "cluster-computing", "module-system"]}
  license="MIT"
>

## Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Lmod system installed and available in PATH
- HPC environment with module system access

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "lmod-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "lmod"]
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
    "lmod-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "lmod"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add lmod-mcp -- uvx iowarp-mcps lmod
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "lmod-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "lmod"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/lmod run lmod-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\lmod run lmod-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\lmod run lmod-mcp --help
```

</details>

## Available Tools


### `module_list`

List all currently loaded environment modules. Shows the active modules in your current shell environment.

**Usage Example:**
```python
# Use module_list function
result = module_list()
print(result)
```


### `module_avail`

Search for available modules that can be loaded. Optionally filter by name pattern (e.g., 'python', 'gcc/*', '*mpi*').

**Usage Example:**
```python
# Use module_avail function
result = module_avail()
print(result)
```


### `module_show`

Display detailed information about a specific module including its description, dependencies, environment variables it sets, and conflicts.

**Usage Example:**
```python
# Use module_show function
result = module_show()
print(result)
```


### `module_load`

Load one or more environment modules into the current session. Modules modify environment variables like PATH, LD_LIBRARY_PATH, etc.

**Usage Example:**
```python
# Use module_load function
result = module_load()
print(result)
```


### `module_unload`

Unload (remove) one or more currently loaded modules from the environment. Reverses the changes made by module load.

**Usage Example:**
```python
# Use module_unload function
result = module_unload()
print(result)
```


### `module_swap`

Swap one module for another (unload old_module and load new_module atomically). Useful for switching between different versions.

**Usage Example:**
```python
# Use module_swap function
result = module_swap()
print(result)
```


### `module_spider`

Search the entire module tree for modules matching a pattern. More comprehensive than module_avail, shows all versions and variants.

**Usage Example:**
```python
# Use module_spider function
result = module_spider()
print(result)
```


### `module_save`

Save the current set of loaded modules as a named collection for easy restoration later.

**Usage Example:**
```python
# Use module_save function
result = module_save()
print(result)
```


### `module_restore`

Restore a previously saved module collection, loading all modules that were saved in that collection.

**Usage Example:**
```python
# Use module_restore function
result = module_restore()
print(result)
```


### `module_savelist`

List all saved module collections available for restoration.

**Usage Example:**
```python
# Use module_savelist function
result = module_savelist()
print(result)
```


## Examples

### 1. HPC Development Environment Setup
```
Set up my development environment by loading the latest GCC compiler, Python 3.9, and OpenMPI. Save this configuration as 'dev_env' for future use.
```

**Tools called:**
- `module_avail` - Search for available versions
- `module_load` - Load development tools
- `module_save` - Save configuration as collection

This prompt will:
- Use `module_avail` to find latest versions of GCC, Python, and OpenMPI
- Load required modules using `module_load` with dependency resolution
- Save the configuration using `module_save` for reproducible environments
- Provide complete development environment setup

### 2. Scientific Computing Environment
```
I need to switch from Intel compilers to GNU compilers for my simulation. Show me what's currently loaded, find GNU alternatives, and make the switch safely.
```

**Tools called:**
- `module_list` - Show current environment
- `module_avail` - Find GNU compiler alternatives
- `module_swap` - Switch compiler toolchains
- `module_show` - Verify new configuration

This prompt will:
- List current modules using `module_list`
- Search for GNU alternatives using `module_avail`
- Perform safe compiler switch using `module_swap`
- Verify configuration using `module_show`

### 3. Reproducible Research Environment
```
Create a reproducible environment for my research project by restoring my 'research_v2' module collection and verifying all dependencies are properly loaded.
```

**Tools called:**
- `module_savelist` - List available collections
- `module_restore` - Restore research environment
- `module_list` - Verify loaded modules

This prompt will:
- List available collections using `module_savelist`
- Restore specific environment using `module_restore`
- Verify environment using `module_list`
- Ensure reproducible research conditions

### 4. Module Discovery and Analysis
```
I'm looking for machine learning libraries and frameworks. Search the module system comprehensively and show me detailed information about the most relevant options.
```

**Tools called:**
- `module_spider` - Comprehensive module search
- `module_avail` - Search for ML-related modules
- `module_show` - Get detailed module information

This prompt will:
- Perform comprehensive search using `module_spider`
- Find ML-related modules using `module_avail`
- Extract detailed information using `module_show`
- Provide comprehensive module discovery and analysis

### 5. Environment Cleanup and Optimization
```
Clean up my current module environment by unloading unnecessary modules and optimizing for performance computing workflows.
```

**Tools called:**
- `module_list` - Assess current environment
- `module_show` - Analyze module dependencies
- `module_unload` - Remove unnecessary modules

This prompt will:
- Assess current environment using `module_list`
- Analyze dependencies using `module_show`
- Remove unnecessary modules using `module_unload`
- Optimize environment for performance computing

</MCPDetail>
