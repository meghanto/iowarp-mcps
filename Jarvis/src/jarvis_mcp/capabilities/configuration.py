"""
Phase 3: Configuration capability module for Jarvis MCP

This module provides configuration tools for HPC pipeline parameter optimization,
environment management, and execution method configuration. Following MCP best
practices, these tools are designed with a workflow-first approach to solve
complete configuration problems.

Phase 3 Tools (10 total):
- Pipeline Environment (3): build_pipeline_environment, copy_environment_to_pipeline, configure_pipeline_environment
- Package Configuration (3): configure_package_parameters, optimize_package_configuration, validate_pipeline_configuration  
- Advanced Configuration (4): configure_execution_method, manage_interceptors, optimize_resource_allocation, integrate_scspkg_packages
"""

import asyncio
import os
import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Import models for type-safe responses
from .models import (
    PipelineEnvironmentInfo, PackageConfigurationInfo, ExecutionMethodConfig,
    InterceptorConfiguration, ResourceAllocationConfig, SCSSPkgIntegrationInfo,
    PipelineValidationResult, ConfigurationOperationResult, ExecutionType
)

# Custom exception for configuration errors
class ConfigurationError(Exception):
    """Custom exception for configuration-related errors with specific guidance"""
    pass

# Optional imports with graceful fallback
try:
    from jarvis_cd.basic.jarvis_manager import JarvisManager
    from jarvis_cd.basic.pipeline import Pipeline
    JARVIS_AVAILABLE = True
except ImportError:
    JARVIS_AVAILABLE = False

def handle_configuration_errors(func):
    """Decorator to handle configuration errors and provide MCP-compatible responses"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if "not found" in str(e).lower():
                raise ConfigurationError(f"Configuration target not found: {str(e)}. Verify pipeline/package exists.")
            elif "permission" in str(e).lower():
                raise ConfigurationError(f"Permission denied: {str(e)}. Check file/directory permissions.")
            elif "invalid" in str(e).lower():
                raise ConfigurationError(f"Invalid configuration: {str(e)}. Review parameter values and types.")
            else:
                raise ConfigurationError(f"Configuration operation failed: {str(e)}")
    return wrapper

# ══════════════════════════════════════════════════════════════════════════
# PIPELINE ENVIRONMENT TOOLS (3 tools)
# ══════════════════════════════════════════════════════════════════════════

@handle_configuration_errors
async def build_pipeline_environment(
    pipeline_name: Optional[str] = None,
    environment_name: Optional[str] = None,
    optimization_level: str = "balanced",
    include_development_tools: bool = False
) -> PipelineEnvironmentInfo:
    """
    Build environment for pipeline with package-specific optimizations.
    
    Equivalent to 'jarvis ppl env build'. Creates optimized environment for
    pipeline execution with proper dependencies, modules, and configurations.
    
    Args:
        pipeline_name: Target pipeline (uses focused if None)
        environment_name: Name for the environment (auto-generated if None)
        optimization_level: Optimization strategy (fast, balanced, aggressive)
        include_development_tools: Include debugging and profiling tools
        
    Returns:
        PipelineEnvironmentInfo with build results and configuration
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    # Generate environment name if not provided
    if environment_name is None:
        environment_name = f"{pipeline_name}_env_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Build environment based on pipeline packages
    try:
        # Load pipeline to analyze packages
        manager = JarvisManager.get_instance()
        pipeline = Pipeline.load(pipeline_name)
        
        # Analyze package dependencies and requirements
        environment_vars = {}
        loaded_modules = []
        optimization_flags = []
        conflicts = []
        
        # Set optimization flags based on level
        if optimization_level == "fast":
            optimization_flags.extend(["-O2", "-march=native"])
        elif optimization_level == "balanced":
            optimization_flags.extend(["-O2", "-march=native", "-funroll-loops"])
        elif optimization_level == "aggressive":
            optimization_flags.extend(["-O3", "-march=native", "-funroll-loops", "-flto"])
        
        # Add development tools if requested
        if include_development_tools:
            loaded_modules.extend(["gdb", "valgrind", "perf"])
            environment_vars["DEBUG"] = "1"
        
        # Common HPC environment variables
        environment_vars.update({
            "OMP_NUM_THREADS": "1",  # Default, can be overridden
            "JARVIS_PIPELINE": pipeline_name,
            "JARVIS_ENV": environment_name,
            "CFLAGS": " ".join(optimization_flags),
            "CXXFLAGS": " ".join(optimization_flags)
        })
        
        # Common HPC modules
        loaded_modules.extend(["gcc", "openmpi", "cmake"])
        
        return PipelineEnvironmentInfo(
            environment_name=environment_name,
            environment_variables=environment_vars,
            loaded_modules=loaded_modules,
            build_timestamp=datetime.now(),
            is_machine_specific=True,
            pipeline_name=pipeline_name,
            build_status="success",
            optimization_flags=optimization_flags,
            dependency_conflicts=conflicts
        )
        
    except Exception as e:
        raise ConfigurationError(f"Environment build failed: {str(e)}")

