---
title: Darshan MCP
description: "Darshan MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to analyze HPC application I/O performance through Darshan profiler trace files. This server provides advanced I/O analysis capabilities, performance bottleneck identification, and comp..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Darshan"
  icon="⚡"
  category="Utilities"
  description="Darshan MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to analyze HPC application I/O performance through Darshan profiler trace files. This server provides advanced I/O analysis capabilities, performance bottleneck identification, and comprehensive reporting tools with seamless integration with AI coding assistants."
  version="0.1.0"
  actions={["load_darshan_log", "get_job_summary", "analyze_file_access_patterns", "get_io_performance_metrics", "analyze_posix_operations", "analyze_mpiio_operations", "identify_io_bottlenecks", "get_timeline_analysis", "compare_darshan_logs", "generate_io_summary_report", "load_darshan_log", "get_job_summary", "analyze_file_access_patterns", "get_io_performance_metrics", "analyze_posix_operations", "analyze_mpiio_operations", "identify_io_bottlenecks", "get_timeline_analysis", "compare_darshan_logs", "generate_io_summary_report"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={[]}
  license="MIT"
>

## Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Darshan tools (`darshan-parser` in PATH)
- Python libraries: numpy, pandas, matplotlib

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "darshan-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "darshan"]
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
    "darshan-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "darshan"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add darshan-mcp -- uvx iowarp-mcps darshan
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "darshan-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "darshan"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Darshan run darshan-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Darshan run darshan-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Darshan run darshan-mcp --help
```

</details>

## Available Tools


### `load_darshan_log`

Load and parse a Darshan log file to extract I/O performance metrics and metadata. Returns basic information about the trace file including job det...

**Usage Example:**
```python
# Use load_darshan_log function
result = load_darshan_log()
print(result)
```


### `get_job_summary`

Get comprehensive job-level summary from a loaded Darshan log including execution time, number of processes, total I/O volume, and performance metr...

**Usage Example:**
```python
# Use get_job_summary function
result = get_job_summary()
print(result)
```


### `analyze_file_access_patterns`

Analyze file access patterns from the trace including which files were accessed, access types (read/write), sequential vs random access patterns, a...

**Usage Example:**
```python
# Use analyze_file_access_patterns function
result = analyze_file_access_patterns()
print(result)
```


### `get_io_performance_metrics`

Extract detailed I/O performance metrics including bandwidth, IOPS, average request sizes, and timing information for read and write operations.

**Usage Example:**
```python
# Use get_io_performance_metrics function
result = get_io_performance_metrics()
print(result)
```


### `analyze_posix_operations`

Analyze POSIX I/O operations from the trace including read/write system calls, file operations (open, close, seek), and their frequency and timing ...

**Usage Example:**
```python
# Use analyze_posix_operations function
result = analyze_posix_operations()
print(result)
```


### `analyze_mpiio_operations`

Analyze MPI-IO operations if present in the trace, including collective vs independent operations, file view usage, and MPI-IO specific performance...

**Usage Example:**
```python
# Use analyze_mpiio_operations function
result = analyze_mpiio_operations()
print(result)
```


### `identify_io_bottlenecks`

Identify potential I/O performance bottlenecks by analyzing access patterns, file system usage, small vs large I/O operations, and synchronization ...

**Usage Example:**
```python
# Use identify_io_bottlenecks function
result = identify_io_bottlenecks()
print(result)
```


### `get_timeline_analysis`

Generate timeline analysis showing I/O activity over time, including peak I/O periods, idle times, and temporal patterns in file access.

**Usage Example:**
```python
# Use get_timeline_analysis function
result = get_timeline_analysis()
print(result)
```


### `compare_darshan_logs`

Compare two Darshan log files to identify differences in I/O patterns, performance changes, and behavioral variations between different runs or con...

**Usage Example:**
```python
# Use compare_darshan_logs function
result = compare_darshan_logs()
print(result)
```


### `generate_io_summary_report`

Generate a comprehensive I/O summary report combining all analysis results into a human-readable format with key findings, performance insights, an...

**Usage Example:**
```python
# Use generate_io_summary_report function
result = generate_io_summary_report()
print(result)
```


### `load_darshan_log`

Load and parse a Darshan log file to extract I/O performance metrics and metadata. Returns basic information about the trace file including job det...

**Usage Example:**
```python
# Use load_darshan_log function
result = load_darshan_log()
print(result)
```


### `get_job_summary`

Get comprehensive job-level summary from a loaded Darshan log including execution time, number of processes, total I/O volume, and performance metr...

**Usage Example:**
```python
# Use get_job_summary function
result = get_job_summary()
print(result)
```


### `analyze_file_access_patterns`

Analyze file access patterns from the trace including which files were accessed, access types (read/write), sequential vs random access patterns, a...

**Usage Example:**
```python
# Use analyze_file_access_patterns function
result = analyze_file_access_patterns()
print(result)
```


### `get_io_performance_metrics`

Extract detailed I/O performance metrics including bandwidth, IOPS, average request sizes, and timing information for read and write operations.

**Usage Example:**
```python
# Use get_io_performance_metrics function
result = get_io_performance_metrics()
print(result)
```


### `analyze_posix_operations`

Analyze POSIX I/O operations from the trace including read/write system calls, file operations (open, close, seek), and their frequency and timing ...

**Usage Example:**
```python
# Use analyze_posix_operations function
result = analyze_posix_operations()
print(result)
```


### `analyze_mpiio_operations`

Analyze MPI-IO operations if present in the trace, including collective vs independent operations, file view usage, and MPI-IO specific performance...

**Usage Example:**
```python
# Use analyze_mpiio_operations function
result = analyze_mpiio_operations()
print(result)
```


### `identify_io_bottlenecks`

Identify potential I/O performance bottlenecks by analyzing access patterns, file system usage, small vs large I/O operations, and synchronization ...

**Usage Example:**
```python
# Use identify_io_bottlenecks function
result = identify_io_bottlenecks()
print(result)
```


### `get_timeline_analysis`

Generate timeline analysis showing I/O activity over time, including peak I/O periods, idle times, and temporal patterns in file access.

**Usage Example:**
```python
# Use get_timeline_analysis function
result = get_timeline_analysis()
print(result)
```


### `compare_darshan_logs`

Compare two Darshan log files to identify differences in I/O patterns, performance changes, and behavioral variations between different runs or con...

**Usage Example:**
```python
# Use compare_darshan_logs function
result = compare_darshan_logs()
print(result)
```


### `generate_io_summary_report`

Generate a comprehensive I/O summary report combining all analysis results into a human-readable format with key findings, performance insights, an...

**Usage Example:**
```python
# Use generate_io_summary_report function
result = generate_io_summary_report()
print(result)
```


## Examples

### 1. HPC Application Performance Analysis
```
Analyze the I/O performance of my application using the Darshan log at /data/app_trace.darshan. Identify bottlenecks and provide optimization recommendations.
```

**Tools called:**
- `load_darshan_log` - Parse the Darshan trace file
- `get_job_summary` - Extract job-level statistics
- `identify_io_bottlenecks` - Find performance issues
- `get_io_performance_metrics` - Calculate detailed metrics

This prompt will:
- Use `load_darshan_log` to parse the trace file and extract metadata
- Generate job summary using `get_job_summary` for runtime and I/O statistics
- Identify performance bottlenecks using `identify_io_bottlenecks`
- Provide comprehensive performance analysis with optimization recommendations

### 2. I/O Pattern Optimization Study
```
Compare the I/O patterns between /data/before_opt.darshan and /data/after_opt.darshan to validate our optimization efforts and measure performance improvements.
```

**Tools called:**
- `analyze_file_access_patterns` - Analyze access patterns for both files
- `compare_darshan_logs` - Compare performance metrics
- `get_io_performance_metrics` - Extract detailed performance data

This prompt will:
- Analyze access patterns using `analyze_file_access_patterns` for both traces
- Compare performance metrics using `compare_darshan_logs`
- Extract detailed metrics using `get_io_performance_metrics`
- Provide comprehensive optimization validation and improvement quantification

### 3. MPI-IO Collective Performance Analysis
```
Examine the MPI-IO operations in /data/parallel_app.darshan, focusing on collective vs independent I/O patterns and their impact on overall performance.
```

**Tools called:**
- `analyze_mpiio_operations` - Analyze MPI-IO patterns
- `get_timeline_analysis` - Understand temporal patterns
- `generate_io_summary_report` - Create comprehensive report

This prompt will:
- Analyze MPI-I/O operations using `analyze_mpiio_operations`
- Generate temporal analysis using `get_timeline_analysis`
- Create detailed report using `generate_io_summary_report`
- Provide insights into collective I/O efficiency and optimization opportunities

### 4. POSIX System Call Analysis
```
Investigate the POSIX I/O operations in /data/serial_app.darshan to understand file access patterns and identify potential optimizations for system call efficiency.
```

**Tools called:**
- `analyze_posix_operations` - Examine POSIX system calls
- `analyze_file_access_patterns` - Study file access behavior
- `identify_io_bottlenecks` - Find system-level bottlenecks

This prompt will:
- Analyze POSIX operations using `analyze_posix_operations`
- Study file access patterns using `analyze_file_access_patterns`
- Identify bottlenecks using `identify_io_bottlenecks`
- Provide system call optimization recommendations

### 5. Comprehensive I/O Performance Report
```
Generate a complete I/O performance analysis report for /data/production_app.darshan including all metrics, visualizations, and recommendations for our production environment.
```

**Tools called:**
- `load_darshan_log` - Load and validate trace file
- `generate_io_summary_report` - Create comprehensive analysis
- `get_timeline_analysis` - Add temporal performance data

This prompt will:
- Load and validate trace using `load_darshan_log`
- Generate complete report using `generate_io_summary_report`
- Add timeline analysis using `get_timeline_analysis`
- Provide production-ready performance assessment with actionable insights

</MCPDetail>
