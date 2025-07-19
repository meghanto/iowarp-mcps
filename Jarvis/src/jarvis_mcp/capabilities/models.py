from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# Phase 1: Discoverability Models

class PackageType(str, Enum):
    SERVICE = "service"
    APPLICATION = "application"
    INTERCEPTOR = "interceptor"
    ALL = "all"

class PackageInfo(BaseModel):
    name: str = Field(..., description="Package name")
    type: str = Field(..., description="Package type (service, application, interceptor)")
    repository: str = Field(..., description="Repository name where package is located")
    description: str = Field(..., description="Package description")
    version: Optional[str] = Field(None, description="Package version if available")
    dependencies: List[str] = Field(default_factory=list, description="List of package dependencies")
    popularity_score: float = Field(default=0.0, description="Usage popularity score")
    documentation_quality: str = Field(default="unknown", description="Documentation quality assessment")
    capabilities: List[str] = Field(default_factory=list, description="Package capabilities")
    configuration_params: Dict[str, Any] = Field(default_factory=dict, description="Configuration parameters")

class PackageRelationship(BaseModel):
    package_a: str = Field(..., description="First package in relationship")
    package_b: str = Field(..., description="Second package in relationship")
    relationship_type: str = Field(..., description="Type of relationship (complement, conflict, dependency)")
    strength: float = Field(..., description="Relationship strength (0.0 to 1.0)")
    description: str = Field(..., description="Human-readable description of relationship")

class PackageCatalog(BaseModel):
    packages: List[PackageInfo] = Field(..., description="List of available packages")
    total_count: int = Field(..., description="Total number of packages")
    repositories: List[str] = Field(..., description="List of repository names")
    common_combinations: Dict[str, List[str]] = Field(default_factory=dict, description="Common package combinations")
    quick_start_recommendations: List[str] = Field(default_factory=list, description="Quick start recommendations")
    categorized_packages: Dict[str, List[str]] = Field(default_factory=dict, description="Packages organized by category")

class RepositoryInfo(BaseModel):
    name: str = Field(..., description="Repository name")
    path: str = Field(..., description="Repository filesystem path")
    priority: int = Field(..., description="Search priority (1 = highest)")
    status: str = Field(..., description="Repository status (active, inactive, error)")
    package_count: int = Field(..., description="Number of packages in repository")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    health_status: str = Field(..., description="Health status indicator")
    repository_type: str = Field(..., description="Repository type (builtin, custom, development)")
    featured_packages: List[str] = Field(default_factory=list, description="Notable packages in repository")

class RepositoryStatus(BaseModel):
    repositories: List[RepositoryInfo] = Field(..., description="List of repository information")
    total_repositories: int = Field(..., description="Total number of repositories")
    priority_order: List[str] = Field(..., description="Repository names in priority order")
    health_summary: Dict[str, int] = Field(default_factory=dict, description="Health status counts")
    total_packages: int = Field(..., description="Total packages across all repositories")

class RepositoryOperationResult(BaseModel):
    operation: str = Field(..., description="Operation performed (add, delete, promote)")
    repository_name: str = Field(..., description="Repository name")
    status: str = Field(..., description="Operation status (success, warning, error)")
    message: str = Field(..., description="Human-readable result message")
    updated_priority_order: List[str] = Field(default_factory=list, description="New repository priority order")
    impact_analysis: Dict[str, Any] = Field(default_factory=dict, description="Impact analysis of the operation")
    rollback_instructions: Optional[str] = Field(None, description="Instructions to undo the operation")

class ResourceInfo(BaseModel):
    resource_type: str = Field(..., description="Type of resource (cpu, memory, storage, network)")
    name: str = Field(..., description="Resource name or identifier")
    capacity: str = Field(..., description="Resource capacity")
    utilization: float = Field(..., description="Current utilization percentage")
    status: str = Field(..., description="Resource status")
    performance_characteristics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")

class ClusterResourceStatus(BaseModel):
    hardware_resources: List[ResourceInfo] = Field(default_factory=list, description="Hardware resource information")
    network_resources: List[ResourceInfo] = Field(default_factory=list, description="Network resource information")
    storage_resources: List[ResourceInfo] = Field(default_factory=list, description="Storage resource information")
    deployment_constraints: Dict[str, Any] = Field(default_factory=dict, description="Deployment constraints")
    optimization_recommendations: List[str] = Field(default_factory=list, description="Resource optimization suggestions")
    resource_graph_status: str = Field(..., description="Resource graph build status")