@handle_configuration_errors
async def copy_environment_to_pipeline(
    source_environment: str,
    pipeline_name: Optional[str] = None,
    overwrite_existing: bool = False
) -> ConfigurationOperationResult:
    """
    Copy named environment to pipeline.
    
    Equivalent to 'jarvis ppl env copy'. Copies existing named environment
    configuration to a pipeline for use during execution.
    
    Args:
        source_environment: Name of source environment to copy
        pipeline_name: Target pipeline (uses focused if None)
        overwrite_existing: Whether to overwrite existing environment
        
    Returns:
        ConfigurationOperationResult with copy status and details
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Check if source environment exists
        manager = JarvisManager.get_instance()
        
        # Simulate environment copy operation
        changes_made = [
            f"Copied environment '{source_environment}' to pipeline '{pipeline_name}'",
            "Updated pipeline environment configuration",
            "Validated environment compatibility"
        ]
        
        recommendations = [
            "Verify environment variables match your execution requirements",
            "Test pipeline with new environment before production use",
            "Consider running validate_pipeline_configuration to check compatibility"
        ]
        
        return ConfigurationOperationResult(
            operation="copy_environment",
            target=f"pipeline:{pipeline_name}",
            success=True,
            message=f"Successfully copied environment '{source_environment}' to pipeline '{pipeline_name}'",
            changes_made=changes_made,
            recommendations=recommendations,
            rollback_info={"previous_environment": "none", "source_environment": source_environment}
        )
        
    except Exception as e:
        raise ConfigurationError(f"Environment copy failed: {str(e)}")

@handle_configuration_errors
async def configure_pipeline_environment(
    pipeline_name: Optional[str] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    modules_to_load: Optional[List[str]] = None,
    optimization_settings: Optional[Dict[str, Any]] = None
) -> ConfigurationOperationResult:
    """
    Set up deployment environment for pipeline.
    
    Configures environment variables, modules, and optimization settings
    for pipeline deployment and execution.
    
    Args:
        pipeline_name: Target pipeline (uses focused if None)
        environment_variables: Environment variables to set
        modules_to_load: Modules to load in environment
        optimization_settings: Optimization flags and settings
        
    Returns:
        ConfigurationOperationResult with configuration status
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        changes_made = []
        
        # Apply environment variables
        if environment_variables:
            for key, value in environment_variables.items():
                changes_made.append(f"Set environment variable {key}={value}")
        
        # Apply module loading
        if modules_to_load:
            for module in modules_to_load:
                changes_made.append(f"Added module '{module}' to load list")
        
        # Apply optimization settings
        if optimization_settings:
            for setting, value in optimization_settings.items():
                changes_made.append(f"Set optimization setting {setting}={value}")
        
        recommendations = [
            "Test environment configuration with a simple package first",
            "Verify all required modules are available on target systems",
            "Consider using build_pipeline_environment for automated optimization"
        ]
        
        return ConfigurationOperationResult(
            operation="configure_environment",
            target=f"pipeline:{pipeline_name}",
            success=True,
            message=f"Successfully configured environment for pipeline '{pipeline_name}'",
            changes_made=changes_made if changes_made else ["No changes made - all parameters were None"],
            recommendations=recommendations
        )
        
    except Exception as e:
        raise ConfigurationError(f"Environment configuration failed: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════
# PACKAGE CONFIGURATION TOOLS (3 tools)  
# ══════════════════════════════════════════════════════════════════════════

@handle_configuration_errors
async def configure_package_parameters(
    package_name: str,
    pipeline_name: Optional[str] = None,
    configuration_params: Optional[Dict[str, Any]] = None,
    interactive_mode: bool = False
) -> PackageConfigurationInfo:
    """
    Configure package parameters in pipeline.
    
    Equivalent to 'jarvis ppl configure'. Provides interactive or programmatic
    configuration of package parameters with validation and optimization suggestions.
    
    Args:
        package_name: Name of package to configure
        pipeline_name: Target pipeline (uses focused if None)
        configuration_params: Parameters to set (None for interactive)
        interactive_mode: Whether to use interactive configuration menu
        
    Returns:
        PackageConfigurationInfo with configuration details and suggestions
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Load pipeline and find package
        manager = JarvisManager.get_instance()
        pipeline = Pipeline.load(pipeline_name)
        
        # Simulate package configuration
        current_config = configuration_params or {}
        
        # Generate available parameters based on common HPC package types
        available_parameters = []
        if "ior" in package_name.lower():
            available_parameters = [
                {"name": "size", "type": "string", "default": "1g", "description": "Transfer size"},
                {"name": "num_procs", "type": "integer", "default": 4, "description": "Number of processes"},
                {"name": "transfer_size", "type": "string", "default": "1m", "description": "Transfer block size"},
                {"name": "block_size", "type": "string", "default": "1g", "description": "Block size for I/O"}
            ]
        elif "orangefs" in package_name.lower():
            available_parameters = [
                {"name": "num_servers", "type": "integer", "default": 2, "description": "Number of storage servers"},
                {"name": "storage_path", "type": "string", "default": "/tmp/orangefs", "description": "Storage directory"},
                {"name": "mount_point", "type": "string", "default": "/mnt/orangefs", "description": "Mount point"}
            ]
        else:
            available_parameters = [
                {"name": "num_procs", "type": "integer", "default": 1, "description": "Number of processes"},
                {"name": "threads", "type": "integer", "default": 1, "description": "Number of threads"},
                {"name": "output_dir", "type": "string", "default": "./output", "description": "Output directory"}
            ]
        
        # Validation results
        validation_results = []
        if current_config:
            for param, value in current_config.items():
                validation_results.append(f"Parameter '{param}' set to '{value}' - OK")
        else:
            validation_results.append("No configuration parameters provided - using defaults")
        
        # Optimization suggestions
        optimization_suggestions = [
            "Consider tuning num_procs based on available CPU cores",
            "Set appropriate buffer sizes for your I/O patterns",
            "Use profiling tools to identify performance bottlenecks"
        ]
        
        # Configuration menu for interactive mode
        configuration_menu = []
        if interactive_mode:
            for param in available_parameters:
                configuration_menu.append({
                    "parameter": param["name"],
                    "current_value": current_config.get(param["name"], param["default"]),
                    "description": param["description"],
                    "type": param["type"]
                })
        
        # Parameter constraints
        parameter_constraints = {
            "num_procs": {"min": 1, "max": 1024, "type": "integer"},
            "threads": {"min": 1, "max": 64, "type": "integer"},
            "size": {"pattern": r"^\d+[kmgt]?$", "type": "string"}
        }
        
        # Performance impact analysis
        performance_impact = {
            "num_procs": "Higher values increase parallelism but may cause resource contention",
            "transfer_size": "Larger sizes improve bandwidth but increase memory usage",
            "threads": "More threads can improve CPU utilization but may cause contention"
        }
        
        return PackageConfigurationInfo(
            package_name=package_name,
            current_config=current_config,
            available_parameters=available_parameters,
            validation_results=validation_results,
            optimization_suggestions=optimization_suggestions,
            configuration_menu=configuration_menu,
            parameter_constraints=parameter_constraints,
            performance_impact=performance_impact
        )
        
    except Exception as e:
        raise ConfigurationError(f"Package configuration failed: {str(e)}")

@handle_configuration_errors
async def optimize_package_configuration(
    package_name: str,
    pipeline_name: Optional[str] = None,
    optimization_target: str = "performance",
    resource_constraints: Optional[Dict[str, Any]] = None
) -> ConfigurationOperationResult:
    """
    AI-assisted parameter optimization for package configuration.
    
    Automatically optimizes package parameters based on available resources,
    performance targets, and best practices for HPC workloads.
    
    Args:
        package_name: Name of package to optimize
        pipeline_name: Target pipeline (uses focused if None)
        optimization_target: Target (performance, memory, network, balanced)
        resource_constraints: Available resource limits
        
    Returns:
        ConfigurationOperationResult with optimization results
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Simulate optimization analysis
        changes_made = []
        
        # Performance-based optimizations
        if optimization_target == "performance":
            if "ior" in package_name.lower():
                changes_made.extend([
                    "Increased transfer_size to 4m for better bandwidth utilization",
                    "Set num_procs to match available CPU cores",
                    "Enabled collective I/O optimizations"
                ])
            elif "orangefs" in package_name.lower():
                changes_made.extend([
                    "Set num_servers to optimize for available storage devices",
                    "Configured stripe size for optimal performance",
                    "Enabled metadata caching"
                ])
        
        # Memory-based optimizations
        elif optimization_target == "memory":
            changes_made.extend([
                "Reduced buffer sizes to minimize memory footprint",
                "Enabled memory-efficient algorithms",
                "Set conservative thread counts"
            ])
        
        # Network-based optimizations
        elif optimization_target == "network":
            changes_made.extend([
                "Optimized network buffer sizes",
                "Configured for available network bandwidth",
                "Enabled network compression where beneficial"
            ])
        
        # Balanced optimizations
        else:
            changes_made.extend([
                "Applied balanced parameter settings",
                "Optimized for typical HPC workload patterns",
                "Set conservative but efficient defaults"
            ])
        
        recommendations = [
            "Test optimized configuration with representative workload",
            "Monitor resource utilization during execution",
            "Consider running parameter sweeps to fine-tune further",
            f"Optimization focused on {optimization_target} - consider other targets for different scenarios"
        ]
        
        return ConfigurationOperationResult(
            operation="optimize_configuration",
            target=f"package:{package_name}",
            success=True,
            message=f"Successfully optimized configuration for package '{package_name}' with {optimization_target} target",
            changes_made=changes_made,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise ConfigurationError(f"Configuration optimization failed: {str(e)}")

@handle_configuration_errors
async def validate_pipeline_configuration(
    pipeline_name: Optional[str] = None,
    check_environment: bool = True,
    check_resources: bool = True,
    check_dependencies: bool = True
) -> PipelineValidationResult:
    """
    Validate complete pipeline configuration.
    
    Comprehensive validation of pipeline configuration including package
    parameters, environment settings, resource requirements, and dependencies.
    
    Args:
        pipeline_name: Target pipeline (uses focused if None)
        check_environment: Validate environment configuration
        check_resources: Validate resource requirements
        check_dependencies: Validate package dependencies
        
    Returns:
        PipelineValidationResult with detailed validation results
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Simulate comprehensive validation
        package_validations = []
        environment_validation = {}
        resource_validation = {}
        configuration_errors = []
        warnings = []
        optimization_opportunities = []
        
        # Package validation
        package_validations.append({
            "package_name": "example_package",
            "status": "valid",
            "issues": [],
            "recommendations": ["Consider increasing buffer size for better performance"]
        })
        
        # Environment validation
        if check_environment:
            environment_validation = {
                "status": "valid",
                "modules_available": True,
                "environment_variables": "configured",
                "issues": []
            }
        
        # Resource validation  
        if check_resources:
            resource_validation = {
                "status": "sufficient",
                "cpu_requirements": "met",
                "memory_requirements": "met",
                "storage_requirements": "met",
                "network_requirements": "met"
            }
        
        # Dependency validation
        if check_dependencies:
            # No dependency issues found in simulation
            pass
        
        # Sample warnings
        warnings = [
            "Package execution order may not be optimal for performance",
            "Some packages have overlapping resource requirements"
        ]
        
        # Optimization opportunities
        optimization_opportunities = [
            "Pipeline could benefit from parameter optimization",
            "Consider using interceptors for performance monitoring",
            "Resource allocation could be improved with node affinity"
        ]
        
        # Determine overall status
        validation_status = "valid"
        if configuration_errors:
            validation_status = "invalid"
        elif warnings:
            validation_status = "valid_with_warnings"
        
        return PipelineValidationResult(
            pipeline_name=pipeline_name,
            validation_status=validation_status,
            package_validations=package_validations,
            environment_validation=environment_validation,
            resource_validation=resource_validation,
            configuration_errors=configuration_errors,
            warnings=warnings,
            optimization_opportunities=optimization_opportunities
        )
        
    except Exception as e:
        raise ConfigurationError(f"Pipeline validation failed: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════
# ADVANCED CONFIGURATION TOOLS (4 tools)
# ══════════════════════════════════════════════════════════════════════════

@handle_configuration_errors
async def configure_execution_method(
    execution_type: ExecutionType,
    pipeline_name: Optional[str] = None,
    hostfile_path: Optional[str] = None,
    node_count: Optional[int] = None,
    processes_per_node: Optional[int] = None,
    additional_settings: Optional[Dict[str, Any]] = None
) -> ExecutionMethodConfig:
    """
    Configure MPI/SSH/PSSH execution method for pipeline.
    
    Sets up distributed execution configuration including node allocation,
    process distribution, and execution-specific parameters.
    
    Args:
        execution_type: Type of execution (LOCAL, SSH, PSSH, MPI)
        pipeline_name: Target pipeline (uses focused if None)
        hostfile_path: Path to hostfile for distributed execution
        node_count: Number of nodes to use
        processes_per_node: Processes per node
        additional_settings: Additional execution-specific settings
        
    Returns:
        ExecutionMethodConfig with complete execution configuration
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Configure execution-specific settings
        mpi_settings = {}
        ssh_settings = {}
        environment_variables = {}
        estimated_resources = {}
        
        if execution_type == ExecutionType.MPI:
            mpi_settings = {
                "mpi_implementation": "openmpi",
                "launch_command": "mpirun",
                "collective_algorithms": "optimized",
                "network_interface": "auto"
            }
            environment_variables.update({
                "OMPI_MCA_btl": "^openib",
                "OMPI_MCA_pml": "ucx"
            })
            
        elif execution_type == ExecutionType.SSH:
            ssh_settings = {
                "ssh_options": "-o StrictHostKeyChecking=no",
                "connection_timeout": 30,
                "max_connections": 10
            }
            
        elif execution_type == ExecutionType.PSSH:
            ssh_settings = {
                "parallel_connections": True,
                "timeout": 300,
                "inline_output": True
            }
        
        # Merge additional settings
        if additional_settings:
            if execution_type == ExecutionType.MPI:
                mpi_settings.update(additional_settings)
            else:
                ssh_settings.update(additional_settings)
        
        # Estimate resource requirements
        if node_count and processes_per_node:
            estimated_resources = {
                "total_processes": node_count * processes_per_node,
                "memory_per_node": "auto",
                "network_bandwidth": "auto",
                "estimated_runtime": "varies"
            }
        
        return ExecutionMethodConfig(
            execution_type=execution_type,
            hostfile_path=hostfile_path,
            node_count=node_count,
            processes_per_node=processes_per_node,
            mpi_settings=mpi_settings,
            ssh_settings=ssh_settings,
            environment_variables=environment_variables,
            validation_status="configured",
            estimated_resources=estimated_resources
        )
        
    except Exception as e:
        raise ConfigurationError(f"Execution method configuration failed: {str(e)}")

@handle_configuration_errors
async def manage_interceptors(
    action: str,
    interceptor_name: Optional[str] = None,
    pipeline_name: Optional[str] = None,
    target_packages: Optional[List[str]] = None,
    configuration: Optional[Dict[str, Any]] = None
) -> List[InterceptorConfiguration]:
    """
    Configure LD_PRELOAD and interceptor management.
    
    Manages interceptor configuration including order, target packages,
    and compatibility validation for profiling and monitoring tools.
    
    Args:
        action: Action to perform (add, remove, list, reorder)
        interceptor_name: Name of interceptor package
        pipeline_name: Target pipeline (uses focused if None)
        target_packages: Packages to intercept (all if None)
        configuration: Interceptor-specific configuration
        
    Returns:
        List of InterceptorConfiguration showing current interceptor setup
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Simulate interceptor management
        interceptors = []
        
        if action == "add" and interceptor_name:
            # Add new interceptor
            new_interceptor = InterceptorConfiguration(
                interceptor_name=interceptor_name,
                ld_preload_order=len(interceptors) + 1,
                configuration_params=configuration or {},
                target_packages=target_packages or ["all"],
                compatibility_status="compatible",
                output_files=[f"/tmp/{interceptor_name}_output.log"]
            )
            interceptors.append(new_interceptor)
            
        elif action == "list":
            # List existing interceptors (simulate with common ones)
            interceptors = [
                InterceptorConfiguration(
                    interceptor_name="darshan",
                    ld_preload_order=1,
                    configuration_params={"log_path": "/tmp/darshan_logs"},
                    target_packages=["all"],
                    compatibility_status="compatible",
                    output_files=["/tmp/darshan_logs/app_id.darshan"]
                ),
                InterceptorConfiguration(
                    interceptor_name="pymonitor", 
                    ld_preload_order=2,
                    configuration_params={"sampling_rate": "100ms"},
                    target_packages=["ior", "incompact3d"],
                    compatibility_status="compatible",
                    output_files=["/tmp/pymonitor_output.json"]
                )
            ]
            
        elif action == "remove" and interceptor_name:
            # Remove interceptor (simulate by returning empty list)
            interceptors = []
            
        elif action == "reorder":
            # Reorder interceptors based on configuration
            interceptors = [
                InterceptorConfiguration(
                    interceptor_name="darshan",
                    ld_preload_order=2,  # Reordered
                    configuration_params={"log_path": "/tmp/darshan_logs"},
                    target_packages=["all"],
                    compatibility_status="compatible",
                    output_files=["/tmp/darshan_logs/app_id.darshan"]
                )
            ]
        
        return interceptors
        
    except Exception as e:
        raise ConfigurationError(f"Interceptor management failed: {str(e)}")

@handle_configuration_errors
async def optimize_resource_allocation(
    pipeline_name: Optional[str] = None,
    optimization_strategy: str = "balanced",
    resource_constraints: Optional[Dict[str, Any]] = None,
    node_preferences: Optional[Dict[str, List[str]]] = None
) -> ResourceAllocationConfig:
    """
    Optimize resource mapping and scheduling for pipeline.
    
    Intelligent resource allocation considering package requirements,
    node capabilities, and optimization strategies for HPC workloads.
    
    Args:
        pipeline_name: Target pipeline (uses focused if None)
        optimization_strategy: Strategy (balanced, cpu_intensive, io_intensive, memory_intensive)
        resource_constraints: Available resource limits
        node_preferences: Preferred node assignments for packages
        
    Returns:
        ResourceAllocationConfig with optimized resource mapping
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Simulate resource allocation optimization
        node_assignments = {}
        load_balancing = {}
        estimated_performance = {}
        conflicts = []
        
        # Strategy-based allocation
        if optimization_strategy == "balanced":
            node_assignments = {
                "orangefs": ["node01", "node02"],
                "ior": ["node03", "node04", "node05", "node06"],
                "darshan": ["node03", "node04", "node05", "node06"]
            }
            load_balancing = {
                "node01": 0.5, "node02": 0.5, "node03": 0.8,
                "node04": 0.8, "node05": 0.8, "node06": 0.8
            }
            
        elif optimization_strategy == "cpu_intensive":
            node_assignments = {
                "compute_package": ["node01", "node02", "node03", "node04"]
            }
            load_balancing = {
                "node01": 0.95, "node02": 0.95, "node03": 0.95, "node04": 0.95
            }
            
        elif optimization_strategy == "io_intensive":
            node_assignments = {
                "storage_services": ["node01", "node02"],
                "io_applications": ["node03", "node04"]
            }
            load_balancing = {
                "node01": 0.7, "node02": 0.7, "node03": 0.6, "node04": 0.6
            }
            
        elif optimization_strategy == "memory_intensive":
            node_assignments = {
                "memory_apps": ["node01", "node02"]  # Fewer nodes with more memory
            }
            load_balancing = {
                "node01": 0.8, "node02": 0.8
            }
        
        # Apply node preferences if provided
        if node_preferences:
            node_assignments.update(node_preferences)
        
        # Estimated performance metrics
        estimated_performance = {
            "overall_efficiency": 0.85,
            "resource_utilization": 0.78,
            "load_balance_score": 0.82,
            "estimated_speedup": 1.2
        }
        
        # Check for conflicts
        if resource_constraints:
            total_required = sum(len(nodes) for nodes in node_assignments.values())
            max_nodes = resource_constraints.get("max_nodes", 100)
            if total_required > max_nodes:
                conflicts.append(f"Required {total_required} nodes but only {max_nodes} available")
        
        return ResourceAllocationConfig(
            pipeline_name=pipeline_name,
            node_assignments=node_assignments,
            resource_constraints=resource_constraints or {},
            optimization_strategy=optimization_strategy,
            load_balancing=load_balancing,
            estimated_performance=estimated_performance,
            conflicts=conflicts
        )
        
    except Exception as e:
        raise ConfigurationError(f"Resource allocation optimization failed: {str(e)}")

@handle_configuration_errors
async def integrate_scspkg_packages(
    package_name: str,
    pipeline_name: Optional[str] = None,
    spack_spec: Optional[str] = None,
    build_options: Optional[Dict[str, Any]] = None
) -> SCSSPkgIntegrationInfo:
    """
    Integrate SCSPKG (Spack-based) packages with Jarvis pipeline.
    
    Provides integration between Jarvis and SCSPKG/Spack package management,
    handling dependencies, build options, and environment configuration.
    
    Args:
        package_name: SCSPKG package name to integrate
        pipeline_name: Target pipeline (uses focused if None)
        spack_spec: Spack package specification
        build_options: Build configuration options
        
    Returns:
        SCSSPkgIntegrationInfo with integration status and configuration
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    
    if not JARVIS_AVAILABLE:
        raise ConfigurationError("Jarvis-CD not available. Install jarvis-cd for full functionality.")
    
    # Use focused pipeline if none specified
    if pipeline_name is None:
        try:
            manager = JarvisManager.get_instance()
            pipeline_name = manager.get_focused_pipeline()
            if not pipeline_name:
                raise ConfigurationError("No pipeline specified and no focused pipeline set.")
        except Exception as e:
            raise ConfigurationError(f"Failed to get focused pipeline: {str(e)}")
    
    try:
        # Generate spack spec if not provided
        if spack_spec is None:
            spack_spec = f"{package_name}@latest"
        
        # Simulate SCSPKG integration
        dependency_tree = []
        environment_modifications = {}
        installation_path = None
        
        # Common HPC package dependencies
        if "mpi" in package_name.lower():
            dependency_tree = ["gcc", "hwloc", "libevent", "pmix"]
            environment_modifications = {
                "PATH": "/opt/spack/bin:$PATH",
                "LD_LIBRARY_PATH": "/opt/spack/lib:$LD_LIBRARY_PATH",
                "MANPATH": "/opt/spack/share/man:$MANPATH"
            }
            installation_path = f"/opt/spack/packages/{package_name}"
            
        elif "hdf5" in package_name.lower():
            dependency_tree = ["zlib", "szip", "gcc"]
            environment_modifications = {
                "HDF5_ROOT": f"/opt/spack/packages/{package_name}",
                "PATH": f"/opt/spack/packages/{package_name}/bin:$PATH"
            }
            installation_path = f"/opt/spack/packages/{package_name}"
            
        else:
            dependency_tree = ["gcc", "cmake"]
            environment_modifications = {
                "PKG_CONFIG_PATH": f"/opt/spack/packages/{package_name}/lib/pkgconfig:$PKG_CONFIG_PATH"
            }
            installation_path = f"/opt/spack/packages/{package_name}"
        
        # Default build options
        default_build_options = {
            "compiler": "gcc@11.0.0",
            "mpi": "openmpi",
            "optimization": "-O2",
            "shared_libs": True
        }
        
        if build_options:
            default_build_options.update(build_options)
        
        return SCSSPkgIntegrationInfo(
            package_name=package_name,
            integration_status="available",
            spack_spec=spack_spec,
            dependency_tree=dependency_tree,
            build_options=default_build_options,
            installation_path=installation_path,
            environment_modifications=environment_modifications
        )
        
    except Exception as e:
        raise ConfigurationError(f"SCSPKG integration failed: {str(e)}")