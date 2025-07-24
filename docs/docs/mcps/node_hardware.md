---
title: Node-Hardware MCP
description: "Node Hardware MCP is a Model Context Protocol server that enables LLMs to monitor and analyze system hardware information including CPU specifications, memory usage, disk performance, network interfaces, GPU details, and sensor data for both local and remote nodes via SSH connections, providing c..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Node-Hardware"
  icon="💻"
  category="Analysis & Visualization"
  description="Node Hardware MCP is a Model Context Protocol server that enables LLMs to monitor and analyze system hardware information including CPU specifications, memory usage, disk performance, network interfaces, GPU details, and sensor data for both local and remote nodes via SSH connections, providing comprehensive hardware monitoring and performance analysis capabilities."
  version="1.0.0"
  actions={["get_cpu_info", "get_memory_info", "get_system_info", "get_disk_info", "get_network_info", "get_gpu_info", "get_sensor_info", "get_process_info", "get_performance_info", "get_remote_node_info", "health_check"]}
  platforms={["claude", "cursor", "vscode"]}
>

## Advanced Features


### Advanced Analytics
Comprehensive analysis and visualization capabilities:
- **Statistical Analysis**: Built-in statistical functions
- **Visualization**: Create charts, plots, and visual representations
- **Interactive**: Generate interactive visualizations

### Customizable Output
- **Multiple Formats**: Support for various output formats
- **Styling Options**: Customizable appearance and themes
- **Export Ready**: Easy export for reports and presentations


## Available Actions


#### `get_cpu_info`
Get comprehensive CPU information including specifications, core configuration, frequency analysis, and performance metrics.

This tool provides detailed CPU analysis including:
- **CPU Model**: Ma...

**Usage Example:**
```python
# Use get_cpu_info function
result = get_cpu_info()
print(result)
```


#### `get_memory_info`
Get comprehensive memory information including capacity, usage patterns, and performance characteristics.

This tool provides detailed memory analysis including:
- **Memory Capacity**: Total, avail...

**Usage Example:**
```python
# Use get_memory_info function
result = get_memory_info()
print(result)
```


#### `get_system_info`
Get comprehensive system information including operating system details, platform configuration, and system status.

This tool provides detailed system analysis including:
- **Operating System**: O...

**Usage Example:**
```python
# Use get_system_info function
result = get_system_info()
print(result)
```


#### `get_disk_info`
Get comprehensive disk information including storage devices, partitions, and I/O performance metrics.

This tool provides detailed disk analysis including:
- **Storage Devices**: Physical disk dri...

**Usage Example:**
```python
# Use get_disk_info function
result = get_disk_info()
print(result)
```


#### `get_network_info`
Get comprehensive network information including interfaces, connections, and bandwidth analysis.

This tool provides detailed network analysis including:
- **Network Interfaces**: Physical and virt...

**Usage Example:**
```python
# Use get_network_info function
result = get_network_info()
print(result)
```


#### Additional Actions
This MCP provides 6 additional actions. Refer to the MCP server documentation for complete details.


## Integration Examples


### Data Analysis Pipeline
```python
# Analyze data with Node-Hardware MCP
data = load_csv("experiment_data.csv")
analysis = analyze_data(data)

# Create visualizations
plot = create_visualization(analysis, "plot_type")
save_plot(plot, "analysis_results.png")
```

### Interactive Analysis
```python
# Interactive data exploration
summary = get_data_summary(data)
correlations = calculate_correlations(data)
create_dashboard(summary, correlations)
```


</MCPDetail>
