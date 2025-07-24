---
title: Jarvis MCP
description: "Jarvis MCP is a Model Context Protocol server that enables LLMs to manage the full lifecycle of data-centric pipelines using the Jarvis framework, featuring pipeline creation, package management, configuration updates, environment building, and execution capabilities for high-performance computin..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Jarvis"
  icon="🤖"
  category="System Management"
  description="Jarvis MCP is a Model Context Protocol server that enables LLMs to manage the full lifecycle of data-centric pipelines using the Jarvis framework, featuring pipeline creation, package management, configuration updates, environment building, and execution capabilities for high-performance computing and data science workflows."
  version="1.0.0"
  actions={["update_pipeline", "build_pipeline_env", "create_pipeline", "load_pipeline", "get_pkg_config", "append_pkg", "configure_pkg", "unlink_pkg", "remove_pkg", "run_pipeline", "destroy_pipeline", "jm_create_config", "jm_load_config", "jm_save_config", "jm_set_hostfile", "jm_bootstrap_from", "jm_bootstrap_list", "jm_reset", "jm_list_pipelines", "jm_cd", "jm_list_repos", "jm_add_repo", "jm_remove_repo", "jm_promote_repo", "jm_get_repo", "jm_construct_pkg", "jm_graph_show", "jm_graph_build", "jm_graph_modify"]}
  platforms={["claude", "cursor", "vscode"]}
>

## Advanced Features


### System Monitoring
Comprehensive system management and monitoring:
- **Real-time Monitoring**: Live system status updates
- **Resource Tracking**: CPU, memory, and disk usage monitoring
- **Performance Analytics**: Detailed performance metrics

### Remote Capabilities
- **SSH Support**: Connect to remote systems securely
- **Distributed Monitoring**: Monitor multiple nodes
- **Health Checks**: Automated system health assessments


## Available Actions


#### `update_pipeline`
Re-apply environment & configuration to every package in a Jarvis-CD pipeline.

**Usage Example:**
```python
# Use update_pipeline function
result = update_pipeline()
print(result)
```


#### `build_pipeline_env`
Rebuild a Jarvis-CD pipeline’s env.yaml, capturing only CMAKE_PREFIX_PATH and PATH

**Usage Example:**
```python
# Use build_pipeline_env function
result = build_pipeline_env()
print(result)
```


#### `create_pipeline`
Create a new Jarvis-CD pipeline environment.

**Usage Example:**
```python
# Use create_pipeline function
result = create_pipeline()
print(result)
```


#### `load_pipeline`
Load an existing Jarvis-CD pipeline environment.

**Usage Example:**
```python
# Use load_pipeline function
result = load_pipeline()
print(result)
```


#### `get_pkg_config`
Retrieve the configuration of a specific package in a Jarvis-CD pipeline.

**Usage Example:**
```python
# Use get_pkg_config function
result = get_pkg_config()
print(result)
```


#### Additional Actions
This MCP provides 24 additional actions. Refer to the MCP server documentation for complete details.


## Integration Examples


### System Monitoring
```python
# Monitor system with Jarvis MCP
status = get_system_status()
performance = get_performance_metrics()

# Set up alerts
if status.cpu_usage > 80:
    send_alert("High CPU usage detected")

# Resource optimization
optimize_resources(performance)
```

### Remote Management
```python
# Manage remote systems
remote_status = get_remote_status("server1.example.com")
deploy_configuration(remote_status, "config.yaml")
monitor_deployment_status()
```


</MCPDetail>
