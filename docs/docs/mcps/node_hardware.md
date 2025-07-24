---
title: Node-Hardware MCP
description: "Node Hardware MCP is a Model Context Protocol server that enables LLMs to monitor and analyze system hardware information including CPU specifications, memory usage, disk performance, network interfaces, GPU details, and sensor data for both local and remote nodes via SSH connections, providing c..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Node-Hardware"
  icon="💻"
  category="Analysis & Visualization"
  description="Node Hardware MCP is a Model Context Protocol server that enables LLMs to monitor and analyze system hardware information including CPU specifications, memory usage, disk performance, network interfaces, GPU details, and sensor data for both local and remote nodes via SSH connections, providing comprehensive hardware monitoring and performance analysis capabilities."
  version="1.0.0"
  actions={["get_cpu_info", "get_memory_info", "get_system_info", "get_disk_info", "get_network_info", "get_gpu_info", "get_sensor_info", "get_process_info", "get_performance_info", "get_remote_node_info", "health_check"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={["hardware-monitoring", "system-analysis", "performance-metrics", "node-information", "ssh-monitoring", "remote-hardware", "mcp", "llm-integration", "infrastructure-monitoring", "distributed-systems"]}
  license="MIT"
>

## Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- SSH client (for remote node capabilities)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "node-hardware-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
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
    "node-hardware-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add node-hardware-mcp -- uvx iowarp-mcps node-hardware
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "node-hardware-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Node_Hardware run node-hardware-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Node_Hardware run node-hardware-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Node_Hardware run node-hardware-mcp --help
```

</details>

## Available Tools


### `get_cpu_info`

Get comprehensive CPU information including specifications, core configuration, frequency analysis, and performance metrics.

This tool provides de...

**Usage Example:**
```python
# Use get_cpu_info function
result = get_cpu_info()
print(result)
```


### `get_memory_info`

Get comprehensive memory information including capacity, usage patterns, and performance characteristics.

This tool provides detailed memory analy...

**Usage Example:**
```python
# Use get_memory_info function
result = get_memory_info()
print(result)
```


### `get_system_info`

Get comprehensive system information including operating system details, platform configuration, and system status.

This tool provides detailed sy...

**Usage Example:**
```python
# Use get_system_info function
result = get_system_info()
print(result)
```


### `get_disk_info`

Get comprehensive disk information including storage devices, partitions, and I/O performance metrics.

This tool provides detailed disk analysis i...

**Usage Example:**
```python
# Use get_disk_info function
result = get_disk_info()
print(result)
```


### `get_network_info`

Get comprehensive network information including interfaces, connections, and bandwidth analysis.

This tool provides detailed network analysis incl...

**Usage Example:**
```python
# Use get_network_info function
result = get_network_info()
print(result)
```


### `get_gpu_info`

Get comprehensive GPU information including specifications, memory, and compute capabilities.

This tool provides detailed GPU analysis including:
...

**Usage Example:**
```python
# Use get_gpu_info function
result = get_gpu_info()
print(result)
```


### `get_sensor_info`

Get sensor information including temperature, fan speeds, and thermal data.

This tool provides detailed sensor analysis including:
- **Temperature...

**Usage Example:**
```python
# Use get_sensor_info function
result = get_sensor_info()
print(result)
```


### `get_process_info`

Get process information including running processes and resource usage.

This tool provides detailed process analysis including:
- **Process List**...

**Usage Example:**
```python
# Use get_process_info function
result = get_process_info()
print(result)
```


### `get_performance_info`

Get real-time performance metrics including CPU, memory, and disk usage.

This tool provides comprehensive performance analysis including:
- **CPU ...

**Usage Example:**
```python
# Use get_performance_info function
result = get_performance_info()
print(result)
```


### `get_remote_node_info`

Get comprehensive remote node hardware and system information via SSH with advanced filtering and intelligent analysis.

This powerful tool provide...

**Usage Example:**
```python
# Use get_remote_node_info function
result = get_remote_node_info()
print(result)
```


### `health_check`

Perform comprehensive health check and system diagnostics with advanced capability verification.

This tool provides complete system health assessm...

**Usage Example:**
```python
# Use health_check function
result = health_check()
print(result)
```


## Examples

### 1. Local Hardware Overview
```
I need a comprehensive overview of my local system's hardware including CPU, memory, disk, and network components.
```

**Tools called:**
- `get_cpu_info` - Get detailed CPU specifications and performance metrics
- `get_memory_info` - Get memory capacity and usage analysis
- `get_disk_info` - Get storage device information and health status
- `get_network_info` - Get network interface and connection details
- `get_system_info` - Get operating system and platform information

This prompt will:
- Use multiple hardware-specific tools to gather comprehensive system information
- Provide detailed specifications for each hardware component
- Generate performance insights and optimization recommendations

### 2. Remote Server Monitoring
```
Monitor the hardware status of a remote server via SSH, focusing on CPU and memory utilization for performance analysis.
```

**Tools called:**
- `get_remote_node_info` - Connect to remote host with SSH authentication and collect CPU/memory data

This prompt will:
- Use `get_remote_node_info` with components filter for CPU and memory analysis
- Establish secure SSH connection to remote server
- Provide performance metrics and utilization analysis for targeted monitoring

### 3. GPU and Thermal Monitoring
```
Check GPU specifications and thermal sensors on both local and remote systems for machine learning workloads.
```

**Tools called:**
- `get_gpu_info` - Local GPU specifications and performance metrics
- `get_sensor_info` - Local thermal monitoring and hardware health
- `get_remote_node_info` - Remote GPU and thermal analysis via SSH

This prompt will:
- Use `get_gpu_info` and `get_sensor_info` for local GPU and thermal monitoring
- Use `get_remote_node_info` with GPU and sensor components for remote analysis
- Provide thermal management insights and performance optimization for ML workloads

### 4. System Health Assessment
```
Perform a comprehensive health check of system capabilities and verify all monitoring tools are working correctly.
```

**Tools called:**
- `health_check` - System health verification and diagnostic assessment
- `get_performance_info` - Performance monitoring and bottleneck analysis

This prompt will:
- Use `health_check` to verify all system monitoring capabilities
- Use `get_performance_info` to assess current system performance
- Provide diagnostic insights and capability verification results

### 5. Performance Bottleneck Analysis
```
Identify performance bottlenecks on a production server by analyzing CPU, memory, disk I/O, and running processes.
```

**Tools called:**
- `get_remote_node_info` - Remote performance analysis via SSH with comprehensive component collection
- `get_performance_info` - Real-time performance monitoring and bottleneck identification

This prompt will:
- Use `get_remote_node_info` with performance-focused component selection (CPU, memory, disk, processes)
- Use `get_performance_info` for detailed bottleneck analysis
- Provide optimization recommendations and performance improvement strategies

### 6. Storage and Network Analysis
```
Analyze storage health and network interface performance on multiple systems for infrastructure monitoring.
```

**Tools called:**
- `get_disk_info` - Local storage analysis and health monitoring
- `get_network_info` - Local network interface performance analysis
- `get_remote_node_info` - Remote storage and network monitoring via SSH

This prompt will:
- Use `get_disk_info` and `get_network_info` for local infrastructure analysis
- Use `get_remote_node_info` with disk and network components for remote monitoring
- Provide infrastructure health insights and performance optimization recommendations

</MCPDetail>
