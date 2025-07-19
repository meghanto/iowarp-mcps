
# Jarvis-MCP

*A comprehensive MCP server for exploring, composing, and configuring HPC workflows*

---

## Overview

**Jarvis-MCP** is a comprehensive Python package that implements **all 4 phases** of the Jarvis Model Context Protocol (MCP) server. These phases provide complete end-to-end HPC workflow management from discovery through production deployment.

**Phase 1: Discoverability** enables users to explore and understand the Jarvis ecosystem - available packages, repositories, capabilities, and system resources.

**Phase 2: Composition** provides intelligent workflow design tools for creating, managing, and optimizing HPC pipeline configurations.

**Phase 3: Configuration** offers advanced parameter optimization, environment management, and execution method configuration for production-ready HPC deployments.

**Phase 4: Deployment** provides complete execution management, monitoring, and production lifecycle control for HPC workloads.

With **Jarvis-MCP All 4 Phases**, you can:

### Phase 1 - Discoverability:
* **Discover Packages**: Get comprehensive catalog of all available packages across repositories
* **Explore Package Details**: Retrieve detailed information about specific packages including configuration, capabilities, and usage examples
* **Manage Repositories**: List, add, remove, and prioritize package repositories
* **Analyze Resources**: Get comprehensive cluster resource information for deployment planning
* **Configure System**: Initialize Jarvis configuration, set hostfiles, and build resource graphs

### Phase 2 - Composition:
* **Pipeline Management**: Create, load, update, and delete HPC workflow pipelines
* **Package Composition**: Add, remove, and reorder packages within pipelines
* **YAML Integration**: Import and export pipeline configurations in standard YAML format
* **Workflow Templates**: Browse and utilize pre-built pipeline examples and templates
* **Relationship Analysis**: Analyze package dependencies, conflicts, and optimization opportunities
* **Focus Management**: Streamlined pipeline operations with focus-based workflow

### Phase 3 - Configuration:
* **Environment Management**: Build optimized execution environments with automated dependency resolution
* **Parameter Optimization**: AI-assisted package parameter tuning for performance and resource efficiency
* **Execution Configuration**: Configure distributed execution methods (MPI, SSH, PSSH) with intelligent optimization
* **Interceptor Management**: Set up monitoring and profiling tools with LD_PRELOAD coordination
* **Resource Allocation**: Intelligent resource mapping and scheduling optimization across cluster nodes
* **External Integration**: Seamlessly integrate SCSPKG/Spack packages with dependency management

### Phase 4 - Deployment:
* **Pipeline Execution**: Execute configured pipelines with comprehensive resource monitoring and error handling
* **Advanced Execution**: Support for YAML-based execution, parameter sweeps, and repository template execution
* **Real-time Monitoring**: Monitor pipeline execution with distributed node tracking and performance analysis
* **Results Analysis**: Post-execution analysis with optimization recommendations and performance insights
* **Log Management**: Comprehensive log collection, analysis, and management across distributed executions
* **Fault Tolerance**: Checkpoint and restart capabilities for long-running simulations with state preservation
* **Production Management**: Complete lifecycle management from execution through cleanup and archival
* **API Integration**: Python API access for programmatic control and automation

---

## Prerequisites

- Python 3.10.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)
- Jarvis-CD (optional, for full functionality)

## Implemented Tools

### Phase 1: Discoverability Tools

| Tool | Type | Description |
|---|---|---|
| `get_all_packages` | Discovery | Retrieve comprehensive catalog of all available packages from all repositories |
| `get_package_info` | Discovery | Get detailed information about specific packages including README, configuration, and capabilities |
| `get_all_repos` | Repository Management | List all registered repositories with status, package counts, and metadata |
| `modify_repo` | Repository Management | Add, remove, or promote repositories with safety controls |
| `get_resource_status` | Resource Planning | Provide cluster resource information for deployment planning |
| `jm_create_config` | Configuration | Initialize JarvisManager configuration directories |
| `jm_load_config` | Configuration | Load existing JarvisManager configuration |
| `jm_set_hostfile` | Configuration | Set hostfile path for multi-node deployments |
| `jm_graph_build` | Configuration | Build or rebuild the resource graph |

### Phase 2: Composition Tools

