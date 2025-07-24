# Slurm MCP - HPC Job Management for LLMs


## Description

Slurm MCP is a Model Context Protocol server that enables LLMs to manage HPC workloads on Slurm-managed clusters with comprehensive job submission, monitoring, and resource management capabilities, featuring intelligent job scheduling, cluster monitoring, array job support, and interactive node allocation for seamless high-performance computing workflows.


## 🛠️ Installation

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

## Capabilities

### `submit_slurm_job`
**Description**: Submit a job script to Slurm scheduler with advanced resource specification and intelligent optimization.

**Parameters**:
- `script_path` (str): Parameter for script_path
- `cores` (int, optional): Parameter for cores (default: 1)
- `memory` (str, optional): Parameter for memory (default: 1GB)
- `time_limit` (str, optional): Parameter for time_limit (default: 01:00:00)
- `job_name` (str, optional): Parameter for job_name
- `partition` (str, optional): Parameter for partition

**Returns**: Dictionary containing comprehensive job submission results with scheduling insights

### `check_job_status`
**Description**: Check comprehensive status of a Slurm job with advanced monitoring and intelligent analysis.

**Parameters**:
- `job_id` (str): Parameter for job_id

**Returns**: Dictionary containing comprehensive job status with performance insights and optimization recommendations

### `cancel_slurm_job`
**Description**: Cancel a Slurm job.

**Parameters**:
- `job_id` (str): Parameter for job_id

**Returns**: Dictionary with cancellation results

### `list_slurm_jobs`
**Description**: List Slurm jobs with optional filtering.

**Parameters**:
- `user` (str, optional): Parameter for user
- `state` (str, optional): Parameter for state

**Returns**: Dictionary with list of jobs

### `get_slurm_info`
**Description**: Get information about the Slurm cluster.

**Returns**: Dictionary with cluster information

### `get_job_details`
**Description**: Get detailed information about a Slurm job.

**Parameters**:
- `job_id` (str): Parameter for job_id

**Returns**: Dictionary with detailed job information

### `get_job_output`
**Description**: Get job output content.

**Parameters**:
- `job_id` (str): Parameter for job_id
- `output_type` (str, optional): Parameter for output_type (default: stdout)

**Returns**: Dictionary with job output content

### `get_queue_info`
**Description**: Get job queue information.

**Parameters**:
- `partition` (str, optional): Parameter for partition

**Returns**: Dictionary with queue information

### `submit_array_job`
**Description**: Submit an array job to Slurm scheduler.

**Parameters**:
- `script_path` (str): Parameter for script_path
- `array_range` (str): Parameter for array_range
- `cores` (int, optional): Parameter for cores (default: 1)
- `memory` (str, optional): Parameter for memory (default: 1GB)
- `time_limit` (str, optional): Parameter for time_limit (default: 01:00:00)
- `job_name` (str, optional): Parameter for job_name
- `partition` (str, optional): Parameter for partition

**Returns**: Dictionary with array job submission results

### `get_node_info`
**Description**: Get cluster node information.

**Returns**: Dictionary with node information

### `allocate_slurm_nodes`
**Description**: Allocate Slurm nodes using salloc command.

**Parameters**:
- `nodes` (int, optional): Parameter for nodes (default: 1)
- `cores` (int, optional): Parameter for cores (default: 1)
- `memory` (str, optional): Parameter for memory
- `time_limit` (str, optional): Parameter for time_limit (default: 01:00:00)
- `partition` (str, optional): Parameter for partition
- `job_name` (str, optional): Parameter for job_name
- `immediate` (bool, optional): Parameter for immediate (default: False)

**Returns**: Dictionary with allocation information

### `deallocate_slurm_nodes`
**Description**: Deallocate Slurm nodes by canceling the allocation.

**Parameters**:
- `allocation_id` (str): Parameter for allocation_id

**Returns**: Dictionary with deallocation status

### `get_allocation_status`
**Description**: Get status of a node allocation.

**Parameters**:
- `allocation_id` (str): Parameter for allocation_id

**Returns**: Dictionary with allocation status information
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