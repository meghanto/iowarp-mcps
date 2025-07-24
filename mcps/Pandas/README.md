# Pandas MCP - Advanced Data Analysis for LLMs


## Description

Pandas MCP is a Model Context Protocol server that enables LLMs to perform advanced data analysis and manipulation using the powerful Pandas library, featuring comprehensive statistical analysis, data cleaning and transformation, time series operations, multi-format data I/O (CSV, Excel, JSON, Parquet, HDF5), and intelligent data quality assessment for seamless data science workflows.



## 🛠️ Installation

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

## Capabilities

### `load_data`
**Description**: Load and parse data from multiple file formats with advanced options for data ingestion, supporting CSV, Excel, JSON, Parquet, and HDF5 formats with intelligent parsing capabilities.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `file_format` (str, optional): File format (csv, excel, json, parquet, hdf5) - auto-detected if None
- `sheet_name` (str, optional): Excel sheet name or index (for Excel files)
- `encoding` (str, optional): Character encoding (utf-8, latin-1, etc.) - auto-detected if None
- `columns` (List[str], optional): List of specific columns to load (None loads all columns)
- `nrows` (int, optional): Maximum number of rows to load (None loads all rows)

**Returns**: Dictionary containing loaded dataset, metadata, data information, and loading statistics with parsing performance metrics.

### `save_data`
**Description**: Save processed data to multiple file formats with optimization options for storage efficiency, supporting format-specific optimizations and compression options.

**Parameters**:
- `file_path` (str): Absolute path where the data will be saved (required)
- `file_format` (str, optional): Output format (csv, excel, json, parquet, hdf5) - auto-detected from extension if None
- `compression` (str, optional): Compression method (gzip, bz2, xz) for supported formats
- `index` (bool): Whether to include row indices in output (default: True)

**Returns**: Dictionary containing save status, file information, export statistics, and optimization recommendations.

### `statistical_summary`
**Description**: Generate comprehensive statistical summary with advanced analytics including descriptive statistics, distribution analysis, and outlier detection.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `columns` (List[str], optional): List of specific columns to analyze (None analyzes all numerical columns)
- `include_distributions` (bool): Whether to include distribution analysis and normality tests (default: False)

**Returns**: Dictionary containing descriptive statistics, distribution analysis, data profiling, and outlier detection results.

### `correlation_analysis`
**Description**: Perform comprehensive correlation analysis with multiple correlation methods and significance testing, providing insights into variable relationships and dependency patterns.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `method` (str): Correlation method (pearson, spearman, kendall, default: "pearson")
- `columns` (List[str], optional): List of specific columns to analyze (None analyzes all numerical columns)
- `significance_level` (float): Significance level for correlation testing (default: 0.05)

**Returns**: Dictionary containing correlation matrices, significance testing results, and relationship insights with multicollinearity analysis.

### `hypothesis_testing`
**Description**: Perform statistical hypothesis testing with multiple test types including t-tests, ANOVA, and normality tests for comprehensive statistical validation.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `test_type` (str): Type of statistical test (t_test, anova, normality, chi_square) (required)
- `columns` (List[str], optional): List of columns for analysis (test-specific requirements)
- `grouping_column` (str, optional): Column for grouping data (required for ANOVA and group comparisons)
- `significance_level` (float): Significance level for hypothesis testing (default: 0.05)

**Returns**: Dictionary containing test statistics, p-values, confidence intervals, and statistical conclusions with interpretation.

### `handle_missing_data`
**Description**: Handle missing data with comprehensive strategies and statistical methods including detection, imputation, and removal with pattern analysis.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `strategy` (str): Missing data strategy (detect, impute, remove, analyze, default: "detect")
- `method` (str, optional): Imputation method (mean, median, mode, forward_fill, backward_fill, interpolate)
- `columns` (List[str], optional): List of specific columns to process (None processes all columns)

**Returns**: Dictionary containing missing data patterns, imputation results, and data quality improvements with strategy recommendations.

### `clean_data`
**Description**: Perform comprehensive data cleaning including outlier removal, duplicate detection, data type optimization, and data validation with quality assessment.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `remove_duplicates` (bool): Whether to remove duplicate rows (default: True)
- `handle_outliers` (str): Outlier handling method (remove, cap, none, default: "none")
- `standardize_columns` (bool): Whether to standardize column names (default: False)
- `optimize_dtypes` (bool): Whether to optimize data types for memory efficiency (default: True)