| Tool | Category | Description |
|---|---|---|
| `create_pipeline` | Pipeline CRUD | Create new empty pipeline for HPC workflow composition |
| `load_pipeline` | Pipeline CRUD | Load existing pipeline for editing and modification |
| `list_pipelines` | Pipeline CRUD | List all available pipelines with status and metadata |
| `switch_pipeline_focus` | Pipeline CRUD | Switch the currently focused pipeline for operations |
| `delete_pipeline` | Pipeline CRUD | Delete pipeline permanently from the system |
| `update_pipeline` | Pipeline CRUD | Update pipeline metadata and configuration settings |
| `add_package_to_pipeline` | Package Management | Add packages to pipelines with optional configuration |
| `remove_package_from_pipeline` | Package Management | Remove packages from specified pipeline |
| `reorder_pipeline_packages` | Package Management | Reorder packages within pipeline to change execution sequence |
| `get_pipeline_composition` | Package Management | Get detailed information about pipeline structure and packages |
| `import_pipeline_from_yaml` | YAML Integration | Import pipeline configuration from YAML script |
| `export_pipeline_to_yaml` | YAML Integration | Export pipeline configuration to YAML format |
| `browse_pipeline_indexes` | Templates | Browse available pipeline examples and templates from repositories |
| `analyze_package_relationships` | Advanced | Analyze relationships and compatibility between packages in pipeline |

### Phase 3: Configuration Tools

| Tool | Category | Description |
|---|---|---|
| `build_pipeline_environment` | Environment Management | Build optimized execution environment with automated dependency resolution |
| `copy_environment_to_pipeline` | Environment Management | Copy named environment configuration to pipeline for execution |
| `configure_pipeline_environment` | Environment Management | Configure deployment environment settings for pipeline execution |
| `configure_package_parameters` | Package Configuration | Configure package parameters within pipeline with intelligent guidance |
| `optimize_package_configuration` | Package Configuration | AI-assisted parameter optimization for package configuration |
| `validate_pipeline_configuration` | Package Configuration | Comprehensive validation of complete pipeline configuration |
| `configure_execution_method` | Advanced Configuration | Configure distributed execution method (MPI/SSH/PSSH) with optimization |
| `manage_interceptors` | Advanced Configuration | Configure LD_PRELOAD interceptors and monitoring tools |
| `optimize_resource_allocation` | Advanced Configuration | Intelligent resource mapping and scheduling optimization |
| `integrate_scspkg_packages` | Advanced Configuration | Integrate SCSPKG (Spack-based) packages with Jarvis pipeline |

### Phase 4: Deployment Tools

| Tool | Category | Description |
|---|---|---|
| `run_pipeline` | Basic Execution | Execute pipeline with specified configuration and resource allocation |
| `stop_pipeline` | Basic Execution | Stop running pipeline execution with graceful shutdown or force termination |
| `clean_pipeline` | Basic Execution | Clean pipeline artifacts and temporary files with configurable preservation |
| `get_pipeline_status` | Basic Execution | Check pipeline execution status with comprehensive progress information |
| `run_pipeline_from_yaml` | Advanced Execution | Execute pipeline directly from YAML configuration with parameter overrides |
| `execute_pipeline_test` | Advanced Execution | Execute parameter sweep testing for optimization and validation |
| `run_pipeline_from_index` | Advanced Execution | Execute pre-built pipeline from repository index with customization |
| `monitor_pipeline_execution` | Monitoring & Analysis | Real-time monitoring with distributed node tracking and performance analysis |
| `analyze_execution_results` | Monitoring & Analysis | Post-execution analysis with optimization recommendations and performance insights |
| `manage_execution_logs` | Monitoring & Analysis | Log collection, analysis, and management across distributed executions |
| `handle_checkpoint_restart` | Advanced Features | Checkpoint and restart management for fault tolerance and long-running executions |
| `integrate_python_api` | Advanced Features | Python API access for programmatic pipeline control and automation |

## Setup

### Method 1: Direct UV Run (Recommended for Development)
```bash
# From the Jarvis directory
uv run jarvis-mcp
```
This will create a `.venv/` folder, install all required packages, and run the server directly.

### Method 2: Installation and CLI
```bash
# Install in development mode
uv pip install -e .

# Run the server
jarvis-mcp
```

### Method 3: Python Module Execution
```bash
# Run with stdio transport (default)
python -m jarvis_mcp.server

# Run with SSE transport
MCP_TRANSPORT=sse python -m jarvis_mcp.server
```

--- 

## Running the Server with different types of Clients:

### Running the Server with the WARP Client
To interact with the Jarvis MCP server, use the main `wrp.py` client. You will need to configure it to point to the Jarvis server.

