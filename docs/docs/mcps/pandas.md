---
title: Pandas MCP
description: "Pandas MCP is a Model Context Protocol server that enables LLMs to perform advanced data analysis and manipulation using the powerful Pandas library, featuring comprehensive statistical analysis, data cleaning and transformation, time series operations, multi-format data I/O (CSV, Excel, JSON, Pa..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Pandas"
  icon="🐼"
  category="Data Processing"
  description="Pandas MCP is a Model Context Protocol server that enables LLMs to perform advanced data analysis and manipulation using the powerful Pandas library, featuring comprehensive statistical analysis, data cleaning and transformation, time series operations, multi-format data I/O (CSV, Excel, JSON, Parquet, HDF5), and intelligent data quality assessment for seamless data science workflows."
  version="1.0.0"
  actions={["load_data", "save_data", "statistical_summary", "correlation_analysis", "hypothesis_testing", "handle_missing_data", "clean_data", "groupby_operations", "merge_datasets", "pivot_table", "time_series_operations", "validate_data", "filter_data", "optimize_memory", "profile_data"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={["pandas", "data-analysis", "statistical-analysis", "data-science", "data-manipulation", "time-series", "data-cleaning", "data-transformation", "mcp", "llm-integration"]}
  license="MIT"
>

## Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "pandas-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in VS Code</b></summary>

Add this to your VS Code MCP config file. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

```json
"mcp": {
  "servers": {
    "pandas-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add pandas-mcp -- uvx iowarp-mcps pandas
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "pandas-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
    }
  }
}
```

</details>

<details>
<summary><b>Manual Setup</b></summary>

**Linux/macOS:**
```bash
CLONE_DIR=$(pwd)
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Pandas run pandas-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Pandas run pandas-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Pandas run pandas-mcp --help
```

</details>

## Available Tools


### `load_data`

Load and parse data from multiple file formats with advanced options for data ingestion. 

This comprehensive tool supports CSV, Excel, JSON, Parqu...

**Usage Example:**
```python
# Use load_data function
result = load_data()
print(result)
```


### `save_data`

Save processed data to multiple file formats with optimization options for storage efficiency.

This tool provides comprehensive data export capabi...

**Usage Example:**
```python
# Use save_data function
result = save_data()
print(result)
```


### `statistical_summary`

Generate comprehensive statistical summaries with descriptive statistics, distribution analysis, and data profiling.

This tool provides detailed i...

**Usage Example:**
```python
# Use statistical_summary function
result = statistical_summary()
print(result)
```


### `correlation_analysis`

Perform comprehensive correlation analysis with multiple correlation methods and significance testing.

This tool provides detailed insights into v...

**Usage Example:**
```python
# Use correlation_analysis function
result = correlation_analysis()
print(result)
```


### `hypothesis_testing`

Perform comprehensive statistical hypothesis testing with multiple test types and advanced analysis.

This tool supports a wide range of statistica...

**Usage Example:**
```python
# Use hypothesis_testing function
result = hypothesis_testing()
print(result)
```


### `handle_missing_data`

Comprehensive missing data handling with multiple strategies for detection, imputation, and removal.

This tool provides sophisticated approaches t...

**Usage Example:**
```python
# Use handle_missing_data function
result = handle_missing_data()
print(result)
```


### `clean_data`

Comprehensive data cleaning with advanced outlier detection, duplicate removal, and intelligent type conversion.

This tool provides sophisticated ...

**Usage Example:**
```python
# Use clean_data function
result = clean_data()
print(result)
```


### `groupby_operations`

Perform sophisticated groupby operations with aggregations, transformations, and filtering.

This tool provides comprehensive data grouping capabil...

**Usage Example:**
```python
# Use groupby_operations function
result = groupby_operations()
print(result)
```


### `merge_datasets`

Merge and join datasets with sophisticated join operations and relationship analysis.

This tool supports all SQL-style joins (inner, outer, left, ...

**Usage Example:**
```python
# Use merge_datasets function
result = merge_datasets()
print(result)
```


### `pivot_table`

Create sophisticated pivot tables and cross-tabulations with advanced aggregation capabilities.

This tool provides comprehensive data summarizatio...

**Usage Example:**
```python
# Use pivot_table function
result = pivot_table()
print(result)
```


### `time_series_operations`

Perform comprehensive time series operations with advanced temporal analysis capabilities.

This tool supports resampling, rolling windows, lag fea...

**Usage Example:**
```python
# Use time_series_operations function
result = time_series_operations()
print(result)
```


### `validate_data`

Comprehensive data validation with advanced constraint checking and quality assessment.

This tool performs range validation, consistency checks, b...

**Usage Example:**
```python
# Use validate_data function
result = validate_data()
print(result)
```


### `filter_data`

Advanced data filtering with sophisticated boolean indexing and conditional expressions.

This tool supports complex multi-condition filtering, log...

**Usage Example:**
```python
# Use filter_data function
result = filter_data()
print(result)
```


### `optimize_memory`

Advanced memory optimization for large datasets with intelligent type conversion and chunking strategies.

This tool provides automatic dtype optim...

**Usage Example:**
```python
# Use optimize_memory function
result = optimize_memory()
print(result)
```


### `profile_data`

Comprehensive data profiling with detailed statistical analysis and quality assessment.

This tool provides dataset overview including shape, data ...

**Usage Example:**
```python
# Use profile_data function
result = profile_data()
print(result)
```


## Examples

### 1. Data Loading and Profiling
```
I have a large CSV file with sales data that I need to load and get a comprehensive profile including data types, missing values, and basic statistics.
```

**Tools called:**
- `load_data` - Load CSV file with intelligent format detection
- `profile_data` - Get comprehensive data profile and quality metrics
- `statistical_summary` - Generate descriptive statistics and distributions

### 2. Data Cleaning and Quality Assessment
```
My dataset has missing values and outliers that need to be handled. I also want to remove duplicates and validate the data quality.
```

**Tools called:**
- `handle_missing_data` - Impute missing values with appropriate strategies
- `clean_data` - Remove outliers, duplicates, and optimize data types
- `validate_data` - Apply business rules and data quality checks

### 3. Statistical Analysis and Correlation
```
Analyze the relationships between different variables in my dataset and perform hypothesis testing to validate my assumptions.
```

**Tools called:**
- `correlation_analysis` - Calculate correlation matrices with different methods
- `hypothesis_testing` - Perform t-tests, ANOVA, and normality tests
- `statistical_summary` - Generate comprehensive statistical insights

### 4. Data Transformation and Aggregation
```
I need to group my sales data by region and product category, then create pivot tables for cross-analysis and merge with customer data.
```

**Tools called:**
- `groupby_operations` - Group data and perform multiple aggregations
- `pivot_table` - Create pivot tables with multi-level indexing
- `merge_datasets` - Join datasets using different merge strategies

### 5. Time Series Analysis and Filtering
```
Analyze my time series data by resampling to different frequencies, calculating rolling averages, and filtering specific date ranges.
```

**Tools called:**
- `time_series_operations` - Resample, rolling windows, and lag features
- `filter_data` - Apply complex time-based filtering conditions
- `statistical_summary` - Analyze time series patterns and trends

### 6. Data Export and Memory Optimization
```
Optimize memory usage of my large dataset and export the cleaned data to multiple formats for different teams.
```

**Tools called:**
- `optimize_memory` - Reduce memory usage with dtype optimization
- `save_data` - Export to CSV, Excel, Parquet, and JSON formats
- `profile_data` - Verify optimization results and final data quality

</MCPDetail>
