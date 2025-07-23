# Slurm MCP Server

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)](https://github.com/modelcontextprotocol)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive Model Context Protocol (MCP) server for Slurm workload management implementation. This server provides comprehensive HPC job management and cluster monitoring capabilities through the Model Context Protocol, enabling users to submit jobs, monitor cluster resources, and manage workloads across Slurm-managed HPC systems with **intelligent job scheduling**, **beautiful output formatting**, and **workflow-first approach**.

## Key Features

### 🔧 **Comprehensive Job Management Tools**
Following MCP best practices, this server provides intelligent, contextual assistance for HPC workload management:

- **`submit_slurm_job`**: Submit jobs with intelligent resource optimization and performance prediction
- **`check_job_status`**: Monitor jobs with advanced analytics and optimization insights  
- **`cancel_slurm_job`**: Cancel jobs with intelligent resource cleanup and impact analysis
- **`list_slurm_jobs`**: List jobs with comprehensive filtering and workflow optimization
- **`get_slurm_info`**: Get cluster info with capacity planning and health assessment
- **`get_job_details`**: Get detailed job information with performance analysis
- **`get_job_output`**: Retrieve job outputs with intelligent organization
- **`get_queue_info`**: Analyze queues with scheduling optimization insights
- **`submit_array_job`**: Submit array jobs with parallel optimization and throughput analysis
- **`get_node_info`**: Get node information with resource availability analysis
- **`allocate_slurm_nodes`**: Allocate nodes with interactive session management
- **`deallocate_slurm_nodes`**: Deallocate nodes with resource cleanup optimization
- **`get_allocation_status`**: Monitor allocations with efficiency tracking

### 🚀 **Workflow-First Design**
- **Intelligent Analysis**: AI-powered insights and job optimization recommendations
- **Advanced Filtering**: Sophisticated job filtering and monitoring capabilities
- **Performance Optimization**: Resource utilization analysis with optimization strategies
- **Predictive Scheduling**: Smart job scheduling recommendations based on cluster state

### 🎨 **Beautiful Output Formatting**
- **Structured Layout**: Rich formatting with comprehensive job summaries and visual indicators
- **Comprehensive Insights**: Actionable recommendations and intelligent observations about job performance
- **Metadata Tracking**: Detailed job metadata and execution metrics
- **Error Handling**: Helpful error messages with troubleshooting suggestions

### 🌐 **Complete Slurm Integration**
- **Job Lifecycle**: Complete job submission, monitoring, and management workflow
- **Resource Management**: CPU, memory, time, and partition specification with validation
- **Queue Analysis**: Real-time queue monitoring and scheduling insights
- **Node Information**: Comprehensive node status and resource availability
- **Interactive Sessions**: Node allocation and management for interactive computing
- **Array Jobs**: High-throughput parallel job submission and management

### 🔒 **Enterprise Ready**
- **Input Validation**: Comprehensive validation of script paths and resource requirements
- **Error Handling**: Robust error handling with detailed error messages
- **Multiple Transports**: Support for both stdio and SSE (Server-Sent Events) transports
- **Streamlined Architecture**: Direct implementation imports for better performance and maintainability

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager  
- Linux/macOS environment (for optimal compatibility)
- Slurm workload manager installed and configured

## Installation and Setup

### Quick Start
```bash
# Navigate to Slurm directory
cd /path/to/scientific-mcps/Slurm

# Install and run with UV (recommended)
uv sync && uv run slurm-mcp
```

### Installation Methods

#### Method 1: UV Package Manager (Recommended)
```bash
# Install dependencies
uv sync

# Run the server
uv run slurm-mcp
```

#### Method 2: Traditional pip
```bash
# Install in development mode
pip install -e .

# Run the server
python -m src.server
```

#### Method 3: Direct Execution
```bash
# Run without installation (creates .venv automatically)
uv run slurm-mcp
```

## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Slurm MCP server, use the main `wrp.py` client. You will need to configure it to point to the Slurm server.

1.  **Configure:** Ensure that `Slurm` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Slurm
    ```

2.  **Run:** Start the client from the repository root with your desired configuration:
    ```bash
    # Example using the Gemini configuration 
    python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```

### Running the Server with Claude Desktop
Add to your Claude Desktop `settings.json`:
```json
{
  "mcpServers": {
    "slurm-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/scientific-mcps/Slurm",
        "run", 
        "slurm-mcp"
      ]
    }
  }
}
```

### **Claude CLI Integration**
```bash
claude add mcp slurm -- uv --directory ~/path/to/scientific-mcps/Slurm run slurm-mcp
```

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
## Usage Examples

### Job Submission (`submit_slurm_job`)

```python
# Submit a basic job with intelligent optimization
submit_slurm_job(script_path="my_job.sh", cores=4, memory="8GB")

# Submit with advanced resource specification
submit_slurm_job(
    script_path="simulation.sh",
    cores=16,
    memory="32GB", 
    time_limit="02:00:00",
    partition="compute"
)

# Submit with intelligent resource optimization
submit_slurm_job(
    script_path="analysis.py",
    cores=8,
    memory="16GB",
    job_name="data_analysis"
)
```

### Job Monitoring (`check_job_status`)

```python
# Monitor job with performance analysis
check_job_status(job_id="12345")

