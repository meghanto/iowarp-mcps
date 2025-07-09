
# Plot MCP Server

## Overview

The Plot MCP Server is a comprehensive Model Context Protocol (MCP) server implementation that provides advanced data visualization capabilities. This server enables AI assistants and other MCP clients to create professional-quality plots from various data sources through a standardized protocol.

The server acts as a bridge between MCP clients and data visualization libraries, providing comprehensive plotting capabilities for CSV, Excel, and other data formats using pandas, matplotlib, and seaborn.

## Features

### Core Capabilities
- **Multiple Plot Types**: Line plots, bar charts, scatter plots, histograms, and correlation heatmaps
- **Data Format Support**: CSV and Excel files (.csv, .xlsx, .xls)
- **Smart Data Handling**: Automatic data cleaning, aggregation, and formatting
- **Data Analysis**: Comprehensive data inspection and column analysis
- **High-Quality Output**: Professional 300 DPI plots with customizable styling
- **Error Handling**: Robust error handling with detailed feedback
- **Flexible Configuration**: Customizable plot parameters and output options

### MCP Tools Available
The server implements the following MCP tools using FastMCP:

1. **get_data_info** - Get detailed information about data files (columns, shape, data types)
2. **create_line_plot** - Create line plots for time series or continuous data
3. **create_bar_plot** - Create bar charts with automatic data aggregation
4. **create_scatter_plot** - Create scatter plots for correlation analysis
5. **create_histogram** - Create histograms for distribution analysis
6. **create_heatmap** - Create correlation heatmaps for numeric data

Each tool is implemented as an async function with proper parameter validation and error handling.

## Prerequisites

### System Requirements
- Linux, macOS, or Windows operating system
- Python 3.10 or higher
- UV package manager (recommended) or pip

### Python Dependencies
- `mcp[cli]>=0.1.0` - MCP framework
- `pytest-asyncio>=1.0.0` - Async testing support
- `python-dotenv>=1.0.0` - Environment variable management
- `pandas>=1.5.0` - Data manipulation and analysis
- `matplotlib>=3.6.0` - Primary plotting library
- `seaborn>=0.12.0` - Statistical visualization
- `openpyxl>=3.0.0` - Excel file support (.xlsx)
- `xlrd>=2.0.0` - Excel file support (.xls)
- `fastapi>=0.95.0` - Web framework (if using HTTP transport)
- `uvicorn>=0.21.0` - ASGI server
- `pydantic>=1.10.0` - Data validation
- `pytest>=7.2.0` - Testing framework
- `requests>=2.28.0` - HTTP client

## Setup

### 1. Navigate to Plot Directory
```bash
cd /path/to/scientific-mcps/Plot
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

### 3. Check Configuration
Ensure `pyproject.toml` is properly configured with all dependencies.

## Quick Start

### 1. Start the MCP Server
```bash
# Using UV with the script entry point (recommended)
uv run plot-mcp

# Using UV with direct Python execution
uv run python src/plot/server.py

# Or using Python directly (after installation)
python src/plot/server.py

# With custom transport options
uv run plot-mcp --transport sse --host 0.0.0.0 --port 8000
```

### 2. Server Initialization
The server will start and display initialization messages:
- Server version: "Plot MCP Server v1.0.0"
- Transport information (stdio or SSE)
- Available tools are automatically registered with FastMCP

### 3. Use with MCP Client


## Project Structure

```
Plot/
├── README.md                      # This documentation
├── pyproject.toml                 # Project configuration and dependencies
├── capability_test.py             # Integration test script
├── data/                          # Sample data files
│   ├── temperature.csv           # Global temperature data (48,470 records)
│   └── sample_data.csv           # Simple test data (10 records)
├── output/                        # Generated plots directory
├── src/                           # Source code
│   └── plot/                      # Main package directory
│       ├── __init__.py
│       ├── server.py              # Main MCP server
│       ├── mcp_handlers.py        # MCP protocol handlers
│       └── capabilities/          # Individual capability modules
│           ├── __init__.py
│           └── plot_capabilities.py # Core plotting functions
└── tests/                         # Test suite
    ├── __init__.py
    ├── test_capabilities.py       # Capability tests
    ├── test_mcp_handlers.py       # MCP handler tests
    └── test_server.py             # Server tests
```

## Configuration

### Environment Variables
- `MCP_TRANSPORT`: Transport type ("stdio" or "sse", default: "stdio")
- `MCP_SSE_HOST`: Host for SSE transport (default: "0.0.0.0")
- `MCP_SSE_PORT`: Port for SSE transport (default: "8000")

### Transport Options
- **stdio**: Standard input/output transport (default)
- **sse**: Server-Sent Events transport for web clients

### Command Line Options
```bash
# Get help
uv run plot-mcp --help

# Specify transport type
uv run plot-mcp --transport sse --host 0.0.0.0 --port 8000

# Check version
uv run plot-mcp --version
```

## Testing

### Running Tests
```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test files
uv run pytest tests/test_capabilities.py -v
uv run pytest tests/test_mcp_handlers.py -v
uv run pytest tests/test_server.py -v