1.  **Configure:** Ensure that `Jarvis` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Jarvis
      
    ```

2.  **Run:** Start the client from the repository root with your desired configuration:
    ```bash
    # Example using the Gemini configuration 
    
    python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```
    For quick setup with Gemini, see our [Quick Start Guide](docs/basic_install.md).
    
    
    For detailed setup with local LLMs and other providers, see the [Complete Installation Guide](../bin/docs/Installation.md).

### Running the Server on Claude Command Line Interface Tool

1. Install the Claude Code using NPM:
```bash
npm install -g @anthropic-ai/claude-code
```

2. Running the server:
```bash
claude add mcp jarvis -- uv --directory ~/scientific-mcps/Jarvis run jarvis-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```json
"jarvis-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/scientific-mcps/Jarvis",
        "run",
        "jarvis-mcp"
    ]
}
```

---

## Operations and Usage Examples

### Phase 1 Operations

##### 1. **Initialize Jarvis Configuration**

The first step is to initialize Jarvis configuration directories. This prepares the system for interaction.

```bash
# Query to initialize Jarvis
Query: Initialize Jarvis configuration with config dir './config', private dir './private', and shared dir './shared'
```

**Example Usage:**
```python
# Initialize configuration
await jm_create_config(
    config_dir="./config",
    private_dir="./private", 
    shared_dir="./shared"
)
```

---

##### 2. **Discover Available Packages**

Explore the complete catalog of available packages across all repositories.

```bash
# Query to get all packages
Query: What packages are available in the Jarvis ecosystem?
```

**Example Usage:**
```python
# Get all packages
catalog = await get_all_packages()

# Filter by package type
applications = await get_all_packages(package_type="application")

# Sort by popularity
popular = await get_all_packages(sort_by="popularity")
```

---

##### 3. **Get Detailed Package Information**

Learn about specific packages including their configuration parameters and capabilities.

```bash
# Query to get package details
Query: What is the Incompact3D package and how do I configure it?
```

**Example Usage:**
```python
# Get basic package info
info = await get_package_info("incompact3d")

# Get configuration parameters
config_info = await get_package_info(
    "incompact3d",
    return_config_params=True,
    return_examples=True
)
```

---

##### 4. **Manage Package Repositories**

List, add, or manage package repositories in the system.

```bash
# Query to list repositories
Query: What repositories are currently configured?
```

**Example Usage:**
```python
# List all repositories
repos = await get_all_repos()

# Add a new repository
result = await modify_repo(
    repo_name="myorg_tools",
    operation="add",
    repo_path="/path/to/myorg_tools"
)

# Promote repository to highest priority
result = await modify_repo(
    repo_name="myorg_tools",
    operation="promote"
)
```

---

##### 5. **Analyze Cluster Resources**

Get comprehensive information about available cluster resources for deployment planning.

```bash
# Query to get resource status
Query: What resources are available on this cluster?
```

**Example Usage:**
```python
# Get complete resource status
resources = await get_resource_status()

# Focus on hardware information
hardware = await get_resource_status(
    include_network=False,
    include_storage=False,
    detail_level="comprehensive"
)
```

---

##### 6. **Build Resource Graph**

Build the resource graph for resource-aware deployment planning.

```bash
# Query to build resource graph
Query: Build the resource graph for the cluster
```

**Example Usage:**
```python
# Build resource graph
await jm_graph_build(net_sleep=1.0)
```

---

### Phase 2 Operations

##### 7. **Create and Manage Pipelines**

Create new HPC workflow pipelines for organizing and executing packages.

```bash
# Query to create a new pipeline
Query: Create a new pipeline called 'hpc_benchmark' for I/O testing
```

**Example Usage:**
```python
# Create a new pipeline
result = await create_pipeline(
    pipeline_name="hpc_benchmark",
    description="I/O benchmarking pipeline with storage system",
    switch_focus=True
)

# List all available pipelines
pipelines = await list_pipelines()

# Switch focus to specific pipeline
await switch_pipeline_focus("hpc_benchmark")
```

---

##### 8. **Build Pipeline Composition**

Add packages to pipelines and create complex HPC workflows.

```bash
# Query to build a workflow
Query: Add orangefs storage and ior benchmark to my pipeline
```

**Example Usage:**
```python
# Add storage service to pipeline
await add_package_to_pipeline(
    package_name="orangefs",
    configuration={"num_servers": 4, "storage_path": "/scratch/orangefs"}
)

# Add I/O benchmark application
await add_package_to_pipeline(
    package_name="ior",
    configuration={"size": "1g", "num_procs": 16, "transfer_size": "1m"}
)

# Get current pipeline composition
composition = await get_pipeline_composition()
```

---

##### 9. **YAML Pipeline Management**

Import and export pipelines using YAML format for reproducibility.

```bash
# Query to export pipeline
Query: Export my current pipeline to YAML format
```