class PackageInformation(BaseModel):
    package_name: str = Field(..., description="Package name")
    package_type: str = Field(..., description="Package type")
    repository: str = Field(..., description="Source repository")
    description: str = Field(..., description="Package description")
    readme_content: Optional[str] = Field(None, description="README content")
    configuration_parameters: Dict[str, Any] = Field(default_factory=dict, description="Configuration parameters with details")
    capabilities: List[str] = Field(default_factory=list, description="Package capabilities")
    output_specifications: Dict[str, Any] = Field(default_factory=dict, description="Output specifications")
    installation_requirements: List[str] = Field(default_factory=list, description="Installation requirements")
    usage_examples: List[str] = Field(default_factory=list, description="Usage examples")
    dependencies: List[str] = Field(default_factory=list, description="Package dependencies")
    performance_notes: List[str] = Field(default_factory=list, description="Performance characteristics")
    related_packages: List[str] = Field(default_factory=list, description="Related or complementary packages")


# Phase 2: Composition Models

class ExecutionType(str, Enum):
    LOCAL = "local"
    SSH = "ssh"
    PSSH = "pssh"
    MPI = "mpi"

class PipelineBasicInfo(BaseModel):
    pipeline_name: str = Field(..., description="Pipeline identifier")
    creation_date: datetime = Field(..., description="Creation timestamp")
    last_modified: datetime = Field(..., description="Last modification time")
    package_count: int = Field(..., description="Number of packages")
    is_focused: bool = Field(False, description="Currently focused pipeline")
    environment_name: Optional[str] = Field(None, description="Associated environment")
    status: str = Field("configured", description="Pipeline status")
    description: str = Field("", description="Pipeline description")

class PipelinePackageEntry(BaseModel):
    package_name: str = Field(..., description="Package name")
    package_type: str = Field(..., description="Package type (service, application, interceptor)")
    execution_order: int = Field(..., description="Execution order in pipeline")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Package configuration")
    status: str = Field("added", description="Package status in pipeline")
    dependencies: List[str] = Field(default_factory=list, description="Package dependencies")

class PipelineCompositionInfo(BaseModel):
    pipeline_name: str = Field(..., description="Pipeline name")
    packages: List[PipelinePackageEntry] = Field(..., description="Packages in execution order")
    environment_config: Optional[str] = Field(None, description="Environment configuration")
    execution_dependencies: List[str] = Field(default_factory=list, description="Package dependencies")
    validation_status: str = Field("unknown", description="Validation status")
    estimated_resources: Dict[str, Any] = Field(default_factory=dict, description="Resource requirements")
    total_packages: int = Field(..., description="Total number of packages")

class PipelineYAMLScript(BaseModel):
    name: str = Field(..., description="Pipeline name")
    environment: Optional[str] = Field(None, description="Named environment to use")
    packages: List[Dict[str, Any]] = Field(..., description="Package configurations")
    execution_type: ExecutionType = Field(default=ExecutionType.LOCAL, description="Execution method")
    hostfile: Optional[str] = Field(None, description="Hostfile for distributed execution")
    yaml_content: str = Field(..., description="Complete YAML script content")

class PipelineIndexInfo(BaseModel):
    repository_name: str = Field(..., description="Source repository")
    available_scripts: List[str] = Field(..., description="Available pipeline scripts")
    script_descriptions: Dict[str, str] = Field(default_factory=dict, description="Script descriptions")
    categories: Dict[str, List[str]] = Field(default_factory=dict, description="Scripts by category")
    total_scripts: int = Field(..., description="Total number of pipeline scripts")

class PackageRelationshipAnalysis(BaseModel):
    analyzed_packages: List[str] = Field(..., description="Packages included in analysis")
    relationships: List[PackageRelationship] = Field(..., description="Identified relationships")
    compatibility_matrix: Dict[str, Dict[str, str]] = Field(default_factory=dict, description="Compatibility matrix")
    performance_synergies: List[Dict[str, Any]] = Field(default_factory=list, description="Performance enhancement opportunities")
    resource_conflicts: List[Dict[str, Any]] = Field(default_factory=list, description="Identified resource conflicts")
    optimization_suggestions: List[str] = Field(default_factory=list, description="Optimization recommendations")

