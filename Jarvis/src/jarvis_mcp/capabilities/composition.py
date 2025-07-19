"""
Phase 2: Composition Tools for Jarvis MCP

This module implements the composition phase tools that enable users to plan and design
complex HPC workflows by intelligently combining packages, understanding dependencies,
and creating deployment strategies.

Following MCP best practices, these tools are designed with a workflow-first approach
rather than direct API mapping, providing intelligent, contextual assistance for
HPC pipeline composition and management.
"""

from typing import Dict, List, Any, Optional
import os
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path

# Import Pydantic models
from jarvis_mcp.capabilities.models import (
    PipelineBasicInfo, PipelinePackageEntry, PipelineCompositionInfo,
    PipelineYAMLScript, PipelineIndexInfo, PackageRelationshipAnalysis,
    PackageOperationResult, PipelineOperationResult, PipelineListResult,
    ExecutionType, PackageRelationship
)

# Try to import Jarvis components - these may not be available in all environments
try:
    from jarvis_cd.basic.jarvis_manager import JarvisManager
    from jarvis_cd.basic.pkg import Pipeline
    JARVIS_AVAILABLE = True
except ImportError:
    JARVIS_AVAILABLE = False

logger = logging.getLogger(__name__)

class CompositionError(Exception):
    """Custom exception for composition-related errors"""
    pass

def _check_jarvis_availability():
    """Check if Jarvis components are available"""
    if not JARVIS_AVAILABLE:
        raise CompositionError(
            "Jarvis components not available. Please ensure jarvis-cd is installed and configured. "
            "You may need to run 'pip install jarvis-cd' or set up the environment properly."
        )

def _get_jarvis_manager():
    """Get Jarvis manager instance with error handling"""
    _check_jarvis_availability()
    try:
        manager = JarvisManager.get_instance()
        if not hasattr(manager, 'config') or manager.config is None:
            raise CompositionError(
                "Jarvis not configured. Please run 'jarvis config init' or use jm_create_config tool first."
            )
        return manager
    except Exception as e:
        raise CompositionError(f"Failed to access Jarvis manager: {str(e)}")

def _get_pipeline_directory():
    """Get the pipeline directory from Jarvis configuration"""
    manager = _get_jarvis_manager()
    config_dir = manager.config.get('CONFIG_DIR', '~/.jarvis')
    pipeline_dir = os.path.join(os.path.expanduser(config_dir), 'pipelines')
    os.makedirs(pipeline_dir, exist_ok=True)
    return pipeline_dir

def _pipeline_exists(pipeline_name: str) -> bool:
    """Check if a pipeline exists"""
    try:
        pipeline_dir = _get_pipeline_directory()
        pipeline_path = os.path.join(pipeline_dir, pipeline_name)
        return os.path.exists(pipeline_path)
    except Exception:
        return False

def _get_focused_pipeline() -> Optional[str]:
    """Get the currently focused pipeline"""
    try:
        manager = _get_jarvis_manager()
        # Try to get focused pipeline from manager state
        if hasattr(manager, 'focused_pipeline'):
            return manager.focused_pipeline
        return None
    except Exception:
        return None

def _set_focused_pipeline(pipeline_name: str):
    """Set the focused pipeline"""
    try:
        manager = _get_jarvis_manager()
        manager.focused_pipeline = pipeline_name
        manager.save()
    except Exception as e:
        logger.warning(f"Could not set focused pipeline: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# BASIC PIPELINE CRUD OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def create_pipeline(
    pipeline_name: str,
    description: str = "",
    switch_focus: bool = True
) -> PipelineOperationResult:
    """
    Create a new empty pipeline.
    
    Equivalent to 'jarvis ppl create [pipeline_name]' command.
    This creates a new pipeline directory and initializes basic metadata.
    
    Args:
        pipeline_name: Name for the new pipeline (must be unique)
        description: Optional description for the pipeline
        switch_focus: Whether to make this the currently focused pipeline
        
    Returns:
        PipelineOperationResult with creation status and pipeline info
        
    Raises:
        CompositionError: If pipeline creation fails
    """
    try:
        _check_jarvis_availability()
        
        # Check if pipeline already exists
        if _pipeline_exists(pipeline_name):
            return PipelineOperationResult(
                operation="create",
                pipeline_name=pipeline_name,
                success=False,
                message=f"Pipeline '{pipeline_name}' already exists",
                warnings=["Use load_pipeline to work with existing pipelines"],
                suggestions=["Try a different pipeline name", "Use list_pipelines to see existing pipelines"]
            )
        
        # Create pipeline using Jarvis API
        pipeline = Pipeline().create(pipeline_name)
        
        # Create pipeline info
        pipeline_info = PipelineBasicInfo(
            pipeline_name=pipeline_name,
            creation_date=datetime.now(),
            last_modified=datetime.now(),
            package_count=0,
            is_focused=switch_focus,
            status="created",
            description=description
        )
        
        # Switch focus if requested
        if switch_focus:
            _set_focused_pipeline(pipeline_name)
        
        return PipelineOperationResult(
            operation="create",
            pipeline_name=pipeline_name,
            success=True,
            message=f"Pipeline '{pipeline_name}' created successfully",
            pipeline_info=pipeline_info,
            suggestions=[
                "Use add_package_to_pipeline to add packages",
                "Use build_pipeline_environment to set up environment",
                "Use export_pipeline_to_yaml to save as script"
            ]
        )
        
    except Exception as e:
        logger.error(f"Failed to create pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Pipeline creation failed: {str(e)}")

