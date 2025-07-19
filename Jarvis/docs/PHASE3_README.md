# Jarvis MCP - Phase 3: Configuration Implementation

## Overview

This document describes the third phase implementation of the Jarvis Model Context Protocol (MCP) server, focusing on **Configuration** tools that enable users to optimize, configure, and manage HPC pipeline execution parameters and environments.

## Design Philosophy

Following MCP best practices from the comprehensive design document, this implementation uses a **workflow-first approach** rather than direct API mapping. The tools are designed to solve complete configuration problems and provide intelligent, contextual assistance for HPC pipeline parameter optimization and environment management.

## Phase 3: Configuration Tools

The configuration phase provides ten core tools organized into three categories that enable users to configure and optimize complex HPC workflows:

### 🏗️ Pipeline Environment Management (3 tools)

#### 1. `build_pipeline_environment`
**Purpose**: Build optimized environment for pipeline with package-specific configurations.

**Key Features**:
- Creates package-specific optimized environments
- Applies optimization levels (fast, balanced, aggressive)
- Automatically configures environment variables and modules
- Includes development tools (debugging, profiling) when requested
- Machine-specific optimization flags
- Dependency conflict detection

**Usage Example**:
```python
# Build balanced environment
env_info = await build_pipeline_environment(
    pipeline_name="hpc_benchmark",
    optimization_level="balanced",
    include_development_tools=True
)

# Build aggressive optimization environment
env_info = await build_pipeline_environment(
    optimization_level="aggressive",
    environment_name="production_env"
)
```

#### 2. `copy_environment_to_pipeline`
**Purpose**: Copy existing named environment configuration to pipeline.

**Key Features**:
- Copies environment variables, modules, and settings
- Validates compatibility before copying
- Provides overwrite protection with confirmation
- Updates pipeline environment associations
- Maintains environment version tracking

**Usage Example**:
```python
# Copy production environment to new pipeline
result = await copy_environment_to_pipeline(
    source_environment="production_baseline",
    pipeline_name="new_simulation",
    overwrite_existing=False
)
```

#### 3. `configure_pipeline_environment`
**Purpose**: Set up deployment environment for pipeline execution.

**Key Features**:
- Manual environment variable configuration
- Module loading and unloading management
- Optimization setting adjustments
- Environment validation and testing
- Configuration rollback support

**Usage Example**:
```python
# Configure environment manually
result = await configure_pipeline_environment(
    environment_variables={
        "OMP_NUM_THREADS": "16",
        "CUDA_VISIBLE_DEVICES": "0,1",
        "MPI_BUFFER_SIZE": "64MB"
    },
    modules_to_load=["gcc/11.0", "openmpi/4.1", "cuda/11.8"],
    optimization_settings={
        "compiler_flags": "-O3 -march=native",
        "link_flags": "-flto"
    }
)
```

### ⚙️ Package Configuration Management (3 tools)

#### 4. `configure_package_parameters`
**Purpose**: Configure package parameters with validation and optimization suggestions.

**Key Features**:
- Interactive and programmatic configuration modes
- Parameter validation with constraint checking
- Type-safe parameter handling
- Performance impact analysis
- Configuration menu generation
- Optimization suggestions based on package type

**Usage Example**:
```python
# Configure IOR benchmark parameters
config_info = await configure_package_parameters(
    package_name="ior",
    configuration_params={
        "size": "10g",
        "num_procs": 32,
        "transfer_size": "4m",
        "block_size": "1g"
    }
)

# Interactive configuration mode
config_info = await configure_package_parameters(
    package_name="orangefs",
    interactive_mode=True
)
```

#### 5. `optimize_package_configuration`
**Purpose**: AI-assisted parameter optimization for package performance.

**Key Features**:
- Performance, memory, network, and balanced optimization targets
- Resource constraint awareness
- Automatic parameter tuning based on best practices
- Workload-specific optimizations
- Performance impact predictions

**Usage Example**:
```python
# Optimize for performance
result = await optimize_package_configuration(
    package_name="ior",
    optimization_target="performance",
    resource_constraints={
        "max_memory": "64GB",
        "available_cores": 32,
        "network_bandwidth": "10Gbps"
    }
)

# Optimize for memory efficiency
result = await optimize_package_configuration(
    package_name="simulation_app",
    optimization_target="memory"
)
```

#### 6. `validate_pipeline_configuration`
**Purpose**: Comprehensive validation of complete pipeline configuration.

**Key Features**:
- Package parameter validation
- Environment compatibility checking
- Resource requirement analysis
- Dependency validation
- Configuration error detection
- Optimization opportunity identification