# Run capability integration test
uv run python capability_test.py
```

## Usage Examples

### Sample Data Files
The server comes with sample data files in the `data/` directory:
- `temperature.csv`: Global temperature data by city and country (48,470 records)
  - Columns: record_id, month, day, year, AverageTemperatureFahr, AverageTemperatureUncertaintyFahr, City, country_id, Country, Latitude, Longitude
- `sample_data.csv`: Simple test data with x, y, category, and value columns (10 records)
  - Columns: x, y, category, value

## MCP Capability Usage

The Plot MCP server provides plotting capabilities through the Model Context Protocol using FastMCP framework. The server implements 6 core tools that can be accessed through MCP clients for comprehensive data visualization.

### Available Tools

#### 1. get_data_info
**Purpose**: Get comprehensive information about data files
- **Input**: `file_path` (CSV or Excel file)
- **Output**: File information including columns, data types, shape, null counts, memory usage, and data preview
- **Use Cases**: Data exploration, column discovery, data quality assessment

#### 2. create_line_plot
**Purpose**: Create line plots for continuous data visualization
- **Required Parameters**: `file_path`, `x_column`, `y_column`
- **Optional Parameters**: `title` (default: "Line Plot"), `output_path` (default: "line_plot.png")
- **Use Cases**: Time series analysis, trend visualization, continuous data relationships

#### 3. create_bar_plot
**Purpose**: Create bar charts with automatic data aggregation
- **Required Parameters**: `file_path`, `x_column`, `y_column`
- **Optional Parameters**: `title` (default: "Bar Plot"), `output_path` (default: "bar_plot.png")
- **Smart Features**: Automatically groups categorical data and limits to top 20 categories
- **Use Cases**: Categorical comparisons, grouped data analysis, aggregated summaries

#### 4. create_scatter_plot
**Purpose**: Create scatter plots for correlation analysis
- **Required Parameters**: `file_path`, `x_column`, `y_column`
- **Optional Parameters**: `title` (default: "Scatter Plot"), `output_path` (default: "scatter_plot.png")
- **Use Cases**: Correlation analysis, pattern identification, outlier detection

#### 5. create_histogram
**Purpose**: Create histograms for distribution analysis
- **Required Parameters**: `file_path`, `column`
- **Optional Parameters**: `bins` (default: 30), `title` (default: "Histogram"), `output_path` (default: "histogram.png")
- **Use Cases**: Distribution analysis, frequency analysis, data exploration

#### 6. create_heatmap
**Purpose**: Create correlation heatmaps for numeric data
- **Required Parameters**: `file_path`
- **Optional Parameters**: `title` (default: "Heatmap"), `output_path` (default: "heatmap.png")
- **Smart Features**: Automatically selects numeric columns and calculates correlation matrix
- **Use Cases**: Multi-variable correlation analysis, pattern discovery, data overview

### Usage with MCP Clients

#### Natural Language Requests
When connected to an MCP client (like Claude Desktop), you can make requests like:

- "Can you analyze the temperature data and show me basic information about it?"
- "Create a line plot showing temperature over time"
- "Make a bar chart comparing average temperatures by country"
- "Generate a scatter plot of temperature vs uncertainty"
- "Show me a histogram of the temperature distribution"
- "Create a correlation heatmap of all numeric variables"

#### Automatic Data Handling
The server automatically handles:
- **File format detection**: Supports CSV and Excel files
- **Data cleaning**: Removes invalid or missing data
- **Smart aggregation**: Groups categorical data appropriately for bar charts
- **Error handling**: Provides clear error messages for invalid requests
- **Output management**: Saves plots to the output directory with appropriate naming


### Best Practices

#### Data Preparation
- Ensure data files are in supported formats (CSV, Excel)
- Use clear, descriptive column names
- Handle missing data appropriately before plotting
- Keep file sizes reasonable for better performance

#### Plot Configuration
- Use descriptive titles for better understanding
- Choose appropriate plot types for your data
- Consider data size when creating visualizations
- Use meaningful output file names

#### Error Handling
- Check data file existence and format before requesting plots
- Verify column names exist in your dataset
- Handle cases where data might be empty or invalid
- Use the data info capability to understand your data structure first

## Advanced Features

### Data Handling
- **Automatic Data Cleaning**: Removes NaN values and handles missing data
- **Data Aggregation**: Automatically groups categorical data for bar charts
- **Data Type Detection**: Intelligently handles different column types
- **Large Dataset Support**: Limits visualization to top 20 categories for clarity

### FastMCP Implementation
- **Async Tool Functions**: All tools implemented as async functions for better performance
- **Type Safety**: Full type hints and parameter validation
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful error handling with detailed error messages

### Server Architecture
- **Modular Design**: Separation of concerns with handlers and capabilities
- **Transport Flexibility**: Support for both stdio and SSE transports
- **Environment Configuration**: Configurable via environment variables and command-line arguments
- **Extensible**: Easy to add new plot types and capabilities

## Integration with MCP Clients

The Plot MCP server is designed to work seamlessly with MCP clients like:

- **Claude Desktop**: For interactive data visualization
- **Custom MCP Clients**: Via stdio transport
- **Web Applications**: Via SSE transport
- **Command Line Tools**: Direct integration

## Development

### Adding New Plot Types
1. Add new plotting function to `src/plot/capabilities/plot_capabilities.py`
2. Create handler function in `src/plot/mcp_handlers.py`
3. Add MCP tool definition to `src/plot/server.py`
4. Write tests for the new capability
5. Update documentation

### Code Structure
- Each plotting capability is a function in `plot_capabilities.py`
- Handlers wrap capabilities for MCP protocol compliance
- `server.py` defines the MCP tools and routes them to handlers
- All capabilities use common data loading and error handling

## License

This project is part of the scientific-mcps collection and follows the same licensing terms.

