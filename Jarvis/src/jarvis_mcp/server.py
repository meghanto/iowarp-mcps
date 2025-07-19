"""
Jarvis MCP Server

This server implements the first three phases of the Jarvis MCP according to the design document:
- Phase 1: Discoverability tools for exploring the Jarvis ecosystem
- Phase 2: Composition tools for planning and designing deployment workflows
- Phase 3: Configuration tools for parameter optimization and environment management

Following MCP best practices, these tools are designed with a workflow-first approach
rather than direct API mapping, providing intelligent, contextual assistance for
HPC workflow planning, composition, and configuration management.
"""

from fastmcp import FastMCP
import os
import sys
import logging
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Import Phase 1 discoverability tools
from jarvis_mcp.capabilities.discoverability import (
    get_all_packages,
    get_package_info,
    get_list_repos,
    modify_repo,
    get_resource_status,
    DiscoverabilityError
)

# Import Phase 2 composition tools
from jarvis_mcp.capabilities.composition import (
    create_pipeline,
    load_pipeline,
    list_pipelines,
    switch_pipeline_focus,
    delete_pipeline,
    update_pipeline,
    add_package_to_pipeline,
    remove_package_from_pipeline,
    get_pipeline_composition,
    reorder_pipeline_packages,
    import_pipeline_from_yaml,
    export_pipeline_to_yaml,
    browse_pipeline_indexes,
    analyze_package_relationships,
    CompositionError
)

# Import Phase 3 configuration tools
from jarvis_mcp.capabilities.configuration import (
    build_pipeline_environment,
    copy_environment_to_pipeline,
    configure_pipeline_environment,
    configure_package_parameters,
    optimize_package_configuration,
    validate_pipeline_configuration,
    configure_execution_method,
    manage_interceptors,
    optimize_resource_allocation,
    integrate_scspkg_packages,
    ConfigurationError
)

# Import data models
from jarvis_mcp.capabilities.models import (
    PackageCatalog,
    PackageInformation,
    RepositoryStatus,
    RepositoryOperationResult,
    ClusterResourceStatus,
    # Phase 2 models
    PipelineBasicInfo,
    PipelineCompositionInfo,
    PipelineOperationResult,
    PipelineListResult,
    PackageOperationResult,
    PipelineYAMLScript,
    PipelineIndexInfo,
    PackageRelationshipAnalysis,
    # Phase 3 models
    PipelineEnvironmentInfo,
    PackageConfigurationInfo,
    ExecutionMethodConfig,
    InterceptorConfiguration,
    ResourceAllocationConfig,
    SCSSPkgIntegrationInfo,
    PipelineValidationResult,
    ConfigurationOperationResult,
    ExecutionType
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server instance
mcp = FastMCP("Jarvis-MCP-Phases1-2-3-Discoverability-Composition-Configuration")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: DISCOVERABILITY TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    name="get_all_packages",
    description="""Get all available packages from all repositories with their descriptions and capabilities. 

This tool scans through all registered Jarvis repositories and returns a comprehensive catalog 
of available packages including their types, descriptions, configuration parameters, capabilities, 
and installation requirements. 

Use this to explore what packages are available before creating pipelines or to understand the 
full ecosystem of tools at your disposal.

**Discovery Strategy**:
1. Scans all registered repositories in priority order
2. Categorizes packages by type and use case  
3. Provides relevance scoring based on common usage patterns
4. Highlights packages with strong documentation and examples
5. Identifies package relationships and common combinations

**Selection Guidance**:
- **Services**: Long-running systems (storage, databases, web servers)
- **Applications**: Finite-execution programs (benchmarks, simulations)  
- **Interceptors**: Monitoring and profiling tools (tracers, debuggers)

**Common Package Combinations**:
- Storage + Benchmark: "orangefs" + "ior" for filesystem testing
- Simulation + Analysis: "incompact3d" + "paraview" for flow visualization
- Development + Debug: "hermes" + "hermes_api" for I/O optimization

**Prerequisites**: Jarvis configuration must be initialized
**Tools to use after this**: get_package_info() to learn about specific packages

Use this tool when:
- Starting HPC workflow planning ("What can I deploy?")
- Exploring available applications for specific use cases
- Auditing the current package ecosystem
- Looking for alternatives to existing tools"""
)
async def get_all_packages_tool(
    package_type: str = "all",
    repository_filter: Optional[str] = None,
    include_descriptions: bool = True,
    sort_by: str = "priority"
) -> dict:
    """
    Get comprehensive catalog of all available packages in the Jarvis ecosystem.
    
    Args:
        package_type: Filter by type ("all", "service", "application", "interceptor")
        repository_filter: Only show packages from specific repository
        include_descriptions: Include package descriptions and use cases
        sort_by: Sort order ("priority", "name", "type", "popularity")
    
    Returns:
        Comprehensive package catalog with metadata and recommendations
    """
    try:
        result = await get_all_packages(
            package_type=package_type,
            repository_filter=repository_filter,
            include_descriptions=include_descriptions,
            sort_by=sort_by
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_all_packages: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_all_packages: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="get_package_info",
    description="""Get detailed information about a specific package including README, configuration, capabilities, and more.

This comprehensive tool retrieves extensive details about any package in the Jarvis ecosystem 
including its full description, README documentation, configuration parameters with their types 
and default values, package capabilities and features, output specifications, installation 
instructions, and usage examples.

Use flexible boolean flags to control which information sections are returned. This is essential 
for understanding how to properly configure and use packages in your pipelines, troubleshooting 
package issues, or learning about package functionality before integration.

**Information Extraction Strategy**:
The tool analyzes the user's request and automatically emphasizes the most relevant information 
sections. It combines data from multiple sources:
- Package README files (description, purpose, use cases)
- Configuration schemas (parameters, types, defaults, validation)
- Example configurations and pipeline scripts
- Performance benchmarks and optimization notes
- Dependency analysis and compatibility requirements

**Smart Content Filtering**:
- "What is X?" → Focus on description and use cases
- "What outputs does X generate?" → Emphasize output specifications
- "How do I configure X?" → Highlight configuration parameters
- "What are X's dependencies?" → Focus on requirements and compatibility

**Prerequisites**: Package must exist in registered repositories
**Tools to use before this**: get_all_packages() to discover available package names

Use this tool when:
- Learning about a specific package for the first time
- Understanding package capabilities and limitations
- Planning configuration strategies for specific use cases
- Troubleshooting package-related issues"""
)
async def get_package_info_tool(
    package_name: str,
    return_description: bool = True,
    return_outputs: bool = False,
    return_config_params: bool = False,
    return_examples: bool = False,
    return_dependencies: bool = False,
    return_performance_notes: bool = False,
    summary_level: str = "detailed"
) -> dict:
    """
    Get detailed information about a specific package.
    
    Args:
        package_name: Name of the package to get information about
        return_description: Include package description
        return_outputs: Include information about outputs
        return_config_params: Include configuration parameters
        return_examples: Include usage examples
        return_dependencies: Include dependency information
        return_performance_notes: Include performance characteristics
        summary_level: Detail level ("brief", "detailed", "comprehensive")
    
    Returns:
        Detailed package information based on requested components
    """
    try:
        result = await get_package_info(
            package_name=package_name,
            return_description=return_description,
            return_outputs=return_outputs,
            return_config_params=return_config_params,
            return_examples=return_examples,
            return_dependencies=return_dependencies,
            return_performance_notes=return_performance_notes,
            summary_level=summary_level
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_package_info: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_package_info: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="get_all_repos",
    description="""Get all currently registered repositories with their status, package counts, and metadata.

This tool provides detailed information about each repository including the repository name, 
file system path, current status (active/inactive), total number of packages available, 
metadata such as maintainer information, and repository health status.

Use this to understand your repository configuration, troubleshoot repository issues, or get 
an overview of your package ecosystem before managing repositories or debugging package availability.

**Repository Priority System**:
Jarvis searches repositories in priority order (1 = highest priority). When multiple repositories 
contain packages with the same name, higher priority repositories take precedence. This system 
allows custom implementations to override built-in packages while maintaining fallback options.

**Repository Types**:
- **Built-in**: Official Jarvis repository with core packages
- **Custom**: Organization-specific repositories with local packages
- **Development**: Local development repositories for testing
- **Cached**: Local copies of remote repositories for offline use

**Health Status Indicators**:
- ✅ Active: Repository accessible and functioning normally
- ⚠️ Warning: Minor issues (slow response, outdated packages)
- ❌ Error: Major issues (inaccessible, corrupted, permission denied)
- 🔄 Updating: Repository sync or update in progress

**Prerequisites**: Jarvis configuration must be initialized
**Tools to use after this**: modify_repo() to add, remove, or reorder repositories

Use this tool when:
- Understanding current repository configuration
- Debugging package resolution or "package not found" issues
- Planning repository management operations
- Auditing package sources and availability"""
)
async def get_all_repos_tool(
    include_package_counts: bool = True,
    include_health_status: bool = True,
    show_priority_order: bool = True
) -> dict:
    """
    Get comprehensive list of all registered repositories.
    
    Args:
        include_package_counts: Show number and types of packages in each repository
        include_health_status: Include connectivity and accessibility status
        show_priority_order: Display repositories in search priority order
    
    Returns:
        Repository status information with health and package details
    """
    try:
        result = await get_list_repos(
            include_package_counts=include_package_counts,
            include_health_status=include_health_status,
            show_priority_order=show_priority_order
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_all_repos: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_all_repos: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="modify_repo",
    description="""Perform comprehensive repository lifecycle management operations with safety controls.

This tool handles all repository management operations while providing safety
checks, validation, and rollback capabilities. Following MCP best practices,
it combines multiple related operations into a single, intelligent interface
that understands the implications of each change.

**Repository Management Operations**:

**ADD**: Register new repository with comprehensive validation
- Validates repository structure and package compatibility
- Checks for naming conflicts with existing repositories
- Verifies accessibility and permission requirements
- Adds to end of priority list (lowest priority initially)
- Creates backup of configuration before changes

**DELETE**: Safely remove repository with dependency checking  
- Analyzes active pipelines for dependencies on repository packages
- Provides impact analysis before removal
- Offers migration suggestions for affected pipelines
- Removes from search path without deleting repository files
- Creates rollback instructions for recovery

**PROMOTE**: Elevate repository to highest priority with conflict resolution
- Moves repository to top of search priority list
- Analyzes package conflicts that may result from priority change
- Provides warnings about packages that will be shadowed
- Updates configuration atomically to prevent inconsistent state

**Repository Structure Requirements** (for add operation):
```
repository_name/
├── repository_name/        # Package namespace directory
│   ├── package1/          # Individual package directories
│   │   └── pkg.py         # Package implementation
│   └── package2/
│       └── pkg.py
└── pipelines/             # Optional: pipeline examples
    ├── example1.yaml
    └── example2.yaml
```

Prerequisites:
- For ADD: Repository path must exist and be properly structured
- For DELETE/PROMOTE: Repository must be currently registered
- User must have write access to Jarvis configuration directory

**Tools to use before this**: get_all_repos() to understand current repository configuration
**Tools to use after this**: get_all_repos() to verify changes took effect

Use this tool when:
- Setting up custom package repositories for organization
- Managing package resolution priority and conflicts
- Cleaning up outdated or unused repositories
- Troubleshooting package availability and version conflicts"""
)
async def modify_repo_tool(
    repo_name: str,
    operation: str,
    repo_path: str = "",
    verify_structure: bool = True,
    backup_config: bool = True
) -> dict:
    """
    Perform comprehensive repository lifecycle management operations.
    
    Args:
        repo_name: Repository identifier (must be unique)
        operation: Management operation ("add", "delete", "promote")
        repo_path: Required for "add" - absolute path to repository directory
        verify_structure: Validate repository structure before operation
        backup_config: Create configuration backup before changes
    
    Returns:
        Operation result with status, impact analysis, and rollback instructions
    """
    try:
        # Convert empty string to None for repo_path
        actual_repo_path = repo_path if repo_path else None
        
        result = await modify_repo(
            repo_name=repo_name,
            operation=operation,
            repo_path=actual_repo_path,
            verify_structure=verify_structure,
            backup_config=backup_config
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in modify_repo: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in modify_repo: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="get_resource_status",
    description="""Provide comprehensive cluster resource information for deployment planning.

This tool exposes the Jarvis resource graph in an intelligent, decision-oriented format that 
helps users understand deployment constraints and optimization opportunities. Rather than raw 
hardware data, it provides actionable insights for HPC workflow planning.

**Resource Analysis Strategy**:
1. Introspects current cluster state via Jarvis resource graph
2. Analyzes resource utilization patterns and availability
3. Provides deployment recommendations based on resource constraints
4. Identifies bottlenecks and optimization opportunities
5. Maps resources to common package requirements

**Resource Information Includes**:
- **Hardware inventory** with deployment-relevant specifications
- **Network topology** with bandwidth and latency characteristics
- **Storage hierarchy** with performance and capacity details
- **Resource availability** and utilization patterns
- **Deployment recommendations** based on current resource state
- **Constraint analysis** for common package types

**Prerequisites**: 
- Jarvis resource graph must be built ('jarvis rg build')
- Hostfile must be configured for multi-node clusters
- Appropriate permissions for hardware introspection

**Tools to use before this**: build_resource_graph() if resource graph is not current
**Tools to use after this**: create_pipeline_composition() with resource-aware package selection

Use this tool when:
- Starting deployment planning for new workflows
- Understanding cluster capabilities and limitations
- Optimizing package placement for performance
- Troubleshooting resource-related deployment failures
- Planning resource allocation for multiple concurrent pipelines"""
)
async def get_resource_status_tool(
    include_hardware: bool = True,
    include_network: bool = True,
    include_storage: bool = True,
    include_utilization: bool = True,
    detail_level: str = "summary"
) -> dict:
    """
    Get comprehensive cluster resource information.
    
    Args:
        include_hardware: CPU, memory, and compute node information
        include_network: Network topology, bandwidth, and fabric details
        include_storage: Storage devices, filesystems, and capacity information
        include_utilization: Current resource usage and availability
        detail_level: Information depth ("summary", "detailed", "comprehensive")
    
    Returns:
        Cluster resource status with hardware, network, and storage details
    """
    try:
        result = await get_resource_status(
            include_hardware=include_hardware,
            include_network=include_network,
            include_storage=include_storage,
            include_utilization=include_utilization,
            detail_level=detail_level
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_resource_status: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_resource_status: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

# ═══════════════════════════════════════════════════════════════════════════════
# JARVIS MANAGER CONFIGURATION TOOLS (Essential for Phase 1)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    name="jm_create_config",
    description="""Initialize JarvisManager config directories.

This tool sets up the basic Jarvis configuration directories and initializes the manager.
This is typically the first step when setting up Jarvis in a new environment.

Args:
    config_dir: Directory where pipeline metadata is stored
    private_dir: Directory for private files (SSH keys, etc.)
    shared_dir: Directory accessible by all nodes in cluster (optional)

Use this tool when:
- Setting up Jarvis for the first time
- Initializing Jarvis in a new environment
- Resetting Jarvis configuration"""
)
def jm_create_config_tool(config_dir: str, private_dir: str, shared_dir: Optional[str] = None) -> dict:
    """Initialize manager directories and persist configuration."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.create(config_dir, private_dir, shared_dir)
        manager.save()
        return {"status": "success", "message": "Jarvis configuration initialized successfully"}
    except Exception as e:
        logger.error(f"Failed to create Jarvis config: {e}")
        return {"status": "error", "message": f"Failed to initialize configuration: {str(e)}"}

@mcp.tool(
    name="jm_load_config",
    description="""Load existing JarvisManager configuration.

