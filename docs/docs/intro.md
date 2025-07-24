---
sidebar_position: 1
---

# IoWarp MCPs - AI Tools for Scientific Computing

🔬 Discover powerful Model Context Protocol servers that bring AI practically to science. Access data processing, analysis, and system management capabilities.

## What are MCPs?

Model Context Protocol (MCP) servers extend the capabilities of AI assistants like Claude by providing specialized tools and data access. IoWarp MCPs focus specifically on scientific computing workflows, bringing together data processing, analysis, and system management in one comprehensive suite.

## Quick Start

All MCPs are available through the `iowarp-mcps` package and can be installed individually or together:

```bash
# Install all MCPs
uvx iowarp-mcps --help

# Or install specific MCPs
uvx iowarp-mcps adios --help
uvx iowarp-mcps pandas --help
```

## MCP Categories

### 📊 Data Processing (8 MCPs)
Handle scientific data formats, processing, and transformation:
- **Adios** - Advanced I/O system for scientific data
- **ArXiv** - Research paper access and analysis  
- **Compression** - Data compression and decompression
- **HDF5** - Hierarchical data format support
- **Jarvis** - Materials science database access
- **Pandas** - Data analysis and manipulation
- **Parallel Sort** - High-performance data sorting
- **Parquet** - Columnar data format support

### 📈 Analysis & Visualization (2 MCPs)
Create insights and visualizations from your data:
- **Darshan** - I/O performance analysis
- **Plot** - Scientific data visualization

### 🖥️ System Management (3 MCPs)
Manage computational resources and environments:
- **Lmod** - Environment module management
- **Node Hardware** - System hardware information
- **Slurm** - HPC job management

## Key Features

- **🔌 Easy Integration** - Works with Claude Code, Claude Desktop, VS Code, and Cursor
- **🧪 Scientific Focus** - Built specifically for research and scientific computing workflows
- **⚡ High Performance** - Optimized for large-scale data processing and analysis
- **🔗 Interconnected** - MCPs work together seamlessly for complex workflows
- **📖 Well Documented** - Comprehensive documentation with examples for each MCP

## Installation Examples

Each MCP supports multiple installation methods. Here's an example for the Adios MCP:

### Claude Desktop
```json
{
  "mcpServers": {
    "adios-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "adios"]
    }
  }
}
```

### VS Code
```json
"mcp": {
  "servers": {
    "adios-mcp": {
      "type": "stdio", 
      "command": "uvx",
      "args": ["iowarp-mcps", "adios"]
    }
  }
}
```

## Getting Help

- 📖 Browse individual MCP documentation in the sidebar
- 🐛 Report issues on [GitHub](https://github.com/iowarp/iowarp-mcps/issues)
- 💬 Join discussions on [GitHub Discussions](https://github.com/iowarp/iowarp-mcps/discussions)
- 🔗 View source code on [GitHub](https://github.com/iowarp/iowarp-mcps)

## Example Workflow

Here's how different MCPs work together in a typical scientific workflow:

```python
# 1. Load experimental data with Pandas MCP
load_csv("experiment_data.csv")

# 2. Read simulation data with Adios MCP  
read_data("simulation.bp", "temperature", step=100)

# 3. Analyze performance with Darshan MCP
analyze_io("simulation_logs.darshan")

# 4. Create visualizations with Plot MCP
create_plot(combined_data, "scatter", "time", "temperature")

# 5. Submit analysis job with Slurm MCP
submit_job("analysis.sh", nodes=4, time="02:00:00")
```

Ready to get started? Choose an MCP from the sidebar to learn more about its specific capabilities and installation instructions.