class PackageOperationResult(BaseModel):
    operation: str = Field(..., description="Operation performed (add, remove, reorder)")
    package_name: str = Field(..., description="Target package name")
    pipeline_name: str = Field(..., description="Target pipeline name")
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Result message")
    updated_package_list: List[str] = Field(..., description="Updated package execution order")
    warnings: List[str] = Field(default_factory=list, description="Operation warnings")
    new_execution_order: List[PipelinePackageEntry] = Field(..., description="Updated pipeline composition")

class PipelineOperationResult(BaseModel):
    operation: str = Field(..., description="Operation performed (create, load, delete, switch)")
    pipeline_name: str = Field(..., description="Target pipeline name")
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Result message")
    pipeline_info: Optional[PipelineBasicInfo] = Field(None, description="Pipeline information after operation")
    warnings: List[str] = Field(default_factory=list, description="Operation warnings")
    suggestions: List[str] = Field(default_factory=list, description="Next step suggestions")

class PipelineListResult(BaseModel):
    pipelines: List[PipelineBasicInfo] = Field(..., description="List of available pipelines")
    total_pipelines: int = Field(..., description="Total number of pipelines")
    focused_pipeline: Optional[str] = Field(None, description="Currently focused pipeline name")
    recent_pipelines: List[str] = Field(default_factory=list, description="Recently accessed pipelines")
    pipeline_summary: Dict[str, int] = Field(default_factory=dict, description="Pipeline statistics by status")


# Phase 3: Configuration Models

class PipelineEnvironmentInfo(BaseModel):
    environment_name: str = Field(..., description="Environment identifier")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    loaded_modules: List[str] = Field(default_factory=list, description="Loaded modules")
    build_timestamp: datetime = Field(..., description="Environment build time")
    is_machine_specific: bool = Field(True, description="Machine-specific environment")
    pipeline_name: str = Field(..., description="Associated pipeline name")
    build_status: str = Field("unknown", description="Environment build status")
    optimization_flags: List[str] = Field(default_factory=list, description="Compiler optimization flags")
    dependency_conflicts: List[str] = Field(default_factory=list, description="Identified dependency conflicts")

class PackageConfigurationInfo(BaseModel):
    package_name: str = Field(..., description="Package name")
    current_config: Dict[str, Any] = Field(default_factory=dict, description="Current configuration")
    available_parameters: List[Dict[str, Any]] = Field(default_factory=list, description="Available parameters")
    validation_results: List[str] = Field(default_factory=list, description="Configuration validation")
    optimization_suggestions: List[str] = Field(default_factory=list, description="Optimization recommendations")
    configuration_menu: List[Dict[str, Any]] = Field(default_factory=list, description="Package configuration menu")
    parameter_constraints: Dict[str, Any] = Field(default_factory=dict, description="Parameter validation constraints")
    performance_impact: Dict[str, str] = Field(default_factory=dict, description="Performance impact of parameters")

class ExecutionMethodConfig(BaseModel):
    execution_type: ExecutionType = Field(..., description="Execution method")
    hostfile_path: Optional[str] = Field(None, description="Hostfile for distributed execution")
    node_count: Optional[int] = Field(None, description="Number of nodes to use")
    processes_per_node: Optional[int] = Field(None, description="Processes per node")
    mpi_settings: Dict[str, Any] = Field(default_factory=dict, description="MPI-specific settings")
    ssh_settings: Dict[str, Any] = Field(default_factory=dict, description="SSH-specific settings")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Execution environment")
    validation_status: str = Field("unchecked", description="Configuration validation status")
    estimated_resources: Dict[str, Any] = Field(default_factory=dict, description="Estimated resource usage")

class InterceptorConfiguration(BaseModel):
    interceptor_name: str = Field(..., description="Interceptor package name")
    ld_preload_order: int = Field(..., description="Order in LD_PRELOAD chain")
    configuration_params: Dict[str, Any] = Field(default_factory=dict, description="Interceptor-specific configuration")
    target_packages: List[str] = Field(default_factory=list, description="Packages this interceptor targets")
    compatibility_status: str = Field("unknown", description="Compatibility with other interceptors")
    output_files: List[str] = Field(default_factory=list, description="Expected output files")

