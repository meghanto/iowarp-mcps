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
  keywords={["hardware-monitoring", "system-analysis", "performance-metrics", "node-information", "ssh-monitoring", "remote-hardware", "mcp", "llm-integration", "infrastructure-monitoring", "distributed-systems"]}
  license="MIT"
>

### 1. Local Hardware Overview
```
I need a comprehensive overview of my local system's hardware including CPU, memory, disk, and network components.
```

**Tools called:**
- `get_cpu_info` - Get detailed CPU specifications and performance metrics
- `get_memory_info` - Get memory capacity and usage analysis
- `get_disk_info` - Get storage device information and health status
- `get_network_info` - Get network interface and connection details
- `get_system_info` - Get operating system and platform information

This prompt will:
- Use multiple hardware-specific tools to gather comprehensive system information
- Provide detailed specifications for each hardware component
- Generate performance insights and optimization recommendations

### 2. Remote Server Monitoring
```
Monitor the hardware status of a remote server via SSH, focusing on CPU and memory utilization for performance analysis.
```

**Tools called:**
- `get_remote_node_info` - Connect to remote host with SSH authentication and collect CPU/memory data

This prompt will:
- Use `get_remote_node_info` with components filter for CPU and memory analysis
- Establish secure SSH connection to remote server
- Provide performance metrics and utilization analysis for targeted monitoring

### 3. GPU and Thermal Monitoring
```
Check GPU specifications and thermal sensors on both local and remote systems for machine learning workloads.
```

**Tools called:**
- `get_gpu_info` - Local GPU specifications and performance metrics
- `get_sensor_info` - Local thermal monitoring and hardware health
- `get_remote_node_info` - Remote GPU and thermal analysis via SSH

This prompt will:
- Use `get_gpu_info` and `get_sensor_info` for local GPU and thermal monitoring
- Use `get_remote_node_info` with GPU and sensor components for remote analysis
- Provide thermal management insights and performance optimization for ML workloads

### 4. System Health Assessment
```
Perform a comprehensive health check of system capabilities and verify all monitoring tools are working correctly.
```

**Tools called:**
- `health_check` - System health verification and diagnostic assessment
- `get_performance_info` - Performance monitoring and bottleneck analysis

This prompt will:
- Use `health_check` to verify all system monitoring capabilities
- Use `get_performance_info` to assess current system performance
- Provide diagnostic insights and capability verification results

### 5. Performance Bottleneck Analysis
```
Identify performance bottlenecks on a production server by analyzing CPU, memory, disk I/O, and running processes.
```

**Tools called:**
- `get_remote_node_info` - Remote performance analysis via SSH with comprehensive component collection
- `get_performance_info` - Real-time performance monitoring and bottleneck identification

This prompt will:
- Use `get_remote_node_info` with performance-focused component selection (CPU, memory, disk, processes)
- Use `get_performance_info` for detailed bottleneck analysis
- Provide optimization recommendations and performance improvement strategies

### 6. Storage and Network Analysis
```
Analyze storage health and network interface performance on multiple systems for infrastructure monitoring.
```

**Tools called:**
- `get_disk_info` - Local storage analysis and health monitoring
- `get_network_info` - Local network interface performance analysis
- `get_remote_node_info` - Remote storage and network monitoring via SSH

This prompt will:
- Use `get_disk_info` and `get_network_info` for local infrastructure analysis
- Use `get_remote_node_info` with disk and network components for remote monitoring
- Provide infrastructure health insights and performance optimization recommendations

</MCPDetail>