This tool loads the Jarvis configuration from saved state. Use this to restore
a previously configured Jarvis environment.

Use this tool when:
- Loading an existing Jarvis configuration
- Restoring Jarvis state after restart
- Switching between different Jarvis configurations"""
)
def jm_load_config_tool() -> dict:
    """Load manager configuration from saved state."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.load()
        return {"status": "success", "message": "Configuration loaded successfully"}
    except Exception as e:
        logger.error(f"Failed to load Jarvis config: {e}")
        return {"status": "error", "message": f"Failed to load configuration: {str(e)}"}

@mcp.tool(
    name="jm_set_hostfile",
    description="""Set hostfile path for JarvisManager.

This tool configures the hostfile that defines which machines are available
for multi-node deployments. The hostfile is essential for distributed HPC workflows.

Args:
    path: Absolute path to the hostfile

Use this tool when:
- Setting up multi-node deployments
- Configuring cluster resources
- Changing available compute nodes"""
)
def jm_set_hostfile_tool(path: str) -> dict:
    """Set and save the path to the hostfile for deployments."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.set_hostfile(path)
        manager.save()
        return {"status": "success", "message": f"Hostfile set to '{path}'"}
    except Exception as e:
        logger.error(f"Failed to set hostfile: {e}")
        return {"status": "error", "message": f"Failed to set hostfile: {str(e)}"}

@mcp.tool(
    name="jm_graph_build",
    description="""Build or rebuild the resource graph with a net sleep interval.

This tool constructs the Jarvis resource graph by introspecting the cluster hardware,
network, and storage resources. The resource graph is essential for resource-aware
deployment planning and optimization.

Args:
    net_sleep: Sleep interval between network operations (seconds)

