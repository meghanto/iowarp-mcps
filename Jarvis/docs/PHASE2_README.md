# Jarvis MCP - Phase 2: Composition Implementation

## Overview

This document describes the second phase implementation of the Jarvis Model Context Protocol (MCP) server, focusing on **Composition** tools that enable users to design, build, and manage HPC workflow pipelines.

## Design Philosophy

Following MCP best practices from the comprehensive design document, this implementation uses a **workflow-first approach** rather than direct API mapping. The tools are designed to solve complete user problems and provide intelligent, contextual assistance for HPC pipeline composition and management.

## Phase 2: Composition Tools

The composition phase provides fourteen core tools organized into four categories that enable users to design and manage complex HPC workflows:

### 🏗️ Pipeline CRUD Operations (6 tools)

#### 1. `create_pipeline`
**Purpose**: Create new empty pipeline for HPC workflow composition.

**Key Features**:
- Validates pipeline name uniqueness
- Creates pipeline directory structure and metadata
- Optionally sets as focused pipeline for subsequent operations
- Supports pipeline descriptions and categorization

**Usage Example**:
```python
# Create a new pipeline
result = await create_pipeline(
    pipeline_name="hpc_benchmark",
    description="I/O benchmarking pipeline with storage system",
    switch_focus=True
)
```

#### 2. `load_pipeline`
**Purpose**: Load existing pipeline for editing and modification.

**Key Features**:
- Prepares pipeline for composition operations
- Validates current pipeline state and configuration
- Sets pipeline as focused for subsequent operations
- Provides suggestions based on pipeline status

**Usage Example**:
```python
# Load existing pipeline for editing
result = await load_pipeline("my_simulation_pipeline")
```

#### 3. `list_pipelines`
**Purpose**: List all available pipelines with status and metadata.

**Key Features**:
- Shows creation dates, package counts, and pipeline status
- Indicates currently focused pipeline
- Provides recent pipeline activity information
- Pipeline status indicators (created, configured, running)

**Usage Example**:
```python
# Get all available pipelines
pipelines = await list_pipelines()
```

#### 4. `switch_pipeline_focus`
**Purpose**: Switch the currently focused pipeline for operations.

**Key Features**:
- Streamlined workflow with focus-based operations
- Eliminates need to specify pipeline names repeatedly
- Context awareness for subsequent operations
- Focus persistence across sessions

**Usage Example**:
```python
# Switch focus to specific pipeline
await switch_pipeline_focus("hpc_benchmark")
```

#### 5. `delete_pipeline`
**Purpose**: Delete pipeline permanently from the system.

**Key Features**:
- Validates pipeline exists before deletion
- Provides impact analysis of what will be lost
- Handles focused pipeline management
- Irreversible operation with safety warnings

**Usage Example**:
```python
# Delete pipeline permanently
result = await delete_pipeline("old_test_pipeline")
```

#### 6. `update_pipeline`
**Purpose**: Update pipeline metadata and configuration settings.

**Key Features**:
- Update pipeline name, description, and metadata
- Link or unlink named environments
- Preserve package configurations during updates
- Handle name changes with reference updates

**Usage Example**:
```python
# Update pipeline properties
result = await update_pipeline(
    pipeline_name="old_name",
    new_name="improved_benchmark",
    new_description="Enhanced I/O benchmark with monitoring",
    environment_name="production_env"
)
```

### 📦 Package Management (4 tools)

#### 7. `add_package_to_pipeline`
**Purpose**: Add packages to pipelines with optional configuration.

**Key Features**:
- Supports all package types (services, applications, interceptors)
- Configuration parameter validation during addition
- Execution order management
- Dependency awareness and warnings

**Usage Example**:
```python
# Add storage service
await add_package_to_pipeline(
    package_name="orangefs",
    configuration={"num_servers": 4, "storage_path": "/scratch/orangefs"}
)

# Add I/O benchmark
await add_package_to_pipeline(
    package_name="ior",
    configuration={"size": "1g", "num_procs": 16, "transfer_size": "1m"}
)
```