async def load_pipeline(
    pipeline_name: str,
    switch_focus: bool = True
) -> PipelineOperationResult:
    """
    Load an existing pipeline for editing.
    
    Args:
        pipeline_name: Name of the pipeline to load
        switch_focus: Whether to make this the currently focused pipeline
        
    Returns:
        PipelineOperationResult with load status and pipeline info
    """
    try:
        _check_jarvis_availability()
        
        # Check if pipeline exists
        if not _pipeline_exists(pipeline_name):
            return PipelineOperationResult(
                operation="load",
                pipeline_name=pipeline_name,
                success=False,
                message=f"Pipeline '{pipeline_name}' not found",
                suggestions=["Use list_pipelines to see available pipelines", "Use create_pipeline to create a new pipeline"]
            )
        
        # Load pipeline using Jarvis API
        pipeline = Pipeline().load(pipeline_name)
        
        # Get pipeline packages
        packages = []
        if hasattr(pipeline, 'pkgs') and pipeline.pkgs:
            for i, pkg in enumerate(pipeline.pkgs):
                packages.append(PipelinePackageEntry(
                    package_name=pkg.pkg_type if hasattr(pkg, 'pkg_type') else 'unknown',
                    package_type=pkg.__class__.__name__ if hasattr(pkg, '__class__') else 'unknown',
                    execution_order=i,
                    configuration=getattr(pkg, 'config', {}),
                    status="configured"
                ))
        
        # Create pipeline info
        pipeline_info = PipelineBasicInfo(
            pipeline_name=pipeline_name,
            creation_date=datetime.now(),  # Would need to get from filesystem
            last_modified=datetime.now(),
            package_count=len(packages),
            is_focused=switch_focus,
            status="loaded"
        )
        
        # Switch focus if requested
        if switch_focus:
            _set_focused_pipeline(pipeline_name)
        
        return PipelineOperationResult(
            operation="load",
            pipeline_name=pipeline_name,
            success=True,
            message=f"Pipeline '{pipeline_name}' loaded successfully",
            pipeline_info=pipeline_info,
            suggestions=[
                "Use get_pipeline_composition to see current packages",
                "Use add_package_to_pipeline to add more packages",
                "Use configure_package_parameters to modify settings"
            ]
        )
        
    except Exception as e:
        logger.error(f"Failed to load pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Pipeline loading failed: {str(e)}")