Use this tool when:
- Setting up Jarvis for the first time
- Hardware configuration has changed
- Resource graph is outdated or corrupted
- Need updated resource information for deployment planning"""
)
def jm_graph_build_tool(net_sleep: float) -> dict:
    """Construct or rebuild the resource graph with a given sleep delay."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.resource_graph_build(net_sleep)
        return {"status": "success", "message": "Resource graph built successfully"}
    except Exception as e:
        logger.error(f"Failed to build resource graph: {e}")
        return {"status": "error", "message": f"Failed to build resource graph: {str(e)}"}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: COMPOSITION TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    name="create_pipeline",
    description="""Create a new empty pipeline for HPC workflow composition.

This tool creates a new pipeline directory and initializes basic metadata, equivalent to
the 'jarvis ppl create [pipeline_name]' command. A pipeline is a sequence of packages
(applications, services, interceptors) that can be executed together to form a complete
HPC workflow.

**Pipeline Creation Process**:
1. Validates pipeline name uniqueness
2. Creates pipeline directory structure
3. Initializes metadata and configuration
4. Optionally sets as focused pipeline for subsequent operations

**Pipeline Types and Use Cases**:
- **Benchmark Pipelines**: Storage system + benchmark + monitoring
- **Simulation Pipelines**: Simulation + analysis + visualization
- **Development Pipelines**: Application + debugging + profiling tools

**Prerequisites**: Jarvis must be configured (use jm_create_config first)
**Tools to use after this**: add_package_to_pipeline to add packages

Use this tool when:
- Starting a new HPC workflow design
- Creating reproducible experiment configurations
- Setting up benchmark or simulation workflows
- Building deployment templates for reuse"""
)
async def create_pipeline_tool(
    pipeline_name: str,
    description: str = "",
    switch_focus: bool = True
) -> dict:
    """
    Create a new empty pipeline.
    
    Args:
        pipeline_name: Name for the new pipeline (must be unique)
        description: Optional description for the pipeline
        switch_focus: Whether to make this the currently focused pipeline
    
    Returns:
        Pipeline creation result with status and suggestions
    """
    try:
        result = await create_pipeline(
            pipeline_name=pipeline_name,
            description=description,
            switch_focus=switch_focus
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in create_pipeline: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in create_pipeline: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="list_pipelines", 
    description="""List all available pipelines with their status and metadata.

This tool provides a comprehensive overview of all pipelines in the system, equivalent
to the 'jarvis ppl ls' command. It shows pipeline creation dates, package counts,
focused status, and recent activity to help users navigate their workflow collection.

**Information Provided**:
- Pipeline names and descriptions
- Creation and modification timestamps
- Package count and pipeline status
- Currently focused pipeline indicator
- Recent pipeline activity

**Pipeline Status Indicators**:
- **created**: Empty pipeline, no packages added
- **configured**: Contains packages, ready for execution
- **running**: Currently executing (if deployment tools are available)
- **unknown**: Pipeline state cannot be determined

**Focused Pipeline Concept**:
The focused pipeline is the current working pipeline that commands operate on by default.
This eliminates the need to specify pipeline names repeatedly during composition.

**Prerequisites**: Jarvis must be configured
**Tools to use after this**: switch_pipeline_focus to change focus, load_pipeline to edit

Use this tool when:
- Getting an overview of available workflows
- Finding pipelines by name or recent activity
- Understanding current pipeline status
- Deciding which pipeline to work on next"""
)
async def list_pipelines_tool() -> dict:
    """
    List all available pipelines.
    
    Returns:
        Comprehensive list of pipelines with metadata and status
    """
    try:
        result = await list_pipelines()
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in list_pipelines: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in list_pipelines: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="switch_pipeline_focus",
    description="""Switch the currently focused pipeline for subsequent operations.

This tool changes the active pipeline context, equivalent to the 'jarvis cd [pipeline_name]'
command. The focused pipeline becomes the default target for composition operations,
eliminating the need to specify pipeline names repeatedly.

**Focus Concept Benefits**:
- Streamlined workflow: operate on one pipeline without repetitive naming
- Error reduction: prevents accidentally modifying wrong pipelines
- Context awareness: tools understand which pipeline you're working on
- Natural workflow: matches how users typically work on one project at a time

**Operations That Use Focus**:
- add_package_to_pipeline (uses focused if no pipeline specified)
- get_pipeline_composition (shows focused pipeline details)
- update_pipeline (updates focused pipeline configuration)
- export_pipeline_to_yaml (exports focused pipeline)

**Focus Persistence**:
The focused pipeline is saved in Jarvis configuration and persists across sessions.
Only one pipeline can be focused at a time.

**Prerequisites**: Target pipeline must exist
**Tools to use before this**: list_pipelines to see available options
**Tools to use after this**: get_pipeline_composition to see focused pipeline details

Use this tool when:
- Starting work on a specific pipeline
- Switching between different workflow projects
- Preparing for multiple operations on the same pipeline
- Setting up workspace context for pipeline development"""
)
async def switch_pipeline_focus_tool(pipeline_name: str) -> dict:
    """
    Switch the currently focused pipeline.
    
    Args:
        pipeline_name: Name of the pipeline to focus on
        
    Returns:
        Focus switch result with status and suggestions
    """
    try:
        result = await switch_pipeline_focus(pipeline_name)
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in switch_pipeline_focus: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in switch_pipeline_focus: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="add_package_to_pipeline",
    description="""Add a package to a pipeline with optional configuration.

This tool adds packages to pipelines, equivalent to the 'jarvis ppl append [package_name]' 
command. Packages are the building blocks of HPC workflows - they can be applications
(benchmarks, simulations), services (storage systems, databases), or interceptors 
(profilers, tracers).

**Package Types and Examples**:
- **Applications**: ior (I/O benchmark), incompact3d (CFD simulation), gray_scott (reaction-diffusion)
- **Services**: orangefs (parallel filesystem), hermes (I/O acceleration), redis (database)
- **Interceptors**: darshan (I/O tracing), asan (memory debugging), pymonitor (performance monitoring)

**Configuration Options**:
You can provide configuration parameters during package addition. Common parameters include:
- Size and scaling: num_procs, ppn, size, transfer_size
- Paths and locations: input_file, output_file, storage_path
- Performance tuning: threads, buffer_size, compression
- Debugging: do_dbg, dbg_port, trace_level

**Execution Order**:
Packages are executed in the order they are added to the pipeline. Consider dependencies:
1. Start services first (storage systems, databases)
2. Configure interceptors (profilers, tracers)
3. Run applications (benchmarks, simulations)
4. Stop services last (cleanup)

**Prerequisites**: 
- Pipeline must exist (use create_pipeline first)
- Package must be available (use get_all_packages to see options)

**Tools to use before this**: get_package_info to understand package parameters
**Tools to use after this**: get_pipeline_composition to verify package addition

Use this tool when:
- Building HPC workflows step by step
- Adding specific packages to existing pipelines
- Configuring packages during pipeline composition
- Creating complex multi-package workflows"""
)
async def add_package_to_pipeline_tool(
    package_name: str,
    pipeline_name: str = "",
    configuration: dict = None
) -> dict:
    """
    Add a package to the specified pipeline.
    
    Args:
        package_name: Name of the package to add
        pipeline_name: Target pipeline (uses focused if empty)
        configuration: Optional package configuration parameters
        
    Returns:
        Package addition result with updated pipeline composition
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await add_package_to_pipeline(
            package_name=package_name,
            pipeline_name=actual_pipeline_name,
            configuration=configuration
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in add_package_to_pipeline: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in add_package_to_pipeline: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="get_pipeline_composition",
    description="""Get detailed information about pipeline structure and packages.

This tool provides comprehensive information about a pipeline's composition, including
all packages, their configurations, execution order, and dependencies. Use this to
understand pipeline structure, verify package additions, and review workflow design.

**Information Provided**:
- **Package List**: All packages in execution order with types and configurations
- **Dependencies**: Package dependencies and execution requirements
- **Environment**: Associated environment configuration if any
- **Validation Status**: Pipeline readiness and configuration validation
- **Resource Requirements**: Estimated resource needs (if available)

**Package Details Include**:
- Package name and type (service, application, interceptor)
- Execution order position in pipeline
- Current configuration parameters and values
- Package status (added, configured, validated)
- Dependencies on other packages or system resources

**Validation Information**:
The tool reports pipeline validation status:
- **configured**: All packages properly configured
- **needs_update**: Some packages need reconfiguration
- **invalid**: Configuration errors detected
- **unknown**: Validation status not determined

**Prerequisites**: Pipeline must exist
**Tools to use before this**: switch_pipeline_focus to set target pipeline
**Tools to use after this**: reorder_pipeline_packages if order changes needed

Use this tool when:
- Reviewing pipeline structure before execution
- Verifying package additions and configurations
- Understanding package execution order and dependencies
- Troubleshooting pipeline composition issues
- Documenting workflow design and architecture"""
)
async def get_pipeline_composition_tool(pipeline_name: str = "") -> dict:
    """
    Get detailed information about pipeline composition.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        
    Returns:
        Comprehensive pipeline composition details
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await get_pipeline_composition(actual_pipeline_name)
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in get_pipeline_composition: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_pipeline_composition: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="remove_package_from_pipeline",
    description="""Remove a package from the specified pipeline.

This tool removes packages from pipelines when they are no longer needed or when
restructuring workflows. Removing packages updates the execution order of remaining
packages and cleans up any package-specific configuration.

**Removal Process**:
1. Locates the specified package in the pipeline
2. Removes package and its configuration
3. Updates execution order of remaining packages
4. Validates remaining pipeline structure

**Impact of Removal**:
- Execution order automatically adjusts for remaining packages
- Package-specific configuration is removed
- Dependencies on removed package may cause validation warnings
- Pipeline can be immediately executed if remaining packages are valid

**Common Removal Scenarios**:
- Removing unnecessary monitoring tools from production workflows
- Eliminating packages that failed to configure properly
- Simplifying complex workflows by removing optional components
- Restructuring workflows to change package combinations

**Prerequisites**: 
- Pipeline must exist and contain the specified package
- Package name must match exactly (case-sensitive)

**Tools to use before this**: get_pipeline_composition to see current packages
**Tools to use after this**: get_pipeline_composition to verify removal

Use this tool when:
- Simplifying overly complex workflows
- Removing packages that failed configuration
- Restructuring pipelines for different use cases
- Cleaning up experimental package additions
- Optimizing workflows by removing unnecessary components"""
)
async def remove_package_from_pipeline_tool(
    package_name: str,
    pipeline_name: str = ""
) -> dict:
    """
    Remove a package from the specified pipeline.
    
    Args:
        package_name: Name of the package to remove
        pipeline_name: Target pipeline (uses focused if empty)
        
    Returns:
        Package removal result with updated pipeline composition
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await remove_package_from_pipeline(
            package_name=package_name,
            pipeline_name=actual_pipeline_name
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in remove_package_from_pipeline: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in remove_package_from_pipeline: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="import_pipeline_from_yaml",
    description="""Import pipeline configuration from YAML script.

This tool creates a new pipeline from a YAML script file, equivalent to the 
'jarvis ppl load yaml [yaml_path]' command. YAML scripts are the standard way
to define reproducible HPC workflows in Jarvis, containing all package configurations
and execution parameters.

**YAML Script Structure**:
```yaml
name: my_hpc_workflow
env: production_environment  # Optional named environment
pkgs:
  - pkg_type: orangefs
    pkg_name: storage_system
    num_servers: 4
    storage_path: /scratch/orangefs
  - pkg_type: ior
    pkg_name: io_benchmark
    size: 1g
    num_procs: 16
    transfer_size: 1m
```