#### 8. `remove_package_from_pipeline`
**Purpose**: Remove packages from specified pipeline.

**Key Features**:
- Updates execution order of remaining packages
- Validates remaining pipeline structure
- Provides warnings about dependency impacts
- Cleans up package-specific configuration

**Usage Example**:
```python
# Remove package from pipeline
result = await remove_package_from_pipeline(
    package_name="old_monitoring_tool",
    pipeline_name="hpc_benchmark"
)
```

#### 9. `get_pipeline_composition`
**Purpose**: Get detailed information about pipeline structure and packages.

**Key Features**:
- Complete package list with execution order
- Configuration parameters and validation status
- Dependency analysis and resource requirements
- Environment association information

**Usage Example**:
```python
# Get current pipeline composition
composition = await get_pipeline_composition()

# Get specific pipeline composition
composition = await get_pipeline_composition("simulation_pipeline")
```

#### 10. `reorder_pipeline_packages`
**Purpose**: Reorder packages within pipeline to change execution sequence.

**Key Features**:
- Dependency-based reordering validation
- Support for common execution patterns
- Configuration preservation during reordering
- Optimization suggestions for package order

**Usage Example**:
```python
# Reorder packages for optimal execution
await reorder_pipeline_packages(
    new_order=["orangefs", "darshan", "ior", "orangefs_stop"]
)
```

### 📄 YAML Integration (2 tools)

#### 11. `import_pipeline_from_yaml`
**Purpose**: Import pipeline configuration from YAML script.

**Key Features**:
- Standard Jarvis YAML format support
- Environment configuration handling
- Package configuration validation during import
- Error reporting with specific guidance

**Usage Example**:
```python
# Import pipeline from YAML
result = await import_pipeline_from_yaml(
    yaml_path="./workflows/hpc_benchmark.yaml",
    pipeline_name="imported_benchmark"
)
```

#### 12. `export_pipeline_to_yaml`
**Purpose**: Export pipeline configuration to YAML format.

**Key Features**:
- Complete pipeline configuration export
- Environment configuration inclusion
- Reproducible workflow definitions
- Version control friendly format

**Usage Example**:
```python
# Export pipeline to YAML
yaml_script = await export_pipeline_to_yaml(
    pipeline_name="hpc_benchmark",
    output_path="./exported_benchmark.yaml"
)
```

### 🎯 Advanced Features (2 tools)

#### 13. `browse_pipeline_indexes`
**Purpose**: Browse available pipeline examples and templates from repositories.

**Key Features**:
- Access to pre-built pipeline templates
- Category-based browsing (benchmarks, simulations, development)
- Repository source filtering
- Complexity level indicators

**Usage Example**:
```python
# Browse available templates
templates = await browse_pipeline_indexes(
    category_filter="benchmark"
)

# Browse specific repository templates
repo_templates = await browse_pipeline_indexes(
    repository_filter="builtin"
)
```

#### 14. `analyze_package_relationships`
**Purpose**: Analyze relationships and compatibility between packages in pipeline.

**Key Features**:
- Dependency analysis and conflict detection
- Performance synergy identification
- Resource conflict analysis
- Optimization recommendations
- Alternative package suggestions

**Usage Example**:
```python
# Analyze current pipeline
analysis = await analyze_package_relationships(
    include_suggested_packages=True
)

# Analyze specific pipeline
analysis = await analyze_package_relationships(
    pipeline_name="complex_workflow",
    include_suggested_packages=False
)
```

## Architecture

### Data Models

All Phase 2 tools use comprehensive Pydantic models for type-safe, structured responses:

- **PipelineBasicInfo**: Pipeline metadata and status information
- **PipelinePackageEntry**: Individual package details within pipelines
- **PipelineCompositionInfo**: Complete pipeline structure and validation
- **PipelineOperationResult**: Results of pipeline CRUD operations
- **PackageOperationResult**: Results of package management operations
- **PipelineListResult**: Pipeline listing with summary information
- **PipelineYAMLScript**: YAML import/export handling
- **PipelineIndexInfo**: Template and example pipeline information
- **PackageRelationshipAnalysis**: Relationship analysis results