async def list_pipelines() -> PipelineListResult:
    """
    List all available pipelines.
    
    Equivalent to 'jarvis ppl ls' command.
    
    Returns:
        PipelineListResult with all available pipelines
    """
    try:
        _check_jarvis_availability()
        
        pipeline_dir = _get_pipeline_directory()
        focused_pipeline = _get_focused_pipeline()
        
        pipelines = []
        pipeline_summary = {"created": 0, "configured": 0, "running": 0}
        
        # Scan pipeline directory
        if os.path.exists(pipeline_dir):
            for item in os.listdir(pipeline_dir):
                item_path = os.path.join(pipeline_dir, item)
                if os.path.isdir(item_path):
                    # Try to get pipeline info
                    try:
                        # Check if pipeline is loadable
                        pipeline = Pipeline().load(item)
                        package_count = len(pipeline.pkgs) if hasattr(pipeline, 'pkgs') and pipeline.pkgs else 0
                        
                        # Get filesystem timestamps
                        stat = os.stat(item_path)
                        creation_date = datetime.fromtimestamp(stat.st_ctime)
                        last_modified = datetime.fromtimestamp(stat.st_mtime)
                        
                        pipeline_info = PipelineBasicInfo(
                            pipeline_name=item,
                            creation_date=creation_date,
                            last_modified=last_modified,
                            package_count=package_count,
                            is_focused=(item == focused_pipeline),
                            status="configured" if package_count > 0 else "created"
                        )
                        
                        pipelines.append(pipeline_info)
                        pipeline_summary[pipeline_info.status] += 1
                        
                    except Exception as e:
                        logger.warning(f"Could not load pipeline {item}: {e}")
                        # Add as basic entry
                        pipeline_info = PipelineBasicInfo(
                            pipeline_name=item,
                            creation_date=datetime.fromtimestamp(os.stat(item_path).st_ctime),
                            last_modified=datetime.fromtimestamp(os.stat(item_path).st_mtime),
                            package_count=0,
                            is_focused=(item == focused_pipeline),
                            status="unknown"
                        )
                        pipelines.append(pipeline_info)
        
        # Sort by last modified (most recent first)
        pipelines.sort(key=lambda p: p.last_modified, reverse=True)
        
        # Get recent pipelines (last 5)
        recent_pipelines = [p.pipeline_name for p in pipelines[:5]]
        
        return PipelineListResult(
            pipelines=pipelines,
            total_pipelines=len(pipelines),
            focused_pipeline=focused_pipeline,
            recent_pipelines=recent_pipelines,
            pipeline_summary=pipeline_summary
        )
        
    except Exception as e:
        logger.error(f"Failed to list pipelines: {e}")
        raise CompositionError(f"Failed to list pipelines: {str(e)}")

async def switch_pipeline_focus(pipeline_name: str) -> PipelineOperationResult:
    """
    Switch the currently focused pipeline.
    
    Equivalent to 'jarvis cd [pipeline_name]' command.
    
    Args:
        pipeline_name: Name of the pipeline to focus on
        
    Returns:
        PipelineOperationResult with switch status
    """
    try:
        _check_jarvis_availability()
        
        # Check if pipeline exists
        if not _pipeline_exists(pipeline_name):
            return PipelineOperationResult(
                operation="switch",
                pipeline_name=pipeline_name,
                success=False,
                message=f"Pipeline '{pipeline_name}' not found",
                suggestions=["Use list_pipelines to see available pipelines"]
            )
        
        # Set as focused pipeline
        _set_focused_pipeline(pipeline_name)
        
        return PipelineOperationResult(
            operation="switch",
            pipeline_name=pipeline_name,
            success=True,
            message=f"Switched focus to pipeline '{pipeline_name}'",
            suggestions=[
                "Use get_pipeline_composition to see current packages",
                "Use add_package_to_pipeline to add packages",
                "Use run_pipeline to execute when ready"
            ]
        )
        
    except Exception as e:
        logger.error(f"Failed to switch to pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Pipeline focus switch failed: {str(e)}")

async def delete_pipeline(
    pipeline_name: str,
    confirm: bool = False
) -> PipelineOperationResult:
    """
    Delete a pipeline completely.
    
    Equivalent to 'jarvis ppl rm' command.
    
    Args:
        pipeline_name: Name of the pipeline to delete
        confirm: Confirmation flag for safety
        
    Returns:
        PipelineOperationResult with deletion status
    """
    try:
        _check_jarvis_availability()
        
        if not confirm:
            return PipelineOperationResult(
                operation="delete",
                pipeline_name=pipeline_name,
                success=False,
                message="Pipeline deletion requires confirmation",
                warnings=["This operation cannot be undone"],
                suggestions=["Set confirm=True to proceed with deletion"]
            )
        
        # Check if pipeline exists
        if not _pipeline_exists(pipeline_name):
            return PipelineOperationResult(
                operation="delete",
                pipeline_name=pipeline_name,
                success=False,
                message=f"Pipeline '{pipeline_name}' not found",
                suggestions=["Use list_pipelines to see available pipelines"]
            )
        
        # Remove pipeline directory
        pipeline_dir = _get_pipeline_directory()
        pipeline_path = os.path.join(pipeline_dir, pipeline_name)
        
        import shutil
        shutil.rmtree(pipeline_path)
        
        # Clear focus if this was the focused pipeline
        if _get_focused_pipeline() == pipeline_name:
            _set_focused_pipeline("")
        
        return PipelineOperationResult(
            operation="delete",
            pipeline_name=pipeline_name,
            success=True,
            message=f"Pipeline '{pipeline_name}' deleted successfully",
            suggestions=["Use list_pipelines to see remaining pipelines"]
        )
        
    except Exception as e:
        logger.error(f"Failed to delete pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Pipeline deletion failed: {str(e)}")

