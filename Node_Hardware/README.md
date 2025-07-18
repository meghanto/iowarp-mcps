# Node Hardware MCP Server

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)](https://github.com/modelcontextprotocol)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive Model Context Protocol (MCP) server for hardware monitoring and system information retrieval. This server enables LLMs to access detailed hardware information, monitor system performance, and analyze resource utilization through **two powerful, specialized tools** with **beautiful, structured output formatting** and **intelligent analysis capabilities**.

## Key Features

- **Two Specialized Tools**  
  - `get_node_info`: Comprehensive local hardware and system information with intelligent filtering
  - `get_remote_node_info`: SSH-based remote node information retrieval with secure authentication

- **Complete Hardware Monitoring**  
  Provides detailed information about CPU, memory, disk, network, and GPU components with real-time statistics and performance metrics.

- **System Information**  
  Retrieves comprehensive OS details, uptime, user information, and system configuration data for complete system analysis.

- **Process Management**  
  Monitors running processes with resource usage statistics, providing insights into system performance and application behavior.

- **Performance Analytics**  
  Offers real-time performance monitoring with CPU usage, memory utilization, and I/O statistics for system optimization.

- **Remote Node Capabilities**  
  Connect to remote nodes via SSH to gather hardware and system information from distributed systems with comprehensive authentication support.

- **Advanced Filtering**  
  Support for include/exclude filters to customize data collection and focus on specific components.

- **Beautiful Output Formatting**  
  Structured, readable output with rich formatting, emojis, and comprehensive summaries with insights and recommendations.

- **Intelligent Analysis**  
  Advanced analysis capabilities with optimization recommendations, performance insights, and predictive maintenance suggestions.

- **Comprehensive Documentation**  
  Detailed tool descriptions with usage examples, parameter explanations, and workflow guidance following pandas MCP patterns.

- **Standardized MCP Interface**  
  Exposes all functionality via the MCP JSON-RPC protocol for seamless integration with language models.

## Capabilities

### Primary Tools

#### **1. `get_node_info` - Local Hardware Information**

**Comprehensive local node hardware and system information with advanced filtering and intelligent analysis.**

This powerful tool provides complete local system analysis by collecting information from all hardware and system components with sophisticated filtering capabilities.

**Key Features:**
- **Local Hardware Discovery**: Automatically detects and analyzes all available local hardware components
- **Intelligent Filtering**: Apply sophisticated filtering to focus on specific components or exclude unwanted data
- **Cross-Component Analysis**: Integrated analysis across all system subsystems for holistic insights
- **Performance Optimization**: Organized hardware information with metadata and collection statistics
- **Predictive Intelligence**: Comprehensive insights and optimization recommendations based on collected data

#### **2. `get_remote_node_info` - Remote Hardware Information via SSH**

**Comprehensive remote node hardware and system information via SSH with advanced filtering and intelligent analysis.**

This powerful tool provides complete remote system analysis by securely connecting to remote nodes via SSH and collecting information from all hardware and system components.

**Key Features:**
- **Secure SSH Connection**: Establishes secure SSH connection with comprehensive authentication support
- **Remote Discovery**: Automatically detects and analyzes all available remote hardware components
- **SSH Authentication**: Support for SSH key-based and password authentication with security best practices
- **Network Optimization**: Optimized data collection to minimize network bandwidth usage and connection overhead
- **Multi-Platform Support**: Compatible with various remote system configurations and platform variations

#### **Available Hardware Components** (Both Tools):
- **cpu**: CPU specifications, core configuration, frequency analysis, cache hierarchy, performance metrics, thermal status
- **memory**: Memory capacity, usage patterns, swap configuration, performance characteristics, health indicators, efficiency analysis
- **disk**: Storage devices, usage analysis, I/O performance, health monitoring, file systems, predictive maintenance
- **network**: Network interfaces, bandwidth analysis, connection details, protocol statistics, security monitoring, performance optimization
- **system**: Operating system details, uptime analysis, user management, configuration, platform information, security status
- **processes**: Running processes, resource consumption, process hierarchy, performance metrics, system load analysis
- **gpu**: GPU specifications, memory analysis, thermal monitoring, performance metrics, driver information, compute capabilities
- **sensors**: Temperature sensors, fan control, voltage monitoring, hardware health, thermal management, predictive maintenance
- **performance**: Real-time performance monitoring, bottleneck analysis, optimization recommendations, trend analysis
- **summary**: Integrated hardware overview with cross-subsystem analysis and comprehensive health assessment

### Secondary Tool: `health_check`

**System health verification and diagnostic tool.**

- Verifies all hardware monitoring capabilities and system compatibility
- Performs comprehensive system diagnostics and performance assessment
- Provides detailed capability status and functionality verification
- Delivers system health metrics and optimization recommendations
- Generates comprehensive diagnostic report with actionable insights

### Beautiful Output Formatting

All tools provide **beautifully formatted output** with:

- **Structured Layout**: Clear organization with emojis and visual indicators
- **Comprehensive Summaries**: Key metrics and statistics at a glance
- **Detailed Insights**: Actionable recommendations and observations
- **Metadata Information**: Collection details and system context
- **Error Handling**: Helpful error messages with troubleshooting suggestions
- **Filter Information**: Clear indication of applied filters and their effects
- **Intelligence Integration**: Smart analysis with optimization recommendations

### Intelligent Analysis Features

- **Performance Optimization**: Automated performance analysis with optimization recommendations
- **Predictive Maintenance**: Sensor-based predictive maintenance and failure prediction
- **Resource Efficiency**: Resource utilization analysis with efficiency improvements
- **System Health Assessment**: Comprehensive health monitoring with trend analysis
- **Bottleneck Identification**: Automated bottleneck detection with resolution strategies
- **Capacity Planning**: Growth trend analysis with capacity recommendations

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)
- SSH client (for remote node capabilities)