**Example Usage:**
```python
# Export pipeline to YAML
yaml_script = await export_pipeline_to_yaml(
    output_path="./hpc_benchmark.yaml"
)

# Import pipeline from YAML
result = await import_pipeline_from_yaml(
    yaml_path="./existing_workflow.yaml",
    pipeline_name="imported_workflow"
)
```

---

##### 10. **Advanced Pipeline Operations**

Reorder packages and analyze relationships for optimization.

```bash
# Query to optimize pipeline
Query: Analyze my pipeline for package conflicts and optimization opportunities
```

**Example Usage:**
```python
# Reorder packages for optimal execution
await reorder_pipeline_packages(
    new_order=["orangefs", "darshan", "ior", "orangefs_stop"]
)

# Analyze package relationships
analysis = await analyze_package_relationships(
    include_suggested_packages=True
)

# Browse available templates
templates = await browse_pipeline_indexes(
    category_filter="benchmark"
)
```

---

### Phase 3 Operations

##### 11. **Environment Management and Optimization**

Build optimized execution environments and manage configurations for production deployment.

```bash
# Query to build optimized environment
Query: Build an optimized environment for my pipeline with aggressive optimizations
```

**Example Usage:**
```python
# Build optimized environment
environment = await build_pipeline_environment(
    optimization_level="aggressive",
    include_development_tools=True
)

# Copy proven environment to new pipeline
await copy_environment_to_pipeline(
    source_environment="production_env_v2",
    pipeline_name="new_simulation"
)

# Configure custom environment settings
await configure_pipeline_environment(
    environment_variables={"OMP_NUM_THREADS": "16", "CUDA_VISIBLE_DEVICES": "0,1"},
    modules_to_load=["gcc/11.0", "openmpi/4.1", "cuda/11.8"],
    optimization_settings={"CFLAGS": "-O3 -march=native"}
)
```

---

##### 12. **Package Parameter Configuration and Optimization**

Configure and optimize package parameters for maximum performance and efficiency.

```bash
# Query to configure and optimize packages
Query: Configure IOR benchmark parameters and optimize for our cluster hardware
```

**Example Usage:**
```python
# Configure package parameters
config_info = await configure_package_parameters(
    package_name="ior",
    configuration_params={
        "size": "10g",
        "num_procs": 32,
        "transfer_size": "4m",
        "block_size": "1g"
    }
)

# AI-assisted optimization
optimization = await optimize_package_configuration(
    package_name="ior",
    optimization_target="performance",
    resource_constraints={"max_memory": "256GB", "max_nodes": 8}
)

# Comprehensive validation
validation = await validate_pipeline_configuration(
    check_environment=True,
    check_resources=True,
    check_dependencies=True
)
```

---

##### 13. **Execution Method and Resource Configuration**

Configure distributed execution methods and optimize resource allocation across cluster nodes.

```bash
# Query to set up distributed execution
Query: Configure MPI execution with 4 nodes and 16 processes per node, optimize resource allocation
```

**Example Usage:**
```python
# Configure MPI execution
execution_config = await configure_execution_method(
    execution_type="mpi",
    hostfile_path="/etc/hosts.cluster",
    node_count=4,
    processes_per_node=16,
    additional_settings={"mpi_implementation": "openmpi"}
)

# Optimize resource allocation
resource_config = await optimize_resource_allocation(
    optimization_strategy="balanced",
    resource_constraints={"max_memory_per_node": "64GB"},
    node_preferences={"orangefs": ["node01", "node02"]}
)
```

---

##### 14. **Advanced Configuration and Integration**

Set up monitoring tools and integrate external packages for comprehensive HPC workflows.

```bash
# Query to add monitoring and integrate external packages
Query: Add Darshan I/O monitoring and integrate HDF5 from Spack
```

**Example Usage:**
```python
# Configure interceptors for monitoring
interceptors = await manage_interceptors(
    action="add",
    interceptor_name="darshan",
    target_packages=["ior", "incompact3d"],
    configuration={"log_path": "/scratch/darshan_logs"}
)

# Integrate Spack packages
integration = await integrate_scspkg_packages(
    package_name="hdf5",
    spack_spec="hdf5@1.12+mpi+fortran",
    build_options={"compiler": "gcc@11.0", "mpi": "openmpi"}
)
```

---

### Phase 4 Operations

##### 15. **Pipeline Execution and Management**

Execute configured pipelines with comprehensive monitoring and control capabilities.

```bash
# Query to execute pipeline
Query: Run my optimized HPC benchmark pipeline with real-time monitoring
```