**Import Process**:
1. Parses YAML file and validates structure
2. Creates new pipeline with specified name
3. Copies named environment if specified
4. Adds all packages with their configurations
5. Sets imported pipeline as focused

**Environment Handling**:
If the YAML specifies an 'env' field, the tool attempts to copy that named
environment to the pipeline. The environment must already exist in Jarvis.

**Error Handling**:
- Invalid YAML syntax is reported with specific error details
- Missing packages are identified during import
- Configuration parameter validation occurs during package addition
- Partial imports are possible if some packages fail

**Prerequisites**: 
- YAML file must exist and be readable
- Named environment must exist if specified in YAML
- All referenced packages must be available in repositories

**Tools to use before this**: get_all_packages to verify package availability
**Tools to use after this**: get_pipeline_composition to review imported structure

Use this tool when:
- Importing workflows from other systems or users
- Loading predefined benchmark or simulation configurations
- Restoring pipeline configurations from backups
- Using template workflows as starting points
- Sharing reproducible HPC workflow definitions"""
)
async def import_pipeline_from_yaml_tool(
    yaml_path: str,
    pipeline_name: str = ""
) -> dict:
    """
    Import pipeline from YAML script.
    
    Args:
        yaml_path: Path to YAML pipeline script
        pipeline_name: Optional custom pipeline name (uses YAML name if empty)
        
    Returns:
        Pipeline import result with status and imported pipeline info
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await import_pipeline_from_yaml(
            yaml_path=yaml_path,
            pipeline_name=actual_pipeline_name
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in import_pipeline_from_yaml: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in import_pipeline_from_yaml: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="export_pipeline_to_yaml",
    description="""Export pipeline configuration to YAML format.

This tool exports a pipeline's configuration to YAML format, creating a portable
and version-controllable representation of the HPC workflow. The generated YAML
can be shared, archived, or used to recreate the pipeline in other environments.

**Export Contents**:
- Pipeline name and metadata
- Environment configuration (if any)
- Complete package list with all configuration parameters
- Execution order preservation
- All package-specific settings and customizations

**YAML Output Structure**:
The exported YAML follows Jarvis standard format:
```yaml
name: exported_pipeline
env: environment_name  # If environment is configured
pkgs:
  - pkg_type: package_type
    pkg_name: package_identifier
    parameter1: value1
    parameter2: value2
```

**Use Cases for Export**:
- **Version Control**: Track pipeline evolution in git repositories
- **Sharing**: Distribute workflows to collaborators or publications
- **Backup**: Archive working configurations for future restoration
- **Templates**: Create reusable workflow templates for similar projects
- **Documentation**: Generate human-readable workflow specifications

**File Handling**:
If output_path is specified, the YAML is saved to that file location.
If not specified, the YAML content is returned for display or further processing.

**Prerequisites**: Pipeline must exist and be properly configured
**Tools to use before this**: get_pipeline_composition to verify pipeline state
**Tools to use after this**: import_pipeline_from_yaml to test exported YAML

Use this tool when:
- Creating reproducible workflow definitions
- Sharing HPC workflows with collaborators
- Archiving successful pipeline configurations
- Creating templates for similar workflows
- Documenting workflow specifications for publications
- Backing up complex pipeline configurations"""
)
async def export_pipeline_to_yaml_tool(
    pipeline_name: str = "",
    output_path: str = ""
) -> dict:
    """
    Export pipeline configuration to YAML format.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        output_path: Optional path to save YAML file
        
    Returns:
        YAML script content and export status
    """
    try:
        # Convert empty strings to None
        actual_pipeline_name = pipeline_name if pipeline_name else None
        actual_output_path = output_path if output_path else None
        
        result = await export_pipeline_to_yaml(
            pipeline_name=actual_pipeline_name,
            output_path=actual_output_path
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in export_pipeline_to_yaml: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in export_pipeline_to_yaml: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="load_pipeline",
    description="""Load an existing pipeline for editing and modification.

This tool loads an existing pipeline into the workspace for editing, making it the
focused pipeline and preparing it for modifications. Unlike switch_pipeline_focus,
this tool specifically prepares the pipeline for composition operations and validates
its current state.

**Load vs Switch Focus**:
- **load_pipeline**: Prepares pipeline for editing, validates state, provides composition context
- **switch_pipeline_focus**: Simple focus change for quick operations

**Loading Process**:
1. Validates pipeline exists and is accessible
2. Loads pipeline metadata and package configuration
3. Sets pipeline as focused for subsequent operations
4. Validates current pipeline state and configuration
5. Provides suggestions for next steps based on pipeline status

**Post-Load Information**:
- Current package count and composition
- Configuration validation status
- Suggested next actions based on pipeline state
- Environment configuration status
- Recent modification history

**Prerequisites**: Pipeline must exist and be accessible
**Tools to use before this**: list_pipelines to see available options
**Tools to use after this**: get_pipeline_composition to review loaded pipeline

Use this tool when:
- Starting a new editing session on an existing pipeline
- Resuming work on a previously created workflow
- Preparing to make significant changes to pipeline composition
- Validating pipeline state before modifications
- Setting up workspace context for pipeline development"""
)
async def load_pipeline_tool(pipeline_name: str) -> dict:
    """
    Load an existing pipeline for editing.
    
    Args:
        pipeline_name: Name of the pipeline to load
        
    Returns:
        Pipeline load result with status and composition summary
    """
    try:
        result = await load_pipeline(pipeline_name)
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in load_pipeline: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in load_pipeline: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="delete_pipeline",
    description="""Delete a pipeline permanently from the system.

This tool permanently removes a pipeline and all its configuration, equivalent to
the 'jarvis ppl rm [pipeline_name]' command. This operation cannot be undone,
so use with caution.

**Deletion Process**:
1. Validates pipeline exists before deletion
2. Checks if pipeline is currently focused (offers to switch focus)
3. Removes pipeline directory and all configuration files
4. Updates pipeline registry and metadata
5. Provides confirmation of successful deletion

**Safety Considerations**:
- Operation is irreversible - pipeline cannot be recovered
- All package configurations and customizations are lost
- If pipeline is currently focused, focus is cleared
- Running pipelines should be stopped before deletion

**Impact Analysis**:
The tool provides information about what will be lost:
- Number of configured packages
- Custom configuration settings
- Environment associations
- Creation date and modification history

**Prerequisites**: Pipeline must exist and not be currently executing
**Tools to use before this**: get_pipeline_composition to review what will be deleted
**Tools to use after this**: list_pipelines to verify deletion

Use this tool when:
- Cleaning up unused or experimental pipelines
- Removing failed pipeline configurations
- Managing storage space by eliminating old workflows
- Preparing clean workspace for new projects
- Removing pipelines that are no longer relevant"""
)
async def delete_pipeline_tool(pipeline_name: str) -> dict:
    """
    Delete a pipeline permanently.
    
    Args:
        pipeline_name: Name of the pipeline to delete
        
    Returns:
        Pipeline deletion result with status and impact summary
    """
    try:
        result = await delete_pipeline(pipeline_name)
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in delete_pipeline: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in delete_pipeline: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="update_pipeline",
    description="""Update pipeline metadata and configuration settings.

This tool updates pipeline-level configuration including name, description, and
global settings, equivalent to the 'jarvis ppl update' command. This is for
pipeline-level changes, not individual package modifications.

**Updatable Properties**:
- **Pipeline name**: Change pipeline identifier (updates all references)
- **Description**: Update pipeline documentation and purpose
- **Environment association**: Link or unlink named environments
- **Execution settings**: Default execution method and parameters
- **Metadata**: Tags, categories, and organizational information

**Update Process**:
1. Validates current pipeline state
2. Applies requested changes with validation
3. Updates pipeline registry and metadata
4. Preserves package configurations and order
5. Maintains pipeline history and tracking

**Name Change Handling**:
When changing pipeline names:
- All internal references are updated automatically
- Focus is maintained on renamed pipeline
- File system directories are renamed appropriately
- Pipeline history is preserved under new name

**Environment Updates**:
- Link to existing named environments
- Unlink from current environment (packages retain individual configs)
- Environment changes affect new package additions
- Existing packages maintain their current configuration

**Prerequisites**: Pipeline must exist and be accessible
**Tools to use before this**: get_pipeline_composition to see current settings
**Tools to use after this**: get_pipeline_composition to verify updates

Use this tool when:
- Renaming pipelines for better organization
- Adding descriptions to undocumented workflows
- Changing environment associations
- Updating pipeline metadata for documentation
- Reorganizing pipeline properties without affecting package composition"""
)
async def update_pipeline_tool(
    pipeline_name: str = "",
    new_name: str = "",
    new_description: str = "",
    environment_name: str = ""
) -> dict:
    """
    Update pipeline metadata and configuration.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        new_name: New pipeline name (optional)
        new_description: New pipeline description (optional)
        environment_name: Environment to associate (optional)
        
    Returns:
        Pipeline update result with changed properties
    """
    try:
        # Convert empty strings to None
        actual_pipeline_name = pipeline_name if pipeline_name else None
        actual_new_name = new_name if new_name else None
        actual_new_description = new_description if new_description else None
        actual_environment_name = environment_name if environment_name else None
        
        result = await update_pipeline(
            pipeline_name=actual_pipeline_name,
            new_name=actual_new_name,
            new_description=actual_new_description,
            environment_name=actual_environment_name
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in update_pipeline: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in update_pipeline: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="reorder_pipeline_packages",
    description="""Reorder packages within a pipeline to change execution sequence.

This tool changes the execution order of packages in a pipeline. Since HPC workflows
often have dependencies and timing requirements, proper package ordering is crucial
for successful execution.

**Reordering Strategies**:
- **Move by position**: Move package to specific position in execution order
- **Swap packages**: Exchange positions of two packages
- **Dependency-based**: Automatically order based on package dependencies
- **Custom sequence**: Specify complete new execution order

**Common Ordering Patterns**:
1. **Services first**: Storage systems, databases before applications
2. **Interceptors early**: Profilers and tracers before target applications
3. **Applications middle**: Main computation workloads
4. **Cleanup last**: Shutdown services and data collection

**Example Execution Order**:
```
1. orangefs (storage service)
2. darshan (I/O tracing interceptor)
3. ior (I/O benchmark application)
4. orangefs_stop (storage cleanup)
```

**Validation and Safety**:
- Checks for obvious dependency violations
- Warns about potential ordering issues
- Validates that all packages remain in pipeline
- Preserves package configurations during reordering

**Prerequisites**: Pipeline must exist and contain multiple packages
**Tools to use before this**: get_pipeline_composition to see current order
**Tools to use after this**: get_pipeline_composition to verify new order

Use this tool when:
- Optimizing workflow execution performance
- Fixing dependency-related execution failures
- Reorganizing complex multi-package workflows
- Following HPC best practices for package sequencing
- Troubleshooting execution order issues"""
)
async def reorder_pipeline_packages_tool(
    new_order: list,
    pipeline_name: str = ""
) -> dict:
    """
    Reorder packages within a pipeline.
    
    Args:
        new_order: List of package names in desired execution order
        pipeline_name: Target pipeline (uses focused if empty)
        
    Returns:
        Package reordering result with updated execution sequence
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await reorder_pipeline_packages(
            new_order=new_order,
            pipeline_name=actual_pipeline_name
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in reorder_pipeline_packages: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in reorder_pipeline_packages: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="browse_pipeline_indexes",
    description="""Browse available pipeline examples and templates from repositories.