## Setup

### 1. Navigate to Node Hardware Directory
```bash
cd /path/to/scientific-mcps/Node_Hardware
```

### 2. Install Dependencies
Using UV (recommended):
```bash
uv sync
```

Using pip:
```bash
pip install -e .
```

**Run the MCP Server directly:**

   ```bash
   uv run node-hardware-mcp
   ```
   
   This will create a `.venv/` folder, install all required packages, and run the server directly.


## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Node Hardware MCP server, use the main `wrp.py` client. You will need to configure it to point to the Node Hardware server.

1.  **Configure:** Ensure that `Node_Hardware` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Node_Hardware
      # - Adios
      # - HDF5
    ```

2.  **Run:** Start the client from the repository root with your desired configuration:
    ```bash
    # Example using the Gemini configuration 
    python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```

### Running the Server with Claude Desktop
Add to your Claude Desktop `settings.json`:
```json
{
  "mcpServers": {
    "pandas-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/scientific-mcps/sNode_Hardware",
        "run", 
        "node-hardware-mcp"
      ]
    }
  }
}
```

### **Claude CLI Integration**
```bash
claude add mcp node-hardware -- uv --directory ~/path/to/scientific-mcps/Node_Hardware run node-hardware-mcp
```

   
### Example Output Structure

```json
{
  "🖥️ Operation": "Get Node Info",
  "✅ Status": "Success",
  "⏰ Timestamp": "2024-01-01 12:00:00",
  "🔧 Hardware Data": {
    "⚡ Cpu": { 
      "🔧 Processor Info": "Intel Core i7-12700K",
      "⚡ Core Configuration": "12 cores, 20 threads",
      "⚡ Frequency Analysis": "3.6 GHz base, 5.0 GHz boost",
      "🌡️ Thermal Status": "Normal, 45°C"
    },
    "💾 Memory": { 
      "📏 Capacity Analysis": "32 GB total, 24 GB available",
      "📊 Usage Patterns": "75% utilization, efficient allocation",
      "🔧 Memory Types": "DDR4-3200, dual-channel"
    },
    "💿 Disk": { 
      "📏 Storage Devices": "1TB NVMe SSD, 2TB HDD",
      "📊 Performance Analysis": "550 MB/s read, 520 MB/s write",
      "💡 Health Status": "Excellent, no errors detected"
    },
    "🌐 Network": {
      "🔧 Interface Configuration": "Gigabit Ethernet, Wi-Fi 6",
      "📊 Bandwidth Analysis": "1000 Mbps capacity, 15% utilization",
      "🔍 Connection Details": "2 active connections, stable"
    }
  },
  "📊 Summary": {
    "🌐 Hostname": "local-system",
    "📊 Components Requested": 4,
    "📊 Components Collected": 4,
    "🔧 Collection Method": "local",
    "⏱️ Collection Time": "1.2 seconds"
  },
  "🔍 Metadata": {
    "🔧 Filters Applied": true,
    "📊 Local Collection": true
  },
  "💡 Insights": [
    "✅ All requested components collected successfully",
    "🔧 Applied component filters: cpu, memory, disk, network",
    "⚡ CPU performance is optimal with good thermal management",
    "💾 Memory utilization is healthy with efficient allocation patterns",
    "💿 Storage performance is excellent with low latency",
    "🌐 Network connectivity is stable with low utilization"
  ]
}
```

### Remote Collection Example Output

```json
{
  "🖥️ Operation": "Get Remote Node Info",
  "✅ Status": "Success",
  "⏰ Timestamp": "2024-01-01 12:00:00",
  "🌐 Target Host": "server1.example.com",
  "🔧 Hardware Data": {
    "⚡ Cpu": { 
      "🔧 Remote Processor": "AMD EPYC 7742",
      "⚡ Core Configuration": "64 cores, 128 threads",
      "⚡ Server Performance": "2.25 GHz base, 3.4 GHz boost"
    },
    "💾 Memory": { 
      "📏 Server Memory": "256 GB total, 180 GB available",
      "📊 Usage Patterns": "70% utilization, server workload",
      "🔧 Memory Configuration": "DDR4-3200, 8-channel"
    }
  },
  "📊 Summary": {
    "🌐 Hostname": "server1",
    "📊 Components Requested": 2,
    "📊 Components Collected": 2,
    "🔧 Collection Method": "remote_ssh",
    "⏱️ Collection Time": "2.8 seconds"
  },
  "🔍 Metadata": {
    "🔧 Filters Applied": true,
    "🌐 SSH Parameters": {
      "🌐 SSH Hostname": "server1.example.com",
      "👤 SSH Username": "admin",
      "🚪 SSH Port": 22,
      "⏳ SSH Timeout": 30
    }
  },
  "💡 Insights": [
    "✅ All requested components collected successfully",
    "🔧 Applied component filters: cpu, memory",
    "🌐 Successfully connected to server1.example.com via SSH",
    "🔑 SSH key authentication used for secure connection",
    "⚡ Remote CPU performance is excellent for server workloads",
    "💾 Remote memory utilization is healthy for production server"
  ]
}
```



## Usage Examples

### Local Hardware Information (`get_node_info`)

```python
# Get all local hardware information with comprehensive analysis
get_node_info()