async def update_pipeline(
    pipeline_name: Optional[str] = None
) -> PipelineOperationResult:
    """
    Update pipeline configuration.
    
    Equivalent to 'jarvis ppl update' command.
    
    Args:
        pipeline_name: Name of pipeline to update (uses focused if None)
        
    Returns:
        PipelineOperationResult with update status
    """
    try:
        _check_jarvis_availability()
        
        # Use focused pipeline if none specified
        if pipeline_name is None:
            pipeline_name = _get_focused_pipeline()
            if not pipeline_name:
                return PipelineOperationResult(
                    operation="update",
                    pipeline_name="",
                    success=False,
                    message="No pipeline specified and no focused pipeline",
                    suggestions=["Specify pipeline_name or use switch_pipeline_focus first"]
                )
        
        # Check if pipeline exists
        if not _pipeline_exists(pipeline_name):
            return PipelineOperationResult(
                operation="update",
                pipeline_name=pipeline_name,
                success=False,
                message=f"Pipeline '{pipeline_name}' not found"
            )
        
        # Load and update pipeline
        pipeline = Pipeline().load(pipeline_name)
        pipeline.update()  # This rebuilds configurations based on current environment
        pipeline.save()
        
        return PipelineOperationResult(
            operation="update",
            pipeline_name=pipeline_name,
            success=True,
            message=f"Pipeline '{pipeline_name}' updated successfully",
            suggestions=["Pipeline configurations rebuilt based on current environment"]
        )
        
    except Exception as e:
        logger.error(f"Failed to update pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Pipeline update failed: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PACKAGE MANAGEMENT OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def add_package_to_pipeline(
    package_name: str,
    pipeline_name: Optional[str] = None,
    configuration: Optional[Dict[str, Any]] = None
) -> PackageOperationResult:
    """
    Add a package to the specified pipeline.
    
    Equivalent to 'jarvis ppl append [package_name]' command.
    
    Args:
        package_name: Name of the package to add
        pipeline_name: Target pipeline (uses focused if None)
        configuration: Optional package configuration parameters
        
    Returns:
        PackageOperationResult with operation status
    """
    try:
        _check_jarvis_availability()
        
        # Use focused pipeline if none specified
        if pipeline_name is None:
            pipeline_name = _get_focused_pipeline()
            if not pipeline_name:
                return PackageOperationResult(
                    operation="add",
                    package_name=package_name,
                    pipeline_name="",
                    success=False,
                    message="No pipeline specified and no focused pipeline",
                    updated_package_list=[],
                    new_execution_order=[]
                )
        
        # Load pipeline
        pipeline = Pipeline().load(pipeline_name)
        
        # Add package with configuration
        if configuration:
            pipeline.append(package_name, do_configure=True, **configuration)
        else:
            pipeline.append(package_name)
        
        pipeline.save()
        
        # Get updated package list
        packages = []
        package_names = []
        if hasattr(pipeline, 'pkgs') and pipeline.pkgs:
            for i, pkg in enumerate(pipeline.pkgs):
                pkg_name = getattr(pkg, 'pkg_type', package_name)
                package_names.append(pkg_name)
                packages.append(PipelinePackageEntry(
                    package_name=pkg_name,
                    package_type=pkg.__class__.__name__ if hasattr(pkg, '__class__') else 'unknown',
                    execution_order=i,
                    configuration=getattr(pkg, 'config', {}),
                    status="configured"
                ))
        
        return PackageOperationResult(
            operation="add",
            package_name=package_name,
            pipeline_name=pipeline_name,
            success=True,
            message=f"Package '{package_name}' added to pipeline '{pipeline_name}'",
            updated_package_list=package_names,
            new_execution_order=packages
        )
        
    except Exception as e:
        logger.error(f"Failed to add package {package_name} to pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Failed to add package: {str(e)}")