**Example Usage:**
```python
# Execute pipeline with monitoring
execution_info = await run_pipeline(
    pipeline_name="hpc_benchmark",
    execution_mode="production",
    background=False
)

# Monitor execution in real-time
monitoring_data = await monitor_pipeline_execution(
    execution_id=execution_info.execution_id,
    monitoring_interval=10,
    include_node_details=True
)

# Get current status
status = await get_pipeline_status(
    execution_id=execution_info.execution_id,
    include_resource_usage=True
)
```

---

##### 16. **Advanced Execution Methods**

Execute pipelines from YAML files, run parameter sweeps, and use repository templates.

```bash
# Query for advanced execution
Query: Execute the I/O benchmark template with custom parameters and run parameter sweep testing
```

**Example Usage:**
```python
# Execute from YAML with overrides
execution_info = await run_pipeline_from_yaml(
    yaml_path="./workflows/io_benchmark.yaml",
    override_params={
        "num_nodes": 8,
        "data_size": "100GB",
        "test_duration": "30min"
    }
)

# Parameter sweep testing
test_info = await execute_pipeline_test(
    pipeline_name="benchmark_pipeline",
    parameter_sweep={
        "block_size": ["1MB", "4MB", "16MB"],
        "num_processes": [16, 32, 64],
        "stripe_count": [4, 8, 16]
    },
    max_parallel_runs=6
)

# Execute repository template
execution_info = await run_pipeline_from_index(
    index_name="hpc_io_benchmark",
    repository="community_benchmarks",
    parameter_overrides={"target_throughput": "10GB/s"}
)
```

---

##### 17. **Analysis and Log Management**

Analyze execution results and manage comprehensive logging across distributed executions.

```bash
# Query for analysis and logs
Query: Analyze my completed execution for bottlenecks and collect all logs from distributed nodes
```

**Example Usage:**
```python
# Comprehensive execution analysis
analysis = await analyze_execution_results(
    execution_id="exec_benchmark_456",
    analysis_type="comprehensive",
    compare_with_baseline=True
)

# Log collection and management
logs_info = await manage_execution_logs(
    action="collect",
    execution_id="exec_benchmark_456",
    log_level="info"
)

# Export logs for analysis
logs_info = await manage_execution_logs(
    action="export",
    execution_id="exec_benchmark_456",
    output_format="json"
)
```

---

##### 18. **Fault Tolerance and API Integration**

Manage checkpoints for long-running executions and use Python API for automation.

```bash
# Query for checkpointing and automation
Query: Set up automatic checkpointing for my simulation and configure Python API access
```

**Example Usage:**
```python
# Configure automatic checkpointing
checkpoint_info = await handle_checkpoint_restart(
    action="configure",
    checkpoint_interval=600  # Every 10 minutes
)

# Create manual checkpoint
checkpoint_info = await handle_checkpoint_restart(
    action="create",
    execution_id="exec_long_simulation_789"
)

# Python API integration for automation
api_info = await integrate_python_api(
    api_action="execute",
    api_commands=[
        "pipeline.run('benchmark_pipeline')",
        "execution.monitor('exec_12345')",
        "logs.collect(execution_id='exec_12345')"
    ]
)

# Stop and clean pipeline
await stop_pipeline(
    execution_id="exec_completed_123",
    cleanup=True
)

await clean_pipeline(
    pipeline_name="benchmark_pipeline",
    clean_level="standard",
    preserve_logs=True
)
```



## Documentation

For detailed documentation about the implementation:

- [COMPLETE_DESIGN_PLAN.md](./COMPLETE_DESIGN_PLAN.md) - Comprehensive design document for all phases
- [PHASE1_README.md](./docs/PHASE1_README.md) - Complete Phase 1 documentation
- [PHASE2_README.md](./docs/PHASE2_README.md) - Complete Phase 2 documentation  
- [PHASE3_README.md](./docs/PHASE3_README.md) - Complete Phase 3 documentation
- [PHASE4_README.md](./docs/PHASE4_README.md) - Complete Phase 4 documentation


## Notes

* Ensure your environment is set up with Python 3.10.12+
* Jarvis-CD is optional but recommended for full functionality
* Use `uv pip install -e .` to enable development mode
* The server supports both stdio and SSE transports
* **Complete 4-phase implementation** provides end-to-end HPC workflow management
* All phases work together: Discovery → Composition → Configuration → Deployment
* **Total of 41 tools** implemented across all four phases:
  * **Phase 1**: 5 tools (Discoverability)
  * **Phase 2**: 14 tools (Composition) 
  * **Phase 3**: 10 tools (Configuration)
  * **Phase 4**: 12 tools (Deployment)
* Production-ready with comprehensive error handling, monitoring, and fault tolerance
* Supports distributed execution across hundreds of nodes with real-time monitoring