# Get only CPU and memory information with focused analysis
get_node_info(components=['cpu', 'memory'])

# Get all information except processes and sensors for streamlined results
get_node_info(exclude_components=['processes', 'sensors'])

# Get basic system overview with essential components
get_node_info(components=['system', 'summary'])

# Get performance-focused analysis
get_node_info(components=['cpu', 'memory', 'disk', 'performance'])

# Get thermal and health monitoring
get_node_info(components=['sensors', 'gpu'], include_health=True)
```

### Remote Hardware Information (`get_remote_node_info`)

```python
# Connect to remote host with default settings and comprehensive analysis
get_remote_node_info(hostname='server1.example.com')

# Connect with specific user and SSH key authentication
get_remote_node_info(
    hostname='192.168.1.100',
    username='admin',
    ssh_key='~/.ssh/id_rsa'
)

# Connect with filtering and custom timeout for optimized collection
get_remote_node_info(
    hostname='server1.example.com',
    username='admin',
    port=2222,
    timeout=60,
    components=['cpu', 'memory', 'disk']
)

# High-performance remote collection with minimal overhead
get_remote_node_info(
    hostname='hpc-node-01',
    username='hpcuser',
    ssh_key='~/.ssh/hpc_key',
    timeout=120,
    components=['cpu', 'memory', 'gpu']
)

# Distributed system monitoring
get_remote_node_info(
    hostname='cluster-node-01',
    components=['performance', 'summary'],
    include_performance=True,
    include_health=True
)
```

### Advanced Analysis Examples

```python
# Comprehensive local system analysis with all components
get_node_info(include_performance=True, include_health=True)

# Performance-focused local analysis with bottleneck identification
get_node_info(
    components=['cpu', 'memory', 'disk', 'network', 'performance'],
    include_performance=True
)

# Remote health monitoring with predictive maintenance
get_remote_node_info(
    hostname='server1.example.com',
    components=['sensors', 'disk', 'gpu'],
    include_health=True
)