This tool provides access to example pipelines and workflow templates available in
registered repositories, equivalent to the 'jarvis ppl index ls' command. These
pre-built pipelines serve as starting points for common HPC workflows.

**Pipeline Index Categories**:
- **Benchmarks**: Standard performance testing workflows (I/O, compute, network)
- **Simulations**: Scientific computing pipelines (CFD, molecular dynamics, etc.)
- **Development**: Debugging and profiling workflow templates
- **Storage**: Storage system testing and optimization workflows
- **Machine Learning**: ML training and inference pipelines

**Index Information Provided**:
- **Pipeline names** and descriptions from each repository
- **Categories** and use case classifications
- **Complexity levels** (beginner, intermediate, advanced)
- **Resource requirements** and recommended configurations
- **Dependencies** and prerequisite packages

**Repository Sources**:
Pipeline indexes are collected from all registered repositories:
- **Built-in**: Official Jarvis example pipelines
- **Community**: User-contributed workflow templates
- **Organization**: Custom organizational pipeline templates

**Template Usage**:
After browsing, use specific pipeline names with:
- `import_pipeline_from_yaml` to load template pipelines
- `run_pipeline_from_index` to execute templates directly
- Manual recreation using `create_pipeline` and `add_package_to_pipeline`

**Prerequisites**: At least one repository must be registered with pipeline indexes
**Tools to use after this**: import_pipeline_from_yaml to load specific templates
**Tools to use before this**: get_all_repos to understand available repositories

Use this tool when:
- Looking for workflow templates to start new projects
- Learning HPC workflow design patterns
- Finding examples for specific use cases
- Discovering available benchmark and simulation workflows
- Understanding common package combinations and configurations"""
)
async def browse_pipeline_indexes_tool(
    repository_filter: str = "",
    category_filter: str = ""
) -> dict:
    """
    Browse available pipeline examples and templates.
    
    Args:
        repository_filter: Only show pipelines from specific repository
        category_filter: Filter by category (benchmark, simulation, development, etc.)
        
    Returns:
        Available pipeline templates and examples with descriptions
    """
    try:
        # Convert empty strings to None
        actual_repo_filter = repository_filter if repository_filter else None
        actual_category_filter = category_filter if category_filter else None
        
        result = await browse_pipeline_indexes(
            repository_filter=actual_repo_filter,
            category_filter=actual_category_filter
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in browse_pipeline_indexes: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in browse_pipeline_indexes: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="analyze_package_relationships",
    description="""Analyze relationships and compatibility between packages in a pipeline.

This advanced tool examines package interactions, dependencies, and compatibility
to provide optimization suggestions and identify potential conflicts. It helps
users understand how packages work together and optimize workflow performance.

**Analysis Types**:
- **Dependency Analysis**: Required packages and execution order constraints
- **Compatibility Matrix**: Which packages work well together
- **Performance Synergies**: Package combinations that enhance performance
- **Resource Conflicts**: Packages that compete for the same resources
- **Configuration Interactions**: Parameter dependencies between packages

**Relationship Categories**:
- **Complementary**: Packages that enhance each other's functionality
- **Conflicting**: Packages that interfere with each other
- **Dependent**: Packages that require specific other packages
- **Independent**: Packages with no significant interactions
- **Synergistic**: Packages that provide performance benefits when combined

**Optimization Suggestions**:
The tool provides actionable recommendations:
- **Package additions**: Suggested packages to enhance functionality
- **Configuration adjustments**: Parameter changes for better compatibility
- **Execution order**: Optimal sequencing for performance
- **Resource allocation**: Better resource distribution strategies
- **Alternative packages**: Substitutions to resolve conflicts

**Analysis Scope**:
Can analyze relationships for:
- Current pipeline packages (default)
- Specific package combinations
- Potential package additions
- Cross-repository package interactions

**Prerequisites**: Pipeline must contain at least one package
**Tools to use before this**: get_pipeline_composition to see current packages
**Tools to use after this**: add_package_to_pipeline or reorder_pipeline_packages based on suggestions

Use this tool when:
- Optimizing complex multi-package workflows
- Troubleshooting performance or compatibility issues
- Planning package additions to existing pipelines
- Understanding workflow design patterns and best practices
- Validating pipeline design before execution"""
)
async def analyze_package_relationships_tool(
    pipeline_name: str = "",
    include_suggested_packages: bool = False
) -> dict:
    """
    Analyze package relationships and compatibility.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        include_suggested_packages: Include suggestions for additional packages
        
    Returns:
        Comprehensive analysis of package relationships and optimization suggestions
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await analyze_package_relationships(
            pipeline_name=actual_pipeline_name,
            include_suggested_packages=include_suggested_packages
        )
        return result.model_dump()
    except CompositionError as e:
        logger.error(f"Composition error in analyze_package_relationships: {e}")
        return {"error": str(e), "type": "composition_error"}
    except Exception as e:
        logger.error(f"Unexpected error in analyze_package_relationships: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: CONFIGURATION TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    name="build_pipeline_environment",
    description="""Build optimized environment for pipeline execution with package-specific configurations.

This tool creates a tailored execution environment for HPC pipelines, equivalent to the 
'jarvis ppl env build' command. It analyzes pipeline packages and builds an optimized 
environment with proper dependencies, modules, compiler flags, and runtime configurations.

**Environment Building Process**:
1. Analyzes all packages in the pipeline for dependencies
2. Determines optimal compiler and runtime configurations
3. Resolves module dependencies and loading order
4. Sets performance-optimized environment variables
5. Configures package-specific optimization flags
6. Validates environment compatibility across packages

**Optimization Levels**:
- **fast**: Basic optimizations (-O2, -march=native) for quick builds
- **balanced**: Moderate optimizations with good performance/compile time balance
- **aggressive**: Maximum optimizations (-O3, -flto) for production performance

**Environment Components**:
- **Compiler settings**: Optimization flags, target architecture, link-time optimization
- **Runtime environment**: MPI settings, OpenMP configuration, memory management
- **Module loading**: Automatic dependency resolution and load order
- **Package integration**: Cross-package compatibility and shared libraries

**Development Tools Integration**:
When enabled, includes debugging and profiling tools:
- GDB for debugging with optimized symbol tables
- Valgrind for memory error detection
- Performance profilers (perf, gprof)
- Static analysis tools

**Prerequisites**: Pipeline must exist and contain packages
**Tools to use before this**: get_pipeline_composition to review pipeline packages
**Tools to use after this**: validate_pipeline_configuration to verify environment

Use this tool when:
- Preparing pipeline for production execution
- Optimizing performance for specific hardware
- Resolving environment dependency conflicts
- Setting up development and debugging environments
- Creating reproducible execution environments"""
)
async def build_pipeline_environment_tool(
    pipeline_name: str = "",
    environment_name: str = "",
    optimization_level: str = "balanced",
    include_development_tools: bool = False
) -> dict:
    """
    Build optimized environment for pipeline execution.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        environment_name: Name for environment (auto-generated if empty)
        optimization_level: Optimization strategy (fast, balanced, aggressive)
        include_development_tools: Include debugging and profiling tools
        
    Returns:
        PipelineEnvironmentInfo with build results and configuration
    """
    try:
        # Convert empty strings to None
        actual_pipeline_name = pipeline_name if pipeline_name else None
        actual_environment_name = environment_name if environment_name else None
        
        result = await build_pipeline_environment(
            pipeline_name=actual_pipeline_name,
            environment_name=actual_environment_name,
            optimization_level=optimization_level,
            include_development_tools=include_development_tools
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in build_pipeline_environment: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in build_pipeline_environment: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="copy_environment_to_pipeline",
    description="""Copy named environment configuration to pipeline for execution.

This tool copies an existing named environment to a pipeline, equivalent to the 
'jarvis ppl env copy' command. Named environments are pre-configured execution 
contexts that can be reused across multiple pipelines for consistency and efficiency.

**Environment Copy Process**:
1. Validates source environment exists and is accessible
2. Analyzes compatibility with target pipeline packages
3. Copies environment variables, modules, and configurations
4. Adapts environment settings for pipeline-specific requirements
5. Validates copied environment for completeness
6. Updates pipeline metadata with environment association

**Named Environment Types**:
- **Production**: Optimized for performance with minimal debugging
- **Development**: Includes debugging tools and verbose logging
- **Testing**: Configured for automated testing and validation
- **Benchmark**: Optimized specifically for performance benchmarking

**Compatibility Checking**:
The tool performs intelligent compatibility analysis:
- Verifies required modules are available in source environment
- Checks for conflicting package requirements
- Validates compiler and runtime compatibility
- Identifies potential performance implications

**Overwrite Behavior**:
- **overwrite_existing=False**: Fails if pipeline already has environment
- **overwrite_existing=True**: Replaces existing environment with warning
- Provides rollback information for environment restoration

**Prerequisites**: Source environment must exist, pipeline must be accessible
**Tools to use before this**: build_pipeline_environment to create source environments
**Tools to use after this**: validate_pipeline_configuration to verify compatibility

Use this tool when:
- Standardizing environments across multiple pipelines
- Reusing proven environment configurations
- Setting up consistent testing environments
- Applying organizational environment policies
- Migrating pipeline environments between systems"""
)
async def copy_environment_to_pipeline_tool(
    source_environment: str,
    pipeline_name: str = "",
    overwrite_existing: bool = False
) -> dict:
    """
    Copy named environment to pipeline.
    
    Args:
        source_environment: Name of source environment to copy
        pipeline_name: Target pipeline (uses focused if empty)
        overwrite_existing: Whether to overwrite existing environment
        
    Returns:
        ConfigurationOperationResult with copy status and details
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await copy_environment_to_pipeline(
            source_environment=source_environment,
            pipeline_name=actual_pipeline_name,
            overwrite_existing=overwrite_existing
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in copy_environment_to_pipeline: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in copy_environment_to_pipeline: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="configure_pipeline_environment",
    description="""Configure deployment environment settings for pipeline execution.