### Error Handling

Comprehensive error handling with specific guidance:

```python
class CompositionError(Exception):
    """Custom exception for composition-related errors"""
    pass

def handle_composition_errors(func):
    """Decorator to handle errors and convert to appropriate MCP responses"""
    # Provides specific guidance based on error type
    # Converts Jarvis pipeline errors to MCP-compatible responses
```

### Focus Management System

Intelligent pipeline focus management for streamlined operations:

```python
# Focus concept eliminates repetitive pipeline name specification
await switch_pipeline_focus("my_pipeline")
await add_package_to_pipeline("ior")  # Uses focused pipeline
await get_pipeline_composition()      # Shows focused pipeline
```

## Installation and Setup

### Prerequisites

1. **Phase 1** must be working (discoverability tools)
2. **Jarvis-CD** (optional, for full functionality)
3. **YAML support** for pipeline import/export

### Pipeline Management Workflow

1. **Discovery**: Use Phase 1 tools to explore available packages
2. **Creation**: Create new pipeline with `create_pipeline`
3. **Composition**: Add packages with `add_package_to_pipeline`
4. **Optimization**: Analyze and reorder with relationship tools
5. **Export**: Save configuration with `export_pipeline_to_yaml`

## Testing

Run the comprehensive Phase 2 test suite:

```bash
python test_phase2.py
```

The test suite verifies:
- ✅ Phase 2 model imports and functionality
- ✅ Composition function availability
- ✅ Server structure and tool registration
- ✅ Pydantic model serialization for Phase 2
- ✅ All 14 Phase 2 tools are present

## User Query Patterns

Phase 2 tools are designed to handle these common user queries:

### Pipeline Management Queries
- "Create a new pipeline for I/O benchmarking"
- "List all my available pipelines"
- "Switch to working on my simulation pipeline"
- "Delete the old test pipeline"

### Composition Queries
- "Add orangefs storage to my pipeline"
- "What packages are in my current pipeline?"
- "Remove the monitoring package"
- "Reorder packages for better performance"

### YAML and Template Queries
- "Export my pipeline to YAML format"
- "Import the benchmark template"
- "What example pipelines are available?"
- "Save my workflow configuration"

### Optimization Queries
- "Analyze my pipeline for conflicts"
- "What packages work well with ior?"
- "Optimize my package execution order"
- "Suggest improvements for my workflow"

## MCP Best Practices Implemented

### 1. Workflow-First Design
Tools solve complete pipeline management problems rather than exposing individual CLI commands.

### 2. Focus-Based Operations
Intelligent focus management eliminates repetitive pipeline name specification.

### 3. Comprehensive Validation
Pipeline and package validation at every step with specific error guidance.

### 4. Template System
Access to pre-built workflows and examples for rapid development.

### 5. Relationship Intelligence
Advanced analysis of package interactions and optimization opportunities.

### 6. YAML Integration
Standard format support for reproducible, version-controllable workflows.

## Integration with Phase 1

Phase 2 builds seamlessly on Phase 1 capabilities:

1. **Package Discovery**: Use Phase 1 tools to find packages
2. **Pipeline Composition**: Use Phase 2 tools to combine packages
3. **Resource Awareness**: Phase 1 resource information guides Phase 2 decisions

## Future Integration

Phase 2 provides the foundation for:

- **Phase 3: Configuration** - Parameter optimization using Phase 2 pipeline structures
- **Phase 4: Deployment** - Execution of Phase 2 composed pipelines

## Contributing

When extending or modifying Phase 2 tools:

1. Follow the workflow-first design philosophy
2. Maintain focus-based operation support
3. Provide comprehensive docstrings with guidance sections
4. Use Pydantic models for structured responses
5. Handle errors gracefully with specific guidance
6. Add appropriate tests to the test suite
7. Consider package relationship impacts

## License

This implementation follows the same license as the Jarvis-CD project.

---

**Phase 2 Status**: ✅ Complete and Ready for Testing
**Total Tools**: 14 composition tools across 4 categories
**Next Phase**: Phase 3 (Configuration) - Parameter optimization and performance tuning