class ResourceAllocationConfig(BaseModel):
    pipeline_name: str = Field(..., description="Pipeline for resource allocation")
    node_assignments: Dict[str, List[str]] = Field(default_factory=dict, description="Package to node mapping")
    resource_constraints: Dict[str, Any] = Field(default_factory=dict, description="Resource usage constraints")
    optimization_strategy: str = Field("balanced", description="Resource allocation strategy")
    load_balancing: Dict[str, float] = Field(default_factory=dict, description="Load distribution across nodes")
    estimated_performance: Dict[str, Any] = Field(default_factory=dict, description="Performance estimates")
    conflicts: List[str] = Field(default_factory=list, description="Resource allocation conflicts")

class SCSSPkgIntegrationInfo(BaseModel):
    package_name: str = Field(..., description="SCSPKG package name")
    integration_status: str = Field(..., description="Integration status with Jarvis")
    spack_spec: str = Field(..., description="Spack package specification")
    dependency_tree: List[str] = Field(default_factory=list, description="SCSPKG dependencies")
    build_options: Dict[str, Any] = Field(default_factory=dict, description="Build configuration options")
    installation_path: Optional[str] = Field(None, description="Package installation path")
    environment_modifications: Dict[str, str] = Field(default_factory=dict, description="Required environment changes")

class PipelineValidationResult(BaseModel):
    pipeline_name: str = Field(..., description="Validated pipeline name")
    validation_status: str = Field(..., description="Overall validation status")
    package_validations: List[Dict[str, Any]] = Field(default_factory=list, description="Per-package validation results")
    environment_validation: Dict[str, Any] = Field(default_factory=dict, description="Environment validation results")
    resource_validation: Dict[str, Any] = Field(default_factory=dict, description="Resource requirement validation")
    configuration_errors: List[str] = Field(default_factory=list, description="Configuration errors found")
    warnings: List[str] = Field(default_factory=list, description="Configuration warnings")
    optimization_opportunities: List[str] = Field(default_factory=list, description="Identified optimization opportunities")

class ConfigurationOperationResult(BaseModel):
    operation: str = Field(..., description="Configuration operation performed")
    target: str = Field(..., description="Target (pipeline, package, environment)")
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Result message")
    changes_made: List[str] = Field(default_factory=list, description="Configuration changes applied")
    validation_results: Optional[PipelineValidationResult] = Field(None, description="Post-operation validation")
    recommendations: List[str] = Field(default_factory=list, description="Further recommendations")
    rollback_info: Optional[Dict[str, Any]] = Field(None, description="Information for rolling back changes")


# Phase 4: Deployment Models

class PipelineExecutionInfo(BaseModel):
    execution_id: str = Field(..., description="Unique execution identifier")
    pipeline_name: str = Field(..., description="Pipeline being executed")
    status: str = Field(..., description="Execution status (running, completed, failed, stopped)")
    start_time: datetime = Field(..., description="Execution start time")
    current_package: Optional[str] = Field(None, description="Currently executing package")
    completed_packages: List[str] = Field(default_factory=list, description="Completed packages")
    execution_method: ExecutionType = Field(..., description="Execution method used")
    resource_usage: Dict[str, Any] = Field(default_factory=dict, description="Current resource usage")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")

class PipelineTestExecutionInfo(BaseModel):
    test_id: str = Field(..., description="Test execution identifier")
    test_configuration: Dict[str, Any] = Field(..., description="Test configuration parameters")
    total_combinations: int = Field(..., description="Total parameter combinations to test")
    completed_runs: int = Field(default=0, description="Number of completed test runs")
    failed_runs: int = Field(default=0, description="Number of failed test runs")
    current_parameters: Dict[str, Any] = Field(default_factory=dict, description="Current parameter set being tested")
    results_location: str = Field(..., description="Results output directory")
    estimated_total_time: Optional[float] = Field(None, description="Estimated total execution time in minutes")

class DistributedExecutionStatus(BaseModel):
    total_nodes: int = Field(..., description="Total nodes in distributed execution")
    active_nodes: List[str] = Field(..., description="Currently active node names")
    failed_nodes: List[str] = Field(default_factory=list, description="Failed or unreachable nodes")
    node_status: Dict[str, str] = Field(default_factory=dict, description="Per-node execution status")
    communication_health: str = Field(..., description="Inter-node communication status")
    load_distribution: Dict[str, float] = Field(default_factory=dict, description="Load distribution across nodes (0.0-1.0)")
    network_utilization: Dict[str, float] = Field(default_factory=dict, description="Network usage per node (0.0-1.0)")