# Quick local system overview for dashboards
get_node_info(components=['summary'])

# Detailed remote component analysis
get_remote_node_info(
    hostname='server2.example.com',
    components=['cpu', 'memory'],
    include_performance=True
)

# System health assessment
health_check()
```

### SSH Configuration

For remote node capabilities, ensure:

1. **SSH Access**: Target hosts must have SSH service running
2. **Authentication**: Either password or SSH key authentication
3. **Python**: Target hosts should have Python 3.6+ installed
4. **Permissions**: User must have appropriate permissions for system information

### Common SSH Key Setup

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy public key to remote host
ssh-copy-id -i ~/.ssh/id_rsa.pub user@hostname

# Test SSH connection
ssh -i ~/.ssh/id_rsa user@hostname
```

## Available Component Filters

When using `get_node_info` or `get_remote_node_info`, you can filter components:

### Available Components:
- `cpu` - CPU specifications and usage with performance optimization
- `memory` - Memory usage and specifications with efficiency analysis
- `disk` - Disk usage and storage information with health monitoring
- `network` - Network interfaces and statistics with security analysis
- `system` - System information (OS, uptime, users) with configuration analysis
- `processes` - Running processes and resource usage with optimization insights
- `gpu` - GPU information with thermal and performance analysis (if available)
- `sensors` - Temperature and sensor data with predictive maintenance
- `performance` - Real-time performance monitoring with bottleneck analysis
- `summary` - Integrated hardware overview with cross-subsystem analysis

### Filter Examples:
- `components=['cpu', 'memory']` - Focus on processor and memory analysis
- `exclude_components=['processes', 'sensors']` - Skip resource-intensive collections
- `components=['system', 'summary']` - Basic system overview with intelligence
- `components=['cpu', 'memory', 'gpu']` - High-performance computing analysis
- `components=['performance']` - Real-time performance monitoring only
- `exclude_components=['processes']` - Faster collection without process details


### Running the Server Standalone
For testing and development:

```bash
# Start the server
uv run node-hardware-mcp

# Or run directly
python -m node_hardware.server
```

## Error Handling and Troubleshooting

The server provides comprehensive error handling with:

- **Detailed Error Messages**: Clear descriptions of what went wrong
- **Error Classifications**: Categorized error types for better understanding
- **Suggestions**: Actionable recommendations for resolving issues
- **Graceful Degradation**: Partial results when some components fail
- **Intelligent Troubleshooting**: Context-aware troubleshooting guidance

### Common Issues and Solutions:

1. **SSH Connection Failures**:
   - Check network connectivity and firewall settings
   - Verify SSH service is running on target host
   - Confirm authentication credentials and permissions
   - Test SSH connection manually with verbose output
   - Check SSH key permissions (600 for private keys)

2. **Permission Errors**:
   - Run with appropriate user privileges for system access
   - Check file system permissions for configuration files
   - Verify SSH key permissions and ownership
   - Ensure user has hardware monitoring permissions

3. **Missing Dependencies**:
   - Install required system utilities (lm-sensors, nvidia-smi, etc.)
   - Ensure Python libraries are available and up-to-date
   - Check for platform-specific requirements and compatibility
   - Verify system monitoring capabilities are enabled

4. **Performance Issues**:
   - Use component filtering to reduce data collection overhead
   - Optimize SSH connection parameters for network conditions
   - Consider local caching for frequently accessed data
   - Monitor system resources during collection

## Performance Considerations

- **Local Operations**: Typically complete in under 1 second with intelligent caching
- **Remote Operations**: Depend on network latency and SSH connection time (optimized for efficiency)
- **Component Filtering**: Significantly reduces data collection time and network usage
- **Intelligent Caching**: Smart caching for frequently accessed information
- **Parallel Processing**: Optimized data collection with concurrent operations
- **Two-Tool Efficiency**: Specialized tools for local vs remote operations optimize performance

## Security Notes

- **SSH Connections**: Use key-based authentication when possible for enhanced security
- **Credentials**: Never store passwords in configuration files or version control
- **Network**: Ensure secure network connections for remote operations
- **Permissions**: Run with minimal required privileges following security best practices
- **Monitoring**: Built-in security monitoring and anomaly detection capabilities


## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
5. Submit a pull request

## License

This project is part of the Scientific MCPs collection and follows the same licensing terms.