This tool provides fine-grained control over pipeline environment configuration,
allowing manual specification of environment variables, modules, and optimization
settings. It complements automated environment building with custom requirements.

**Configuration Capabilities**:
- **Environment Variables**: Set custom variables for execution control
- **Module Management**: Specify modules to load and their versions
- **Optimization Settings**: Configure compiler flags and runtime optimizations
- **Runtime Parameters**: Set execution-specific configurations

**Common Environment Variables**:
- **OMP_NUM_THREADS**: OpenMP thread count for parallel regions
- **MPI_COMM_WORLD_SIZE**: MPI process count (auto-set by execution method)
- **CUDA_VISIBLE_DEVICES**: GPU device selection for CUDA applications
- **LD_LIBRARY_PATH**: Additional library search paths
- **PKG_CONFIG_PATH**: Package configuration search paths

**Module Loading**:
The tool manages module dependencies and load order:
- Automatic dependency resolution between specified modules
- Version conflict detection and resolution
- Load order optimization for performance
- Module availability validation across target systems

**Optimization Settings**:
Configurable optimization parameters:
- **Compiler flags**: -O levels, architecture-specific optimizations
- **Linker options**: Link-time optimization, static vs dynamic linking
- **Runtime tuning**: Memory allocators, threading libraries
- **Debugging options**: Symbol generation, profiling instrumentation

**Validation and Testing**:
- Environment variable validation against package requirements
- Module compatibility checking
- Performance impact analysis of optimization settings
- Dry-run capability for testing configurations

**Prerequisites**: Pipeline must exist and be accessible
**Tools to use before this**: get_pipeline_composition to understand package requirements
**Tools to use after this**: validate_pipeline_configuration to verify settings

Use this tool when:
- Setting custom environment variables for specific packages
- Loading non-standard or custom modules
- Applying organization-specific optimization settings
- Configuring environments for special hardware (GPUs, accelerators)
- Fine-tuning performance for specific workloads"""
)
async def configure_pipeline_environment_tool(
    pipeline_name: str = "",
    environment_variables: dict = None,
    modules_to_load: list = None,
    optimization_settings: dict = None
) -> dict:
    """
    Configure deployment environment settings for pipeline.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        environment_variables: Environment variables to set
        modules_to_load: Modules to load in environment
        optimization_settings: Optimization flags and settings
        
    Returns:
        ConfigurationOperationResult with configuration status
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await configure_pipeline_environment(
            pipeline_name=actual_pipeline_name,
            environment_variables=environment_variables,
            modules_to_load=modules_to_load,
            optimization_settings=optimization_settings
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in configure_pipeline_environment: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in configure_pipeline_environment: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="configure_package_parameters",
    description="""Configure package parameters within pipeline with intelligent guidance.

This tool provides comprehensive package configuration, equivalent to the 'jarvis ppl configure'
command. It offers both interactive and programmatic configuration modes with intelligent 
parameter validation, optimization suggestions, and performance impact analysis.

**Configuration Modes**:
- **Programmatic**: Direct parameter setting via configuration_params
- **Interactive**: Menu-driven configuration with guided parameter selection
- **Hybrid**: Programmatic base with interactive refinement

**Parameter Categories**:
- **Performance**: Thread counts, buffer sizes, optimization levels
- **I/O**: File paths, transfer sizes, caching strategies  
- **Resource**: Memory limits, CPU affinity, GPU device selection
- **Debugging**: Logging levels, output verbosity, trace generation

**Intelligent Parameter Validation**:
The tool provides comprehensive validation:
- Type checking and range validation for numerical parameters
- Path validation for file and directory parameters
- Cross-parameter dependency validation
- Performance impact analysis for parameter choices

**Package-Specific Optimizations**:
- **IOR**: Transfer size optimization, process distribution, file system tuning
- **OrangeFS**: Server count optimization, storage allocation, network configuration
- **Incompact3D**: Grid sizing, solver parameters, output frequency
- **Generic packages**: Common HPC parameter patterns and best practices

**Interactive Configuration Menu**:
When interactive_mode=True, provides:
- Parameter descriptions and recommendations
- Current value display with change tracking
- Validation feedback for invalid entries
- Performance impact warnings for significant changes
- Undo/redo capability for configuration changes

**Performance Impact Analysis**:
For each parameter, provides guidance on:
- Memory usage implications
- CPU utilization impact
- I/O performance effects
- Network bandwidth requirements
- Scaling behavior across node counts

**Prerequisites**: Package must exist in pipeline
**Tools to use before this**: get_pipeline_composition to see current package list
**Tools to use after this**: validate_pipeline_configuration to verify complete setup

Use this tool when:
- Optimizing package performance for specific workloads
- Setting up packages for first-time use
- Adapting configurations for different hardware
- Troubleshooting performance issues through parameter tuning
- Learning about package capabilities and options"""
)
async def configure_package_parameters_tool(
    package_name: str,
    pipeline_name: str = "",
    configuration_params: dict = None,
    interactive_mode: bool = False
) -> dict:
    """
    Configure package parameters in pipeline.
    
    Args:
        package_name: Name of package to configure
        pipeline_name: Target pipeline (uses focused if empty)
        configuration_params: Parameters to set (None for interactive)
        interactive_mode: Whether to use interactive configuration menu
        
    Returns:
        PackageConfigurationInfo with configuration details and suggestions
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await configure_package_parameters(
            package_name=package_name,
            pipeline_name=actual_pipeline_name,
            configuration_params=configuration_params,
            interactive_mode=interactive_mode
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in configure_package_parameters: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in configure_package_parameters: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="optimize_package_configuration",
    description="""AI-assisted parameter optimization for package configuration with intelligent analysis.

This advanced tool automatically optimizes package parameters based on available resources,
performance targets, and HPC best practices. It provides intelligent parameter tuning
that goes beyond manual configuration to achieve optimal performance.

**Optimization Targets**:
- **performance**: Maximum throughput and minimal execution time
- **memory**: Minimal memory footprint for constrained environments  
- **network**: Optimized for network bandwidth and latency
- **balanced**: Balanced optimization across all resource dimensions

**AI-Driven Analysis**:
The optimization engine analyzes:
- Package characteristics and scaling behavior
- Available cluster resources and topology
- Historical performance data and patterns
- Cross-package interactions and dependencies
- Resource contention and bottleneck identification

**Resource-Aware Optimization**:
Considers comprehensive resource constraints:
- **CPU**: Core count, architecture, cache hierarchy
- **Memory**: Total RAM, NUMA topology, bandwidth characteristics
- **Storage**: I/O subsystem performance, capacity, file system type
- **Network**: Bandwidth, latency, topology, protocol optimization

**Optimization Strategies**:
- **Scaling analysis**: Optimal process/thread distribution
- **Buffer tuning**: I/O and communication buffer optimization
- **Memory management**: Cache optimization and memory affinity
- **Communication optimization**: MPI and network parameter tuning

**Performance Modeling**:
Uses analytical models to predict:
- Execution time with different parameter sets
- Resource utilization patterns
- Scaling efficiency across node counts
- Bottleneck identification and mitigation

**Validation and Testing**:
- Parameter feasibility validation
- Performance prediction confidence intervals
- Rollback capability for unsuccessful optimizations
- A/B testing suggestions for parameter validation

**Prerequisites**: Package must exist in pipeline with baseline configuration
**Tools to use before this**: configure_package_parameters to set baseline
**Tools to use after this**: validate_pipeline_configuration to verify optimization