class ExecutionOperationResult(BaseModel):
    operation: str = Field(..., description="Deployment operation performed")
    target: str = Field(..., description="Target execution or pipeline")
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Operation result message")
    changes_made: List[str] = Field(default_factory=list, description="Changes made during operation")
    recommendations: List[str] = Field(default_factory=list, description="Post-operation recommendations")
    execution_time: Optional[float] = Field(None, description="Operation execution time in seconds")

class PipelineMonitoringData(BaseModel):
    monitor_id: str = Field(..., description="Monitoring session identifier")
    execution_info: PipelineExecutionInfo = Field(..., description="Current execution information")
    node_status: Optional[DistributedExecutionStatus] = Field(None, description="Distributed node status")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Real-time performance metrics")
    resource_trends: Dict[str, str] = Field(default_factory=dict, description="Resource usage trends")
    monitoring_interval: int = Field(..., description="Monitoring update interval in seconds")
    last_update: datetime = Field(..., description="Last monitoring update timestamp")
    alerts: List[str] = Field(default_factory=list, description="Active alerts and critical issues")
    warnings: List[str] = Field(default_factory=list, description="Active warnings")

class ExecutionAnalysisResult(BaseModel):
    analysis_id: str = Field(..., description="Analysis session identifier")
    target: str = Field(..., description="Analyzed execution or pipeline")
    analysis_type: str = Field(..., description="Type of analysis performed")
    analysis_timestamp: datetime = Field(..., description="Analysis completion time")
    performance_summary: Dict[str, Any] = Field(default_factory=dict, description="Overall performance summary")
    resource_analysis: Dict[str, Any] = Field(default_factory=dict, description="Resource utilization analysis")
    bottlenecks: List[Dict[str, Any]] = Field(default_factory=list, description="Identified performance bottlenecks")
    optimization_recommendations: List[str] = Field(default_factory=list, description="Performance optimization suggestions")
    baseline_comparison: Optional[Dict[str, Any]] = Field(None, description="Comparison with baseline execution")
    error_analysis: Dict[str, Any] = Field(default_factory=dict, description="Error and failure analysis")

class ExecutionLogsInfo(BaseModel):
    log_operation_id: str = Field(..., description="Log operation identifier")
    target: str = Field(..., description="Target execution or pipeline")
    action: str = Field(..., description="Log operation action performed")
    log_level: str = Field(..., description="Log level filter applied")
    output_format: str = Field(..., description="Log output format")
    log_locations: List[str] = Field(default_factory=list, description="Available log file locations")
    log_statistics: Dict[str, Any] = Field(default_factory=dict, description="Log file statistics and metadata")
    operation_results: List[str] = Field(default_factory=list, description="Results of log operation")
    log_quality: Dict[str, float] = Field(default_factory=dict, description="Log quality assessment metrics")
    available_categories: List[str] = Field(default_factory=list, description="Available log categories")

class CheckpointInfo(BaseModel):
    operation_id: str = Field(..., description="Checkpoint operation identifier")
    action: str = Field(..., description="Checkpoint action performed")
    execution_id: Optional[str] = Field(None, description="Target execution identifier")
    checkpoint_id: Optional[str] = Field(None, description="Checkpoint identifier")
    checkpoint_location: str = Field(..., description="Checkpoint storage location")
    available_checkpoints: List[Dict[str, Any]] = Field(default_factory=list, description="Available checkpoint information")
    operation_results: List[str] = Field(default_factory=list, description="Checkpoint operation results")
    checkpoint_config: Dict[str, Any] = Field(default_factory=dict, description="Checkpoint configuration settings")
    system_status: Dict[str, Any] = Field(default_factory=dict, description="Checkpoint system status")

class PythonAPIInfo(BaseModel):
    api_session_id: str = Field(..., description="API session identifier")
    api_action: str = Field(..., description="API action performed")
    execution_id: Optional[str] = Field(None, description="Target execution for API operations")
    return_format: str = Field(..., description="API response data format")
    available_methods: List[str] = Field(default_factory=list, description="Available API methods")
    operation_results: List[str] = Field(default_factory=list, description="API operation results")
    api_response: Dict[str, Any] = Field(default_factory=dict, description="API response data")
    api_documentation: Dict[str, Any] = Field(default_factory=dict, description="API usage documentation")
    connection_info: Dict[str, Any] = Field(default_factory=dict, description="API connection information")
    usage_statistics: Dict[str, Any] = Field(default_factory=dict, description="API usage statistics")