async def remove_package_from_pipeline(
    package_name: str,
    pipeline_name: Optional[str] = None
) -> PackageOperationResult:
    """
    Remove a package from the specified pipeline.
    
    Args:
        package_name: Name of the package to remove
        pipeline_name: Target pipeline (uses focused if None)
        
    Returns:
        PackageOperationResult with operation status
    """
    try:
        _check_jarvis_availability()
        
        # Use focused pipeline if none specified
        if pipeline_name is None:
            pipeline_name = _get_focused_pipeline()
            if not pipeline_name:
                return PackageOperationResult(
                    operation="remove",
                    package_name=package_name,
                    pipeline_name="",
                    success=False,
                    message="No pipeline specified and no focused pipeline",
                    updated_package_list=[],
                    new_execution_order=[]
                )
        
        # Load pipeline
        pipeline = Pipeline().load(pipeline_name)
        
        # Find and remove package
        if hasattr(pipeline, 'pkgs') and pipeline.pkgs:
            original_count = len(pipeline.pkgs)
            pipeline.pkgs = [pkg for pkg in pipeline.pkgs 
                           if getattr(pkg, 'pkg_type', '') != package_name]
            
            if len(pipeline.pkgs) == original_count:
                return PackageOperationResult(
                    operation="remove",
                    package_name=package_name,
                    pipeline_name=pipeline_name,
                    success=False,
                    message=f"Package '{package_name}' not found in pipeline '{pipeline_name}'",
                    updated_package_list=[],
                    new_execution_order=[]
                )
        
        pipeline.save()
        
        # Get updated package list
        packages = []
        package_names = []
        if hasattr(pipeline, 'pkgs') and pipeline.pkgs:
            for i, pkg in enumerate(pipeline.pkgs):
                pkg_name = getattr(pkg, 'pkg_type', f'package_{i}')
                package_names.append(pkg_name)
                packages.append(PipelinePackageEntry(
                    package_name=pkg_name,
                    package_type=pkg.__class__.__name__ if hasattr(pkg, '__class__') else 'unknown',
                    execution_order=i,
                    configuration=getattr(pkg, 'config', {}),
                    status="configured"
                ))
        
        return PackageOperationResult(
            operation="remove",
            package_name=package_name,
            pipeline_name=pipeline_name,
            success=True,
            message=f"Package '{package_name}' removed from pipeline '{pipeline_name}'",
            updated_package_list=package_names,
            new_execution_order=packages
        )
        
    except Exception as e:
        logger.error(f"Failed to remove package {package_name} from pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Failed to remove package: {str(e)}")

async def get_pipeline_composition(
    pipeline_name: Optional[str] = None
) -> PipelineCompositionInfo:
    """
    Get detailed information about pipeline composition.
    
    Args:
        pipeline_name: Target pipeline (uses focused if None)
        
    Returns:
        PipelineCompositionInfo with complete pipeline details
    """
    try:
        _check_jarvis_availability()
        
        # Use focused pipeline if none specified
        if pipeline_name is None:
            pipeline_name = _get_focused_pipeline()
            if not pipeline_name:
                raise CompositionError("No pipeline specified and no focused pipeline")
        
        # Load pipeline
        pipeline = Pipeline().load(pipeline_name)
        
        # Extract package information
        packages = []
        dependencies = []
        
        if hasattr(pipeline, 'pkgs') and pipeline.pkgs:
            for i, pkg in enumerate(pipeline.pkgs):
                pkg_name = getattr(pkg, 'pkg_type', f'package_{i}')
                pkg_deps = getattr(pkg, 'dependencies', [])
                
                packages.append(PipelinePackageEntry(
                    package_name=pkg_name,
                    package_type=pkg.__class__.__name__ if hasattr(pkg, '__class__') else 'unknown',
                    execution_order=i,
                    configuration=getattr(pkg, 'config', {}),
                    status="configured",
                    dependencies=pkg_deps
                ))
                
                dependencies.extend(pkg_deps)
        
        return PipelineCompositionInfo(
            pipeline_name=pipeline_name,
            packages=packages,
            environment_config=getattr(pipeline, 'env_name', None),
            execution_dependencies=list(set(dependencies)),
            validation_status="configured",
            total_packages=len(packages)
        )
        
    except Exception as e:
        logger.error(f"Failed to get pipeline composition for {pipeline_name}: {e}")
        raise CompositionError(f"Failed to get pipeline composition: {str(e)}")