**Returns**: Dictionary containing cleaned dataset, cleaning summary, data quality improvements, and optimization results.

### `groupby_operations`
**Description**: Perform comprehensive group-by operations with multiple aggregation functions and statistical analysis for data summarization and insights.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `group_columns` (List[str]): List of columns to group by (required)
- `agg_functions` (dict): Dictionary mapping columns to aggregation functions (mean, sum, count, std, etc.)
- `include_stats` (bool): Whether to include additional statistical metrics (default: False)

**Returns**: Dictionary containing grouped data, aggregation results, group statistics, and insights with pattern analysis.

### `merge_datasets`
**Description**: Merge multiple datasets using different join strategies with comprehensive data integration and validation for complex data combinations.

**Parameters**:
- `left_file_path` (str): Absolute path to the left dataset (required)
- `right_file_path` (str): Absolute path to the right dataset (required)
- `join_keys` (List[str]): List of columns to join on (required)
- `how` (str): Type of merge (inner, outer, left, right, default: "inner")
- `validate` (str, optional): Validation level (one_to_one, one_to_many, many_to_one, many_to_many)

**Returns**: Dictionary containing merged dataset, merge statistics, data integration summary, and validation results.

### `pivot_table`
**Description**: Create comprehensive pivot tables with multi-level indexing and aggregation for advanced data summarization and cross-tabulation analysis.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `index_columns` (List[str]): List of columns to use as row indices (required)
- `value_columns` (List[str]): List of columns to aggregate (required)
- `agg_function` (str): Aggregation function (mean, sum, count, std, default: "mean")
- `columns` (List[str], optional): List of columns to use as column indices

**Returns**: Dictionary containing pivot table results, aggregation summary, and cross-tabulation insights with statistical analysis.

### `time_series_operations`
**Description**: Perform comprehensive time series analysis including resampling, rolling windows, lag features, and trend analysis for temporal data insights.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `date_column` (str): Name of the date/time column (required)
- `operation` (str): Time series operation (resample, rolling, lag, trend, default: "resample")
- `frequency` (str, optional): Resampling frequency (D, W, M, Q, Y) for resample operations
- `window_size` (int, optional): Window size for rolling operations (default: 7)

**Returns**: Dictionary containing time series results, temporal patterns, trend analysis, and seasonal insights.

### `validate_data`
**Description**: Perform comprehensive data validation with business rules, data quality checks, and constraint validation for data integrity assessment.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `validation_rules` (dict): Dictionary of validation rules and constraints (required)
- `strict_mode` (bool): Whether to use strict validation (default: False)
- `generate_report` (bool): Whether to generate detailed validation report (default: True)

**Returns**: Dictionary containing validation results, rule compliance, data quality scores, and improvement recommendations.

### `filter_data`
**Description**: Apply complex filtering operations with multiple conditions and logical operators for advanced data subsetting and selection.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `conditions` (dict): Dictionary of filtering conditions and criteria (required)
- `logical_operator` (str): Logical operator for multiple conditions (and, or, default: "and")
- `save_filtered` (bool): Whether to save filtered results to file (default: False)

**Returns**: Dictionary containing filtered dataset, filtering summary, condition results, and data subset statistics.

### `optimize_memory`
**Description**: Optimize memory usage of datasets with dtype optimization, memory profiling, and efficiency recommendations for large data processing.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `aggressive` (bool): Whether to use aggressive optimization (default: False)
- `preserve_precision` (bool): Whether to preserve numerical precision (default: True)
- `generate_report` (bool): Whether to generate optimization report (default: True)

**Returns**: Dictionary containing optimized dataset, memory usage statistics, optimization results, and efficiency improvements.

### `profile_data`
**Description**: Generate comprehensive data profile with detailed schema analysis, data quality assessment, and statistical profiling for thorough data exploration.

**Parameters**:
- `file_path` (str): Absolute path to the data file (required)
- `detailed` (bool): Whether to include detailed profiling analysis (default: False)
- `sample_size` (int, optional): Number of rows to sample for large datasets (None uses all data)

**Returns**: Dictionary containing data schema, quality metrics, statistical profile, and visualization recommendations with insights.

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