Use this tool when:
- Maximizing performance for production workloads
- Adapting configurations for new hardware platforms
- Resolving performance bottlenecks through parameter tuning
- Optimizing resource utilization in shared environments
- Learning optimal parameter patterns for similar workloads"""
)
async def optimize_package_configuration_tool(
    package_name: str,
    pipeline_name: str = "",
    optimization_target: str = "performance",
    resource_constraints: dict = None
) -> dict:
    """
    AI-assisted parameter optimization for package configuration.
    
    Args:
        package_name: Name of package to optimize
        pipeline_name: Target pipeline (uses focused if empty)
        optimization_target: Target (performance, memory, network, balanced)
        resource_constraints: Available resource limits
        
    Returns:
        ConfigurationOperationResult with optimization results
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await optimize_package_configuration(
            package_name=package_name,
            pipeline_name=actual_pipeline_name,
            optimization_target=optimization_target,
            resource_constraints=resource_constraints
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in optimize_package_configuration: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in optimize_package_configuration: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="validate_pipeline_configuration",
    description="""Comprehensive validation of complete pipeline configuration for deployment readiness.

This tool performs thorough validation of all pipeline configuration aspects to ensure
successful deployment and execution. It provides detailed analysis of configuration
completeness, compatibility, and optimization opportunities.

**Validation Scope**:
- **Package Configuration**: Parameter validation and completeness
- **Environment Setup**: Module availability and variable consistency
- **Resource Requirements**: Resource adequacy and allocation
- **Dependencies**: Cross-package compatibility and dependency resolution
- **Execution Method**: Distributed execution configuration validation

**Package Validation**:
For each package in the pipeline:
- Parameter type and range validation
- Required parameter completeness check
- Cross-parameter dependency validation
- Performance impact analysis
- Resource requirement estimation

**Environment Validation**:
When check_environment=True:
- Module availability on target systems
- Environment variable consistency and completeness
- Compiler and runtime compatibility
- Library and dependency resolution
- Path accessibility and permissions

**Resource Validation**:
When check_resources=True:
- CPU requirement vs availability analysis
- Memory requirement validation
- Storage capacity and performance requirements
- Network bandwidth and latency requirements
- GPU and accelerator availability (if needed)

**Dependency Analysis**:
When check_dependencies=True:
- Package interdependency validation
- Version compatibility checking
- Execution order dependency analysis
- Resource conflict identification
- Communication pattern analysis

**Validation Results**:
- **valid**: All checks passed, ready for deployment
- **valid_with_warnings**: Usable but with performance or efficiency concerns
- **invalid**: Critical issues preventing successful execution

**Optimization Opportunities**:
Identifies potential improvements:
- Parameter tuning suggestions
- Resource allocation optimizations
- Environment configuration improvements
- Package ordering optimizations

**Prerequisites**: Pipeline must exist and have packages configured
**Tools to use before this**: configure_package_parameters for all packages
**Tools to use after this**: Address any validation issues before deployment

Use this tool when:
- Preparing pipeline for production deployment
- Troubleshooting configuration issues
- Verifying changes after configuration updates
- Ensuring reproducibility across different systems
- Quality assurance before important computational runs"""
)
async def validate_pipeline_configuration_tool(
    pipeline_name: str = "",
    check_environment: bool = True,
    check_resources: bool = True,
    check_dependencies: bool = True
) -> dict:
    """
    Comprehensive validation of complete pipeline configuration.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        check_environment: Validate environment configuration
        check_resources: Validate resource requirements
        check_dependencies: Validate package dependencies
        
    Returns:
        PipelineValidationResult with detailed validation results
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await validate_pipeline_configuration(
            pipeline_name=actual_pipeline_name,
            check_environment=check_environment,
            check_resources=check_resources,
            check_dependencies=check_dependencies
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in validate_pipeline_configuration: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in validate_pipeline_configuration: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="configure_execution_method",
    description="""Configure distributed execution method (MPI/SSH/PSSH) with intelligent parameter optimization.

This tool configures the execution method for pipeline deployment, setting up distributed
execution parameters including node allocation, process distribution, and method-specific
optimizations for HPC workloads.

**Execution Methods**:
- **LOCAL**: Single-node execution with thread-based parallelism
- **SSH**: Sequential remote execution across multiple nodes
- **PSSH**: Parallel SSH execution with simultaneous deployment
- **MPI**: Message Passing Interface for tightly-coupled parallel execution

**MPI Configuration**:
When execution_type=MPI:
- MPI implementation selection (OpenMPI, MPICH, Intel MPI)
- Process topology and binding configuration
- Communication fabric optimization (InfiniBand, Ethernet)
- Collective operation algorithm selection
- Memory management and buffer optimization

**SSH/PSSH Configuration**:
When execution_type=SSH or PSSH:
- Connection pooling and reuse optimization
- Authentication method configuration
- Timeout and retry settings
- Output aggregation and logging
- Error handling and recovery procedures

**Node and Process Allocation**:
- **Node Count**: Total nodes for distributed execution
- **Processes Per Node**: Process distribution strategy
- **CPU Binding**: Core affinity and NUMA awareness
- **Memory Allocation**: Per-process memory limits

**Advanced Configuration Options**:
- **Network Interface Selection**: Choose optimal network for communication
- **Process Placement**: NUMA-aware and topology-conscious placement
- **Communication Optimization**: Bandwidth and latency tuning
- **Fault Tolerance**: Checkpoint/restart and error recovery settings

**Resource Estimation**:
Provides estimates for:
- Total computational resources required
- Network bandwidth utilization
- Memory footprint per node
- Expected scaling efficiency

**Validation and Compatibility**:
- Hostfile validation and node accessibility
- Resource requirement vs availability
- Network connectivity and performance testing
- MPI installation and version compatibility

**Prerequisites**: Pipeline must exist, hostfile configured for distributed execution
**Tools to use before this**: get_resource_status to understand cluster capabilities
**Tools to use after this**: validate_pipeline_configuration to verify execution setup

Use this tool when:
- Setting up distributed HPC workloads
- Optimizing communication patterns for specific applications
- Configuring execution for different cluster architectures
- Tuning performance for specific network fabrics
- Preparing pipelines for production-scale execution"""
)
async def configure_execution_method_tool(
    execution_type: str,
    pipeline_name: str = "",
    hostfile_path: str = "",
    node_count: int = None,
    processes_per_node: int = None,
    additional_settings: dict = None
) -> dict:
    """
    Configure distributed execution method for pipeline.
    
    Args:
        execution_type: Type of execution (LOCAL, SSH, PSSH, MPI)
        pipeline_name: Target pipeline (uses focused if empty)
        hostfile_path: Path to hostfile for distributed execution
        node_count: Number of nodes to use
        processes_per_node: Processes per node
        additional_settings: Additional execution-specific settings
        
    Returns:
        ExecutionMethodConfig with complete execution configuration
    """
    try:
        # Convert empty strings to None and parse execution type
        actual_pipeline_name = pipeline_name if pipeline_name else None
        actual_hostfile_path = hostfile_path if hostfile_path else None
        
        # Convert string to ExecutionType enum
        exec_type = ExecutionType(execution_type.lower())
        
        result = await configure_execution_method(
            execution_type=exec_type,
            pipeline_name=actual_pipeline_name,
            hostfile_path=actual_hostfile_path,
            node_count=node_count,
            processes_per_node=processes_per_node,
            additional_settings=additional_settings
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in configure_execution_method: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in configure_execution_method: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="manage_interceptors",
    description="""Configure LD_PRELOAD interceptors and monitoring tools for comprehensive pipeline instrumentation.

This tool manages interceptor configuration for HPC pipelines, providing intelligent
setup of profiling, tracing, and monitoring tools. It handles LD_PRELOAD ordering,
compatibility validation, and cross-interceptor coordination.

**Interceptor Management Actions**:
- **add**: Add new interceptor to pipeline with configuration
- **remove**: Remove interceptor and clean up configuration
- **list**: Display current interceptor setup and status
- **reorder**: Optimize LD_PRELOAD order for compatibility and performance

**Common HPC Interceptors**:
- **Darshan**: I/O characterization and performance analysis
- **PyMonitor**: Real-time performance monitoring and visualization
- **ASAN**: Memory error detection and debugging
- **Intel VTune**: CPU performance profiling and optimization
- **NVIDIA Nsight**: GPU performance analysis and debugging

**LD_PRELOAD Order Management**:
Critical for interceptor compatibility:
- Automatic dependency resolution between interceptors
- Compatibility matrix validation
- Performance impact minimization
- Conflict detection and resolution

**Target Package Selection**:
- **All packages**: Apply interceptor to entire pipeline
- **Specific packages**: Target particular applications
- **Package types**: Target all services, applications, or interceptors
- **Conditional targeting**: Apply based on execution conditions

**Configuration Management**:
- **Interceptor-specific parameters**: Log paths, sampling rates, output formats
- **Output file management**: Automated naming and organization
- **Performance tuning**: Overhead minimization and sampling optimization
- **Integration settings**: Cross-tool data correlation and analysis

**Compatibility Analysis**:
The tool performs intelligent compatibility checking:
- Memory layout conflicts between interceptors
- Signal handler interference detection
- Library symbol conflicts and resolution
- Performance overhead accumulation analysis

**Output Management**:
- Automated output file naming and organization
- Cross-interceptor data correlation
- Post-execution analysis preparation
- Data format standardization and conversion

**Prerequisites**: Pipeline must exist with target packages
**Tools to use before this**: get_pipeline_composition to see available packages
**Tools to use after this**: validate_pipeline_configuration to verify interceptor setup