async def reorder_pipeline_packages(
    new_order: List[str],
    pipeline_name: Optional[str] = None
) -> PackageOperationResult:
    """
    Reorder packages in the pipeline execution sequence.
    
    Args:
        new_order: List of package names in desired execution order
        pipeline_name: Target pipeline (uses focused if None)
        
    Returns:
        PackageOperationResult with operation status
    """
    try:
        _check_jarvis_availability()
        
        # Use focused pipeline if none specified
        if pipeline_name is None:
            pipeline_name = _get_focused_pipeline()
            if not pipeline_name:
                return PackageOperationResult(
                    operation="reorder",
                    package_name="",
                    pipeline_name="",
                    success=False,
                    message="No pipeline specified and no focused pipeline",
                    updated_package_list=[],
                    new_execution_order=[]
                )
        
        # Load pipeline
        pipeline = Pipeline().load(pipeline_name)
        
        if not hasattr(pipeline, 'pkgs') or not pipeline.pkgs:
            return PackageOperationResult(
                operation="reorder",
                package_name="",
                pipeline_name=pipeline_name,
                success=False,
                message="Pipeline has no packages to reorder",
                updated_package_list=[],
                new_execution_order=[]
            )
        
        # Create package lookup
        pkg_dict = {}
        for pkg in pipeline.pkgs:
            pkg_name = getattr(pkg, 'pkg_type', '')
            if pkg_name:
                pkg_dict[pkg_name] = pkg
        
        # Validate new order
        missing_packages = [name for name in new_order if name not in pkg_dict]
        if missing_packages:
            return PackageOperationResult(
                operation="reorder",
                package_name="",
                pipeline_name=pipeline_name,
                success=False,
                message=f"Packages not found in pipeline: {missing_packages}",
                updated_package_list=[],
                new_execution_order=[]
            )
        
        # Reorder packages
        pipeline.pkgs = [pkg_dict[name] for name in new_order if name in pkg_dict]
        pipeline.save()
        
        # Get updated package list
        packages = []
        for i, pkg in enumerate(pipeline.pkgs):
            pkg_name = getattr(pkg, 'pkg_type', f'package_{i}')
            packages.append(PipelinePackageEntry(
                package_name=pkg_name,
                package_type=pkg.__class__.__name__ if hasattr(pkg, '__class__') else 'unknown',
                execution_order=i,
                configuration=getattr(pkg, 'config', {}),
                status="configured"
            ))
        
        return PackageOperationResult(
            operation="reorder",
            package_name="",
            pipeline_name=pipeline_name,
            success=True,
            message=f"Pipeline '{pipeline_name}' packages reordered successfully",
            updated_package_list=new_order,
            new_execution_order=packages
        )
        
    except Exception as e:
        logger.error(f"Failed to reorder packages in pipeline {pipeline_name}: {e}")
        raise CompositionError(f"Failed to reorder packages: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# YAML & SCRIPTING OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def import_pipeline_from_yaml(
    yaml_path: str,
    pipeline_name: Optional[str] = None
) -> PipelineOperationResult:
    """
    Import pipeline from YAML script.
    
    Equivalent to 'jarvis ppl load yaml [yaml_path]' command.
    
    Args:
        yaml_path: Path to YAML pipeline script
        pipeline_name: Optional custom pipeline name (uses YAML name if None)
        
    Returns:
        PipelineOperationResult with import status
    """
    try:
        _check_jarvis_availability()
        
        # Check if YAML file exists
        if not os.path.exists(yaml_path):
            return PipelineOperationResult(
                operation="import_yaml",
                pipeline_name=pipeline_name or "",
                success=False,
                message=f"YAML file not found: {yaml_path}",
                suggestions=["Check the file path and ensure the YAML file exists"]
            )
        
        # Parse YAML file
        with open(yaml_path, 'r') as f:
            yaml_content = yaml.safe_load(f)
        
        # Extract pipeline name
        if pipeline_name is None:
            pipeline_name = yaml_content.get('name', 'imported_pipeline')
        
        # Check if pipeline already exists
        if _pipeline_exists(pipeline_name):
            return PipelineOperationResult(
                operation="import_yaml",
                pipeline_name=pipeline_name,
                success=False,
                message=f"Pipeline '{pipeline_name}' already exists",
                warnings=["Use a different pipeline name or delete existing pipeline"],
                suggestions=["Set a custom pipeline_name parameter"]
            )
        
        # Create new pipeline
        pipeline = Pipeline().create(pipeline_name)
        
        # Set environment if specified
        if 'env' in yaml_content:
            try:
                pipeline.env_copy(yaml_content['env'])
            except Exception as e:
                logger.warning(f"Could not copy environment {yaml_content['env']}: {e}")
        
        # Add packages from YAML
        packages_added = []
        if 'pkgs' in yaml_content:
            for pkg_config in yaml_content['pkgs']:
                pkg_type = pkg_config.get('pkg_type')
                if pkg_type:
                    # Extract configuration parameters
                    config_params = {k: v for k, v in pkg_config.items() 
                                   if k not in ['pkg_type', 'pkg_name']}
                    
                    # Add package to pipeline
                    if config_params:
                        pipeline.append(pkg_type, do_configure=True, **config_params)
                    else:
                        pipeline.append(pkg_type)
                    
                    packages_added.append(pkg_type)
        
        pipeline.save()
        
        # Create pipeline info
        pipeline_info = PipelineBasicInfo(
            pipeline_name=pipeline_name,
            creation_date=datetime.now(),
            last_modified=datetime.now(),
            package_count=len(packages_added),
            is_focused=True,
            status="imported"
        )
        
        # Set as focused pipeline
        _set_focused_pipeline(pipeline_name)
        
        return PipelineOperationResult(
            operation="import_yaml",
            pipeline_name=pipeline_name,
            success=True,
            message=f"Pipeline '{pipeline_name}' imported from YAML with {len(packages_added)} packages",
            pipeline_info=pipeline_info,
            suggestions=[
                "Use get_pipeline_composition to review imported packages",
                "Use update_pipeline to refresh configurations",
                "Use run_pipeline when ready to execute"
            ]
        )
        
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error: {e}")
        raise CompositionError(f"Invalid YAML file: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to import pipeline from YAML {yaml_path}: {e}")
        raise CompositionError(f"YAML import failed: {str(e)}")

