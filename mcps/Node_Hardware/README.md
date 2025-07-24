# Node Hardware MCP - System Monitoring for LLMs


## Description

Node Hardware MCP is a Model Context Protocol server that enables LLMs to monitor and analyze system hardware information including CPU specifications, memory usage, disk performance, network interfaces, GPU details, and sensor data for both local and remote nodes via SSH connections, providing comprehensive hardware monitoring and performance analysis capabilities.


## 🛠️ Installation

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

## Capabilities

### `get_cpu_info`
**Description**: Get comprehensive CPU information including specifications, core configuration, frequency analysis, and performance metrics with thermal status and load analysis.

**Parameters**:
- None

**Returns**: Structured CPU information with performance insights including CPU model, core configuration, frequency analysis, cache information, thermal status, and optimization recommendations.

### `get_memory_info`
**Description**: Get comprehensive memory information including capacity, usage patterns, and performance characteristics with swap analysis and optimization recommendations.

**Parameters**:
- None

**Returns**: Detailed memory analysis including capacity metrics, usage patterns, swap configuration, performance characteristics, health indicators, and efficiency recommendations.

### `get_system_info`
**Description**: Get comprehensive system information including operating system details, uptime analysis, user management, configuration, and platform information with security status.

**Parameters**:
- None

**Returns**: Complete system overview including OS details, uptime metrics, user information, platform configuration, security status, and system optimization insights.

### `get_disk_info`
**Description**: Get comprehensive disk information including storage devices, usage analysis, I/O performance, health monitoring, file systems, and predictive maintenance recommendations.

**Parameters**:
- None

**Returns**: Detailed storage analysis including device specifications, usage metrics, I/O performance, health indicators, file system information, and maintenance recommendations.

### `get_network_info`
**Description**: Get comprehensive network information including interfaces, connections, and bandwidth analysis with protocol statistics and security monitoring.

**Parameters**:
- None

**Returns**: Complete network analysis including interface details, IP configuration, connection statistics, bandwidth metrics, protocol analysis, and security recommendations.

### `get_gpu_info`
**Description**: Get comprehensive GPU information including specifications, memory analysis, thermal monitoring, performance metrics, driver information, and compute capabilities.

**Parameters**:
- None

**Returns**: Detailed GPU analysis including specifications, memory usage, thermal status, performance metrics, driver information, compute capabilities, and optimization recommendations.

### `get_sensor_info`
**Description**: Get comprehensive sensor information including temperature monitoring, fan control, voltage analysis, hardware health indicators, and thermal management with predictive maintenance.

**Parameters**:
- None

**Returns**: Complete sensor analysis including temperature readings, fan speeds, voltage levels, hardware health metrics, thermal management status, and predictive maintenance insights.

### `get_process_info`
**Description**: Get comprehensive process information including running processes, resource consumption, process hierarchy, performance metrics, and system load analysis.

**Parameters**:
- None

**Returns**: Detailed process analysis including active processes, resource utilization, process relationships, performance metrics, system load indicators, and optimization recommendations.

### `get_performance_info`
**Description**: Get comprehensive performance information including real-time monitoring, bottleneck analysis, optimization recommendations, and trend analysis for system performance assessment.

**Parameters**:
- None

**Returns**: Complete performance analysis including real-time metrics, bottleneck identification, performance trends, optimization suggestions, and system efficiency recommendations.

### `get_remote_node_info`
**Description**: Get comprehensive remote node hardware and system information via SSH with advanced filtering and intelligent analysis for distributed system monitoring.

**Parameters**:
- `hostname` (str): Target hostname or IP address for remote collection (required)
- `username` (str, optional): SSH username for remote authentication
- `port` (int): SSH port number for remote connection (default: 22)
- `ssh_key` (str, optional): Path to SSH private key file for authentication
- `timeout` (int): SSH connection timeout in seconds (default: 30)
- `components` (List[str], optional): List of specific components to include in collection
- `exclude_components` (List[str], optional): List of specific components to exclude from collection
- `include_performance` (bool): Whether to include real-time performance analysis (default: True)
- `include_health` (bool): Whether to include health assessment and predictive maintenance insights (default: True)

**Returns**: Comprehensive remote hardware analysis including hardware data, collection metadata, performance analysis, health assessment, SSH connection info, and optimization recommendations.

### `health_check`
**Description**: Perform comprehensive health check and system diagnostics with advanced capability verification, system compatibility testing, and performance assessment.

**Parameters**:
- None

**Returns**: Complete health assessment including server status, capability verification, system compatibility, performance metrics, diagnostic insights, and optimization recommendations with predictive maintenance guidance.

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