# Check status with optimization insights
check_job_status(job_id="67890")  # Returns performance metrics and recommendations
```

### Job Management (`list_slurm_jobs`)

```python
# List all jobs with analysis
list_slurm_jobs()

# List jobs with filtering and optimization insights
list_slurm_jobs(user="username", state="RUNNING")

# Analyze job queue with intelligent filtering
list_slurm_jobs(state="PENDING")  # Returns scheduling optimization insights
```

### Array Jobs (`submit_array_job`)

```python
# Submit array job with parallel optimization
submit_array_job(
    script_path="parallel_task.sh",
    array_range="1-100",
    cores=2,
    memory="4GB"
)

# High-throughput computing with optimization
submit_array_job(
    script_path="parameter_sweep.py",
    array_range="1-1000:10",
    cores=4,
    memory="8GB",
    time_limit="01:00:00"
)
```

### Interactive Sessions (`allocate_slurm_nodes`)

```python
# Allocate nodes for interactive work
allocate_slurm_nodes(nodes=1, cores=4, memory="8GB", time_limit="02:00:00")

# Interactive session with optimization
allocate_slurm_nodes(
    nodes=2,
    cores=8, 
    memory="16GB",
    partition="interactive"
)
```

## Development and Testing

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/test_capabilities.py
uv run pytest tests/test_implementation.py

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### Development Tools
```bash
# Format code
uv run black src tests

# Sort imports
uv run isort src tests

# Type checking
uv run mypy src

# Linting
uv run ruff check src tests
```

### Running the Server Standalone
For testing and development:

```bash
# Start the server (recommended)
uv run slurm-mcp

# Alternative methods
python -m src.server
python src/server.py
```

## Error Handling and Troubleshooting

The server provides comprehensive error handling with:

- **Detailed Error Messages**: Clear descriptions of what went wrong
- **Error Classifications**: Categorized error types for better understanding
- **Suggestions**: Actionable recommendations for resolving issues
- **Graceful Degradation**: Partial results when some operations fail
- **Intelligent Troubleshooting**: Context-aware troubleshooting guidance

### Common Issues and Solutions:

1. **Slurm Not Available**:
   - Ensure Slurm is installed and configured
   - Check Slurm service status
   - Verify user permissions for Slurm commands

2. **Permission Errors**:
   - Check file permissions for job scripts
   - Verify Slurm user permissions
   - Ensure proper cluster access rights

3. **Resource Allocation Issues**:
   - Check cluster resource availability
   - Verify partition access permissions
   - Review resource request parameters

## Performance Considerations

- **Local Operations**: Slurm command execution with intelligent caching
- **Job Submission**: Optimized job submission with validation and analysis
- **Resource Monitoring**: Efficient resource usage tracking and analysis
- **Intelligent Caching**: Smart caching for frequently accessed information
- **Parallel Processing**: Optimized data collection with concurrent operations

## Architecture

### Project Structure
```
Slurm/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── server.py                # Main MCP server with streamlined tools
│   └── implementation/          # Core implementation modules
│       ├── __init__.py
│       ├── job_submission.py    # Job submission functionality
│       ├── job_status.py        # Job status monitoring
│       ├── job_details.py       # Detailed job information
│       ├── job_output.py        # Job output management
│       ├── job_listing.py       # Job listing and filtering
│       ├── job_cancellation.py  # Job cancellation
│       ├── cluster_info.py      # Cluster information
│       ├── queue_info.py        # Queue monitoring
│       ├── node_info.py         # Node information
│       ├── node_allocation.py   # Interactive node allocation
│       ├── array_jobs.py        # Array job management
│       ├── slurm_handler.py     # Unified handler interface
│       └── utils.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_capabilities.py     # Implementation tests
│   ├── test_integration.py      # Integration tests
│   └── test_node_allocation.py  # Node allocation tests
├── docs/                        # Additional documentation
├── example_scripts/             # Example Slurm scripts
├── slurm_installation/          # Slurm installation utilities
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

### Design Philosophy

Following MCP best practices, this server implements:

1. **Workflow-First Approach**: Tools designed for real-world HPC workflows
2. **Intelligent Analysis**: AI-powered insights and optimization recommendations  
3. **Beautiful Formatting**: Structured, readable output with comprehensive metadata
4. **Enterprise Security**: Secure job management and cluster access
5. **Performance Optimization**: Efficient job submission and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`uv sync --dev`)
4. Make your changes following the existing patterns
5. Add tests for new functionality
6. Run tests and ensure they pass (`uv run pytest`)
7. Run formatting and linting (`uv run black . && uv run ruff check .`)
8. Commit your changes (`git commit -m 'Add amazing feature'`)
9. Push to the branch (`git push origin feature/amazing-feature`)
10. Submit a pull request

### Development Guidelines

- Follow the existing code style and patterns
- Add comprehensive tests for new features
- Update documentation for any API changes
- Use type hints for better code clarity
- Follow the workflow-first design philosophy

## License

MIT License - This project is part of the Scientific MCPs collection.

---

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Follow the contributing guidelines
- Ensure all tests pass before submitting PRs

**Part of the IoWarp Scientific MCPs Collection** 🔬