**Usage Example**:
```python
# Full pipeline validation
validation = await validate_pipeline_configuration(
    pipeline_name="production_workflow",
    check_environment=True,
    check_resources=True,
    check_dependencies=True
)

# Quick validation (environment only)
validation = await validate_pipeline_configuration(
    check_resources=False,
    check_dependencies=False
)
```

### 🎯 Advanced Configuration Management (4 tools)

#### 7. `configure_execution_method`
**Purpose**: Configure MPI/SSH/PSSH execution methods for distributed execution.

**Key Features**:
- Multiple execution types (LOCAL, SSH, PSSH, MPI)
- Hostfile management and validation
- Process distribution optimization
- Execution-specific parameter tuning
- Resource estimation and planning

**Usage Example**:
```python
# Configure MPI execution
exec_config = await configure_execution_method(
    execution_type=ExecutionType.MPI,
    hostfile_path="/etc/cluster_hosts",
    node_count=8,
    processes_per_node=16,
    additional_settings={
        "mpi_implementation": "openmpi",
        "network_interface": "ib0"
    }
)

# Configure SSH execution
exec_config = await configure_execution_method(
    execution_type=ExecutionType.SSH,
    node_count=4,
    additional_settings={
        "ssh_options": "-o StrictHostKeyChecking=no",
        "connection_timeout": 60
    }
)
```

#### 8. `manage_interceptors`
**Purpose**: Configure LD_PRELOAD and interceptor management for monitoring.

**Key Features**:
- Interceptor addition, removal, and reordering
- LD_PRELOAD order management
- Target package specification
- Compatibility validation
- Output file management

**Usage Example**:
```python
# Add Darshan interceptor
interceptors = await manage_interceptors(
    action="add",
    interceptor_name="darshan",
    target_packages=["ior", "simulation_app"],
    configuration={
        "log_path": "/scratch/darshan_logs",
        "compression": "bzip2"
    }
)

# List current interceptors
interceptors = await manage_interceptors(action="list")

# Reorder interceptors for optimal performance
interceptors = await manage_interceptors(
    action="reorder",
    configuration={"new_order": ["darshan", "pymonitor"]}
)
```

#### 9. `optimize_resource_allocation`
**Purpose**: Optimize resource mapping and scheduling for pipeline execution.

**Key Features**:
- Intelligent node assignment strategies
- Load balancing optimization
- Resource conflict detection
- Performance estimation
- Strategy-based allocation (balanced, CPU-intensive, I/O-intensive, memory-intensive)

**Usage Example**:
```python
# Balanced resource allocation
allocation = await optimize_resource_allocation(
    optimization_strategy="balanced",
    resource_constraints={
        "max_nodes": 16,
        "memory_per_node": "128GB",
        "cores_per_node": 32
    }
)

# I/O intensive workload optimization
allocation = await optimize_resource_allocation(
    optimization_strategy="io_intensive",
    node_preferences={
        "storage_services": ["node01", "node02"],
        "compute_tasks": ["node03", "node04", "node05"]
    }
)
```

#### 10. `integrate_scspkg_packages`
**Purpose**: Integrate SCSPKG (Spack-based) packages with Jarvis pipelines.

**Key Features**:
- Spack package specification support
- Dependency tree management
- Build option configuration
- Environment modification handling
- Installation path management

**Usage Example**:
```python
# Integrate HDF5 with Spack
integration = await integrate_scspkg_packages(
    package_name="hdf5",
    spack_spec="hdf5@1.12.1+mpi+szip",
    build_options={
        "compiler": "gcc@11.0.0",
        "mpi": "openmpi@4.1.0",
        "optimization": "-O3"
    }
)

# Integrate MPI library
integration = await integrate_scspkg_packages(
    package_name="openmpi",
    spack_spec="openmpi@4.1.0+cuda+hwloc"
)
```

## Architecture

### Data Models

All Phase 3 tools use comprehensive Pydantic models for type-safe, structured responses:

- **PipelineEnvironmentInfo**: Environment build results and configuration
- **PackageConfigurationInfo**: Package parameter details and validation
- **ExecutionMethodConfig**: Execution method settings and validation
- **InterceptorConfiguration**: Interceptor setup and management
- **ResourceAllocationConfig**: Resource mapping and optimization results
- **SCSSPkgIntegrationInfo**: Spack package integration details
- **PipelineValidationResult**: Comprehensive validation results
- **ConfigurationOperationResult**: Configuration operation outcomes
- **ExecutionType**: Enumeration of execution methods (LOCAL, SSH, PSSH, MPI)

### Error Handling

Comprehensive error handling with specific guidance:

```python
class ConfigurationError(Exception):
    """Custom exception for configuration-related errors with specific guidance"""
    pass

def handle_configuration_errors(func):
    """Decorator to handle configuration errors and provide MCP-compatible responses"""
    # Provides specific guidance based on error type
    # Converts configuration errors to MCP-compatible responses
```

### Focus Management Integration

Seamless integration with Phase 2 focus management:

```python
# All tools support focused pipeline operations
await build_pipeline_environment()  # Uses focused pipeline
await configure_package_parameters("ior")  # Uses focused pipeline
await validate_pipeline_configuration()  # Uses focused pipeline
```

## Installation and Setup

### Prerequisites

1. **Phase 1 & 2** must be working (discoverability and composition tools)
2. **Jarvis-CD** (optional, for full functionality)
3. **Environment modules** for module management
4. **MPI implementation** for distributed execution

### Configuration Workflow

1. **Environment Setup**: Use environment tools to prepare execution environment
2. **Parameter Configuration**: Configure individual package parameters
3. **Execution Method**: Set up distributed execution configuration
4. **Validation**: Validate complete configuration before execution
5. **Optimization**: Apply performance optimizations and resource allocation

## Testing

Run the comprehensive Phase 3 test suite:

```bash
python test_phase3.py
```

The test suite verifies:
- ✅ Phase 3 model imports and functionality
- ✅ Configuration function availability
- ✅ Server structure and tool registration
- ✅ Pydantic model serialization for Phase 3
- ✅ All 10 Phase 3 tools are present
- ✅ Tool categorization (Environment: 3, Package: 3, Advanced: 4)

## User Query Patterns

Phase 3 tools are designed to handle these common user queries:

### Environment Management Queries
- "Build an optimized environment for my pipeline"
- "Copy the production environment to my test pipeline"
- "Configure environment variables for CUDA execution"
- "Set up modules for Intel compiler suite"

### Package Configuration Queries
- "Configure IOR parameters for large-scale I/O testing"
- "Optimize OrangeFS settings for my storage cluster"
- "Validate my pipeline configuration before deployment"
- "What are the optimal parameters for this workload?"

### Execution Configuration Queries
- "Set up MPI execution across 16 nodes"
- "Configure SSH-based execution for heterogeneous cluster"
- "Add Darshan monitoring to my pipeline"
- "Optimize resource allocation for memory-intensive workload"

### Advanced Integration Queries
- "Integrate HDF5 from Spack with MPI support"
- "Configure interceptors for performance profiling"
- "Optimize node assignment for I/O-intensive pipeline"
- "Set up PSSH execution for parameter sweep"

## MCP Best Practices Implemented

### 1. Workflow-First Design
Tools solve complete configuration problems rather than exposing individual configuration commands.

### 2. Parameter Optimization Intelligence
AI-assisted optimization based on workload patterns, resource constraints, and best practices.

### 3. Comprehensive Validation
Multi-level validation including parameters, environment, resources, and dependencies.

### 4. Execution Method Flexibility
Support for multiple execution paradigms from local to large-scale distributed.

### 5. Interceptor Integration
Seamless integration of monitoring and profiling tools through interceptor management.

### 6. Resource Intelligence
Smart resource allocation considering package requirements and cluster capabilities.

## Integration with Previous Phases

Phase 3 builds seamlessly on Phase 1 & 2 capabilities:

1. **Package Discovery (Phase 1)**: Use to find packages before configuration
2. **Pipeline Composition (Phase 2)**: Use to build pipeline structure before configuration
3. **Configuration (Phase 3)**: Use to optimize and configure for execution
4. **Resource Information (Phase 1)**: Use to guide resource allocation decisions

## Future Integration

Phase 3 provides the foundation for:

- **Phase 4: Deployment** - Execution of configured pipelines
- **Advanced Monitoring** - Integration with monitoring and profiling tools
- **Performance Optimization** - Iterative optimization based on execution results

## Contributing

When extending or modifying Phase 3 tools:

1. Follow the workflow-first design philosophy
2. Maintain focus-based operation support from Phase 2
3. Provide comprehensive docstrings with guidance sections
4. Use Pydantic models for structured responses
5. Handle errors gracefully with specific guidance
6. Add appropriate tests to the test suite
7. Consider resource constraints and optimization opportunities
8. Validate configuration changes before applying

## License

This implementation follows the same license as the Jarvis-CD project.

---

**Phase 3 Status**: ✅ Complete and Ready for Testing
**Total Tools**: 10 configuration tools across 3 categories
- **Environment Management**: 3 tools
- **Package Configuration**: 3 tools  
- **Advanced Configuration**: 4 tools
**Next Phase**: Phase 4 (Deployment) - Pipeline execution and monitoring