Use this tool when:
- Setting up performance monitoring for production runs
- Debugging performance issues with profiling tools
- Collecting I/O traces for storage system analysis
- Monitoring resource utilization across pipeline execution
- Comparing performance across different configurations"""
)
async def manage_interceptors_tool(
    action: str,
    interceptor_name: str = "",
    pipeline_name: str = "",
    target_packages: list = None,
    configuration: dict = None
) -> dict:
    """
    Configure LD_PRELOAD interceptors and monitoring tools.
    
    Args:
        action: Action to perform (add, remove, list, reorder)
        interceptor_name: Name of interceptor package
        pipeline_name: Target pipeline (uses focused if empty)
        target_packages: Packages to intercept (all if None)
        configuration: Interceptor-specific configuration
        
    Returns:
        List of InterceptorConfiguration showing current interceptor setup
    """
    try:
        # Convert empty strings to None
        actual_interceptor_name = interceptor_name if interceptor_name else None
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await manage_interceptors(
            action=action,
            interceptor_name=actual_interceptor_name,
            pipeline_name=actual_pipeline_name,
            target_packages=target_packages,
            configuration=configuration
        )
        return [interceptor.model_dump() for interceptor in result]
    except ConfigurationError as e:
        logger.error(f"Configuration error in manage_interceptors: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in manage_interceptors: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="optimize_resource_allocation",
    description="""Intelligent resource mapping and scheduling optimization for HPC pipeline execution.

This advanced tool optimizes resource allocation across cluster nodes, considering package
requirements, hardware capabilities, and execution patterns to maximize performance and
efficiency for complex HPC workloads.

**Optimization Strategies**:
- **balanced**: Even distribution across all resources
- **cpu_intensive**: Optimize for computational workloads
- **io_intensive**: Optimize for I/O-heavy applications  
- **memory_intensive**: Optimize for memory-constrained workloads
- **network_intensive**: Optimize for communication-heavy applications

**Resource Allocation Analysis**:
- **Package Profiling**: CPU, memory, I/O, and network requirements
- **Node Capabilities**: Hardware specifications and performance characteristics
- **Workload Patterns**: Computational vs I/O phases, communication patterns
- **Contention Analysis**: Resource conflicts and bottleneck identification

**Multi-Dimensional Optimization**:
- **CPU Allocation**: Core assignment, NUMA awareness, thread affinity
- **Memory Management**: NUMA-aware allocation, shared memory optimization
- **I/O Optimization**: Storage device utilization, bandwidth allocation
- **Network Optimization**: Fabric utilization, communication locality

**Load Balancing Strategies**:
- **Static Balancing**: Pre-computed optimal allocation
- **Dynamic Balancing**: Runtime adaptation to workload changes
- **Hierarchical Balancing**: Multi-level resource management
- **Predictive Balancing**: Machine learning-based allocation

**Node Assignment Optimization**:
Intelligent package-to-node mapping:
- **Service Placement**: Storage and database services on optimal nodes
- **Compute Distribution**: Parallel applications across compute nodes
- **Communication Optimization**: Minimize inter-node communication overhead
- **Fault Tolerance**: Redundancy and recovery planning

**Performance Estimation**:
Provides detailed performance predictions:
- Overall pipeline efficiency estimation
- Resource utilization projections
- Communication overhead analysis
- Scaling efficiency predictions

**Constraint Handling**:
- **Hard Constraints**: Absolute limits (memory, CPU count)
- **Soft Constraints**: Preferences and optimization targets
- **Policy Constraints**: Organizational resource allocation policies
- **Dynamic Constraints**: Runtime adaptation to changing conditions

**Prerequisites**: Pipeline must exist with configured packages
**Tools to use before this**: get_resource_status to understand cluster capabilities
**Tools to use after this**: configure_execution_method to implement allocation

Use this tool when:
- Optimizing performance for large-scale HPC deployments
- Resolving resource contention in shared cluster environments
- Maximizing efficiency for production computational workflows
- Planning resource allocation for new hardware platforms
- Analyzing and improving existing deployment performance"""
)
async def optimize_resource_allocation_tool(
    pipeline_name: str = "",
    optimization_strategy: str = "balanced",
    resource_constraints: dict = None,
    node_preferences: dict = None
) -> dict:
    """
    Optimize resource mapping and scheduling for pipeline.
    
    Args:
        pipeline_name: Target pipeline (uses focused if empty)
        optimization_strategy: Strategy (balanced, cpu_intensive, io_intensive, memory_intensive)
        resource_constraints: Available resource limits
        node_preferences: Preferred node assignments for packages
        
    Returns:
        ResourceAllocationConfig with optimized resource mapping
    """
    try:
        # Convert empty string to None for pipeline_name
        actual_pipeline_name = pipeline_name if pipeline_name else None
        
        result = await optimize_resource_allocation(
            pipeline_name=actual_pipeline_name,
            optimization_strategy=optimization_strategy,
            resource_constraints=resource_constraints,
            node_preferences=node_preferences
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in optimize_resource_allocation: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in optimize_resource_allocation: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="integrate_scspkg_packages",
    description="""Integrate SCSPKG (Spack-based) packages with Jarvis pipeline configuration.

This tool provides seamless integration between Jarvis pipelines and SCSPKG/Spack package
management, enabling use of Spack-built scientific software packages within HPC workflows
with proper dependency management and environment configuration.

**SCSPKG Integration Features**:
- **Package Discovery**: Find and validate Spack packages for HPC workflows
- **Dependency Resolution**: Automatic dependency tree analysis and management
- **Build Configuration**: Optimize build options for target hardware
- **Environment Integration**: Seamless environment variable and module setup
- **Version Management**: Handle multiple package versions and conflicts

**Spack Specification Handling**:
Supports complete Spack spec syntax:
- **Package@version**: Specific version requirements
- **%compiler**: Compiler selection and optimization
- **+variants**: Feature enablement and customization
- **arch=architecture**: Target architecture specification
- **^dependencies**: Dependency version constraints

**Common SCSPKG Packages**:
- **MPI Implementations**: OpenMPI, MPICH, Intel MPI with optimizations
- **Scientific Libraries**: HDF5, NetCDF, FFTW, BLAS/LAPACK implementations
- **Simulation Packages**: OpenFOAM, GROMACS, LAMMPS, Quantum ESPRESSO
- **Analysis Tools**: ParaView, VisIt, Matplotlib, NumPy/SciPy stacks

**Build Optimization**:
- **Compiler Selection**: GCC, Intel, LLVM with version optimization
- **Architecture Targeting**: CPU-specific optimizations and vectorization
- **Dependency Optimization**: Shared vs static linking, library selection
- **Performance Tuning**: BLAS/LAPACK backends, MPI implementations

**Environment Management**:
Automatic environment setup:
- **Module Integration**: Spack module generation and loading
- **Path Management**: Binary, library, and include path configuration
- **Variable Setup**: Package-specific environment variables
- **Dependency Chaining**: Cascading environment from dependencies

**Integration Validation**:
- **Package Availability**: Spack package existence and buildability
- **Dependency Compatibility**: Version conflict resolution
- **Architecture Compatibility**: Target system validation
- **License Compliance**: Open source license verification

**Prerequisites**: SCSPKG/Spack must be available and configured
**Tools to use before this**: get_package_info to understand package requirements
**Tools to use after this**: configure_package_parameters to set integrated package options

Use this tool when:
- Integrating scientific software not available in standard Jarvis repositories
- Using specific versions or build configurations of scientific packages
- Leveraging Spack's extensive scientific software ecosystem
- Managing complex dependency trees for scientific workflows
- Ensuring reproducible builds across different HPC systems"""
)
async def integrate_scspkg_packages_tool(
    package_name: str,
    pipeline_name: str = "",
    spack_spec: str = "",
    build_options: dict = None
) -> dict:
    """
    Integrate SCSPKG packages with Jarvis pipeline.
    
    Args:
        package_name: SCSPKG package name to integrate
        pipeline_name: Target pipeline (uses focused if empty)
        spack_spec: Spack package specification
        build_options: Build configuration options
        
    Returns:
        SCSSPkgIntegrationInfo with integration status and configuration
    """
    try:
        # Convert empty strings to None
        actual_pipeline_name = pipeline_name if pipeline_name else None
        actual_spack_spec = spack_spec if spack_spec else None
        
        result = await integrate_scspkg_packages(
            package_name=package_name,
            pipeline_name=actual_pipeline_name,
            spack_spec=actual_spack_spec,
            build_options=build_options
        )
        return result.model_dump()
    except ConfigurationError as e:
        logger.error(f"Configuration error in integrate_scspkg_packages: {e}")
        return {"error": str(e), "type": "configuration_error"}
    except Exception as e:
        logger.error(f"Unexpected error in integrate_scspkg_packages: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

# ══════════════════════════════════════════════════════════════════════════
# SERVER SUMMARY
# ══════════════════════════════════════════════════════════════════════════

# This Jarvis MCP server implements comprehensive HPC workflow management across
# Phases 1, 2 & 3:
#
# Phase 1: Discoverability (5 tools) - Package discovery and resource exploration
# Phase 2: Composition (14 tools) - Pipeline design and package management  
# Phase 3: Configuration (10 tools) - Parameter optimization and environment setup
#
# Total: 29 tools across Phases 1 & 2 & 3 providing complete workflow lifecycle support

def main():
    """
    Main entry point to start the FastMCP server using the specified transport.
    Chooses between stdio and SSE based on MCP_TRANSPORT environment variable.
    """
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    if transport == "sse":
        host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_SSE_PORT", "8000"))
        print(f"Starting Jarvis MCP on {host}:{port}", file=sys.stderr)
        mcp.run(transport="sse", host=host, port=port)
    else:
        print("Starting Jarvis MCP with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()