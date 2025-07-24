---
title: Slurm MCP
description: "Slurm MCP is a Model Context Protocol server that enables LLMs to manage HPC workloads on Slurm-managed clusters with comprehensive job submission, monitoring, and resource management capabilities, featuring intelligent job scheduling, cluster monitoring, array job support, and interactive node a..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Slurm"
  icon="🖥️"
  category="System Management"
  description="Slurm MCP is a Model Context Protocol server that enables LLMs to manage HPC workloads on Slurm-managed clusters with comprehensive job submission, monitoring, and resource management capabilities, featuring intelligent job scheduling, cluster monitoring, array job support, and interactive node allocation for seamless high-performance computing workflows."
  version="1.0.0"
  actions={["submit_slurm_job", "check_job_status", "cancel_slurm_job", "list_slurm_jobs", "get_slurm_info", "get_job_details", "get_job_output", "get_queue_info", "submit_array_job", "get_node_info", "allocate_slurm_nodes", "deallocate_slurm_nodes", "get_allocation_status"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={["MCP", "Slurm", "HPC", "job-management", "cluster-monitoring", "workload-management", "scientific-computing", "high-performance-computing"]}
  license="MIT"
>

## Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "slurm-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
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
    "slurm-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add slurm-mcp -- uvx iowarp-mcps slurm
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "slurm-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Slurm run slurm-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Slurm run slurm-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Slurm run slurm-mcp --help
```

</details>

## Available Tools


### `submit_slurm_job`

Submit Slurm jobs with comprehensive resource specification and intelligent job optimization.

This powerful tool provides complete job submission ...

**Usage Example:**
```python
# Use submit_slurm_job function
result = submit_slurm_job()
print(result)
```


### `check_job_status`

Check comprehensive Slurm job status with advanced monitoring, performance insights, and intelligent analysis.

This powerful tool provides complet...

**Usage Example:**
```python
# Use check_job_status function
result = check_job_status()
print(result)
```


### `cancel_slurm_job`

Cancel Slurm jobs with intelligent resource cleanup and comprehensive lifecycle management.

This powerful tool provides complete job cancellation ...

**Usage Example:**
```python
# Use cancel_slurm_job function
result = cancel_slurm_job()
print(result)
```


### `list_slurm_jobs`

List and analyze Slurm jobs with comprehensive filtering, intelligent analysis, and optimization insights.

This powerful tool provides complete jo...

**Usage Example:**
```python
# Use list_slurm_jobs function
result = list_slurm_jobs()
print(result)
```


### `get_slurm_info`

Get comprehensive Slurm cluster information with intelligent analysis and optimization insights.

This powerful tool provides complete cluster anal...

**Usage Example:**
```python
# Use get_slurm_info function
result = get_slurm_info()
print(result)
```


### `get_job_details`

Get comprehensive Slurm job details with intelligent analysis and performance insights.

This powerful tool provides complete job information analy...

**Usage Example:**
```python
# Use get_job_details function
result = get_job_details()
print(result)
```


### `get_job_output`

Get comprehensive Slurm job output with intelligent analysis and content organization.

This powerful tool provides complete job output retrieval a...

**Usage Example:**
```python
# Use get_job_output function
result = get_job_output()
print(result)
```


### `get_queue_info`

Get comprehensive Slurm queue information with intelligent analysis and optimization insights.

This powerful tool provides complete queue analysis...

**Usage Example:**
```python
# Use get_queue_info function
result = get_queue_info()
print(result)
```


### `submit_array_job`

Submit Slurm array jobs with intelligent parallel optimization and comprehensive workflow management.

This powerful tool provides complete array j...

**Usage Example:**
```python
# Use submit_array_job function
result = submit_array_job()
print(result)
```


### `get_node_info`

Get comprehensive Slurm node information with intelligent analysis and resource optimization insights.

This powerful tool provides complete node a...

**Usage Example:**
```python
# Use get_node_info function
result = get_node_info()
print(result)
```


### `allocate_slurm_nodes`

Allocate Slurm nodes with intelligent resource optimization and comprehensive interactive session management.

This powerful tool provides complete...

**Usage Example:**
```python
# Use allocate_slurm_nodes function
result = allocate_slurm_nodes()
print(result)
```


### `deallocate_slurm_nodes`

Deallocate Slurm nodes with intelligent resource cleanup and optimization analysis.

This powerful tool provides complete node deallocation capabil...

**Usage Example:**
```python
# Use deallocate_slurm_nodes function
result = deallocate_slurm_nodes()
print(result)
```


### `get_allocation_status`

Get comprehensive Slurm allocation status with intelligent monitoring and performance insights.

This powerful tool provides complete allocation st...

**Usage Example:**
```python
# Use get_allocation_status function
result = get_allocation_status()
print(result)
```


## Examples

### 1. Job Submission and Monitoring
```
I need to submit a Python simulation script to Slurm with 16 cores and 32GB memory, then monitor its progress until completion.
```

**Tools called:**
- `submit_slurm_job` - Submit job with resource specification
- `check_job_status` - Monitor job progress and performance

This prompt will:
- Use `submit_slurm_job` to submit the Python script with specified resources
- Use `check_job_status` to continuously monitor job execution and performance
- Provide comprehensive job lifecycle management with intelligent optimization

### 2. Array Job Management
```
Submit an array job for parameter sweep analysis with 100 tasks, each requiring 4 cores and 8GB memory, then check the overall progress.
```

**Tools called:**
- `submit_array_job` - Submit parallel array job
- `list_slurm_jobs` - Monitor array job progress
- `get_job_details` - Get detailed array job information

This prompt will:
- Use `submit_array_job` to create a high-throughput parameter sweep with intelligent task distribution
- Use `list_slurm_jobs` to monitor overall array job progress and efficiency
- Use `get_job_details` to analyze individual task performance and optimization opportunities

### 3. Interactive Session Management
```
Allocate 2 compute nodes with 8 cores each for an interactive analysis session, then deallocate when finished.
```

**Tools called:**
- `allocate_slurm_nodes` - Allocate interactive nodes
- `get_node_info` - Check node status and resources
- `get_allocation_status` - Monitor allocation efficiency
- `deallocate_slurm_nodes` - Clean up allocated resources

This prompt will:
- Use `allocate_slurm_nodes` to request interactive compute resources with optimization
- Use `get_node_info` to verify node availability and resource status
- Use `get_allocation_status` to monitor allocation usage and efficiency
- Use `deallocate_slurm_nodes` to clean up resources when analysis is complete

### 4. Job Management and Cleanup
```
I have a long-running job that needs to be cancelled, and I want to retrieve the output from a completed job before cleaning up.
```

**Tools called:**
- `cancel_slurm_job` - Cancel running job with cleanup
- `get_job_output` - Retrieve completed job outputs
- `get_job_details` - Get final job performance metrics

This prompt will:
- Use `cancel_slurm_job` to safely terminate the running job with intelligent cleanup
- Use `get_job_output` to retrieve both stdout and stderr from completed jobs
- Use `get_job_details` to analyze final performance metrics and resource utilization

### 5. Comprehensive Cluster Analysis
```
Analyze the current cluster queue status, identify bottlenecks, and suggest optimal resource allocation for my pending jobs.
```

**Tools called:**
- `get_slurm_info` - Get cluster status and capacity
- `get_queue_info` - Analyze queue performance and bottlenecks
- `list_slurm_jobs` - Review pending job queue and priorities

This prompt will:
- Use `get_slurm_info` to assess overall cluster capacity and resource availability
- Use `get_queue_info` to analyze partition-specific queue performance and bottlenecks
- Use `list_slurm_jobs` to review pending jobs and identify optimization opportunities

### 6. HPC Workflow Optimization
```
I need to optimize my computational workflow by analyzing my recent job performance, understanding cluster utilization patterns, and planning future submissions with better resource allocation.
```

**Tools called:**
- `list_slurm_jobs` - Review recent job history and performance patterns
- `get_job_details` - Analyze specific job performance metrics
- `get_slurm_info` - Understand cluster capacity and optimization opportunities
- `get_queue_info` - Analyze queue performance for optimal timing

This prompt will:
- Use `list_slurm_jobs` to examine historical job performance and identify trends
- Use `get_job_details` to deep-dive into resource utilization and efficiency metrics
- Use `get_slurm_info` to understand cluster constraints and optimization opportunities
- Use `get_queue_info` to plan optimal submission timing and partition selection

</MCPDetail>