async def export_pipeline_to_yaml(
    pipeline_name: Optional[str] = None,
    output_path: Optional[str] = None
) -> PipelineYAMLScript:
    """
    Export pipeline to YAML format.
    
    Args:
        pipeline_name: Target pipeline (uses focused if None)
        output_path: Optional path to save YAML file
        
    Returns:
        PipelineYAMLScript with YAML content
    """
    try:
        _check_jarvis_availability()
        
        # Use focused pipeline if none specified
        if pipeline_name is None:
            pipeline_name = _get_focused_pipeline()
            if not pipeline_name:
                raise CompositionError("No pipeline specified and no focused pipeline")
        
        # Load pipeline
        pipeline = Pipeline().load(pipeline_name)
        
        # Build YAML structure
        yaml_structure = {
            'name': pipeline_name,
            'pkgs': []
        }
        
        # Add environment if available
        if hasattr(pipeline, 'env_name') and pipeline.env_name:
            yaml_structure['env'] = pipeline.env_name
        
        # Add packages
        if hasattr(pipeline, 'pkgs') and pipeline.pkgs:
            for pkg in pipeline.pkgs:
                pkg_config = {
                    'pkg_type': getattr(pkg, 'pkg_type', 'unknown'),
                    'pkg_name': getattr(pkg, 'pkg_name', getattr(pkg, 'pkg_type', 'unknown'))
                }
                
                # Add package configuration
                if hasattr(pkg, 'config') and pkg.config:
                    pkg_config.update(pkg.config)
                
                yaml_structure['pkgs'].append(pkg_config)
        
        # Convert to YAML string
        yaml_content = yaml.dump(yaml_structure, default_flow_style=False, sort_keys=False)
        
        # Save to file if path specified
        if output_path:
            with open(output_path, 'w') as f:
                f.write(yaml_content)
        
        return PipelineYAMLScript(
            name=pipeline_name,
            environment=yaml_structure.get('env'),
            packages=yaml_structure['pkgs'],
            execution_type=ExecutionType.LOCAL,
            yaml_content=yaml_content
        )
        
    except Exception as e:
        logger.error(f"Failed to export pipeline {pipeline_name} to YAML: {e}")
        raise CompositionError(f"YAML export failed: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED FEATURES
# ═══════════════════════════════════════════════════════════════════════════════

async def browse_pipeline_indexes() -> PipelineIndexInfo:
    """
    Browse available pipeline examples from repositories.
    
    Equivalent to 'jarvis ppl index ls' command.
    
    Returns:
        PipelineIndexInfo with available pipeline scripts
    """
    try:
        _check_jarvis_availability()
        manager = _get_jarvis_manager()
        
        all_scripts = []
        script_descriptions = {}
        categories = {}
        
        # Get repositories from manager
        if hasattr(manager, 'repos') and manager.repos:
            for repo_name, repo_path in manager.repos.items():
                # Look for pipelines directory in repository
                pipelines_dir = os.path.join(repo_path, 'pipelines')
                if os.path.exists(pipelines_dir):
                    # Scan for YAML files
                    for root, dirs, files in os.walk(pipelines_dir):
                        for file in files:
                            if file.endswith('.yaml') or file.endswith('.yml'):
                                script_path = os.path.join(root, file)
                                relative_path = os.path.relpath(script_path, pipelines_dir)
                                
                                all_scripts.append(relative_path)
                                
                                # Try to extract description from YAML
                                try:
                                    with open(script_path, 'r') as f:
                                        script_data = yaml.safe_load(f)
                                        script_descriptions[relative_path] = script_data.get('description', 'No description available')
                                        
                                        # Categorize by directory structure
                                        category = os.path.dirname(relative_path) or 'root'
                                        if category not in categories:
                                            categories[category] = []
                                        categories[category].append(relative_path)
                                        
                                except Exception as e:
                                    logger.warning(f"Could not parse pipeline script {script_path}: {e}")
                                    script_descriptions[relative_path] = "Could not parse YAML"
        
        return PipelineIndexInfo(
            repository_name="all_repositories",
            available_scripts=all_scripts,
            script_descriptions=script_descriptions,
            categories=categories,
            total_scripts=len(all_scripts)
        )
        
    except Exception as e:
        logger.error(f"Failed to browse pipeline indexes: {e}")
        raise CompositionError(f"Failed to browse pipeline indexes: {str(e)}")

async def analyze_package_relationships(
    package_names: List[str]
) -> PackageRelationshipAnalysis:
    """
    Analyze relationships and dependencies between packages.
    
    Args:
        package_names: List of package names to analyze
        
    Returns:
        PackageRelationshipAnalysis with relationship information
    """
    try:
        _check_jarvis_availability()
        
        # This is a simplified implementation - in a full implementation,
        # this would analyze actual package definitions, dependencies,
        # and performance characteristics
        
        relationships = []
        compatibility_matrix = {}
        performance_synergies = []
        resource_conflicts = []
        optimization_suggestions = []
        
        # Initialize compatibility matrix
        for pkg_a in package_names:
            compatibility_matrix[pkg_a] = {}
            for pkg_b in package_names:
                if pkg_a != pkg_b:
                    # Simplified compatibility check
                    compatibility_matrix[pkg_a][pkg_b] = "compatible"  # Default assumption
        
        # Common package relationship patterns
        known_synergies = {
            ('orangefs', 'ior'): "OrangeFS storage system pairs well with IOR benchmark for filesystem testing",
            ('hermes', 'ior'): "Hermes I/O acceleration complements IOR for performance evaluation",
            ('incompact3d', 'paraview'): "Incompact3D simulation generates data compatible with ParaView visualization"
        }
        
        # Check for known relationships
        for i, pkg_a in enumerate(package_names):
            for j, pkg_b in enumerate(package_names[i+1:], i+1):
                # Check both directions for known synergies
                synergy_key = (pkg_a, pkg_b)
                reverse_key = (pkg_b, pkg_a)
                
                if synergy_key in known_synergies:
                    relationships.append(PackageRelationship(
                        package_a=pkg_a,
                        package_b=pkg_b,
                        relationship_type="complement",
                        strength=0.8,
                        description=known_synergies[synergy_key]
                    ))
                    performance_synergies.append({
                        "packages": [pkg_a, pkg_b],
                        "synergy": known_synergies[synergy_key],
                        "expected_benefit": "Improved overall workflow performance"
                    })
                elif reverse_key in known_synergies:
                    relationships.append(PackageRelationship(
                        package_a=pkg_b,
                        package_b=pkg_a,
                        relationship_type="complement",
                        strength=0.8,
                        description=known_synergies[reverse_key]
                    ))
                    performance_synergies.append({
                        "packages": [pkg_b, pkg_a],
                        "synergy": known_synergies[reverse_key],
                        "expected_benefit": "Improved overall workflow performance"
                    })
        
        # Generate optimization suggestions
        if len(package_names) > 1:
            optimization_suggestions.extend([
                "Consider execution order based on package dependencies",
                "Review resource requirements to avoid conflicts",
                "Optimize package configurations for your specific use case",
                "Use monitoring tools to validate package interactions"
            ])
        
        if any(pkg in ['orangefs', 'lustre', 'beegfs'] for pkg in package_names):
            optimization_suggestions.append("Storage system detected - ensure proper filesystem mounting")
        
        if any(pkg in ['ior', 'mdtest', 'filebench'] for pkg in package_names):
            optimization_suggestions.append("Benchmark detected - configure appropriate test parameters")
        
        return PackageRelationshipAnalysis(
            analyzed_packages=package_names,
            relationships=relationships,
            compatibility_matrix=compatibility_matrix,
            performance_synergies=performance_synergies,
            resource_conflicts=resource_conflicts,
            optimization_suggestions=optimization_suggestions
        )
        
    except Exception as e:
        logger.error(f"Failed to analyze package relationships: {e}")
        raise CompositionError(f"Package relationship analysis failed: {str(e)}")