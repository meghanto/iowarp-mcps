# Pandas MCP Server

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)](https://github.com/modelcontextprotocol)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive **Model Context Protocol (MCP)** server for advanced data analysis and manipulation using Pandas. This server provides LLMs with powerful data science capabilities including statistical analysis, data cleaning, transformation, time series operations, and comprehensive data quality assessment with **beautiful, structured output formatting**.


## Capabilities

### `load_data`
**Description**: Load data from various file formats with comprehensive parsing options.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `file_format` (Any, optional): Parameter for file_format
- `sheet_name` (Any, optional): Parameter for sheet_name
- `encoding` (Any, optional): Parameter for encoding
- `columns` (Any, optional): Parameter for columns
- `nrows` (Any, optional): Parameter for nrows

**Returns**: Dictionary containing: - data: Loaded dataset in structured format - metadata: File information, data types, and loading statistics - data_info: Shape, columns, and data quality metrics - loading_stats: Performance metrics and parsing information

### `save_data`
**Description**: Save data to various file formats with comprehensive export options.

**Parameters**:
- `data` (dict): Parameter for data
- `file_path` (str): Parameter for file_path
- `file_format` (Any, optional): Parameter for file_format
- `index` (bool, optional): Parameter for index (default: True)

**Returns**: Dictionary containing: - save_info: File save details including size and format - compression_stats: Space savings and compression metrics - export_stats: Performance metrics and data integrity checks - file_details: Output file specifications and validation

### `statistical_summary`
**Description**: Generate comprehensive statistical summary with advanced analytics.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `columns` (Any, optional): Parameter for columns
- `include_distributions` (bool, optional): Parameter for include_distributions (default: False)

**Returns**: Dictionary containing: - descriptive_stats: Mean, median, mode, standard deviation, and percentiles - distribution_analysis: Skewness, kurtosis, and normality test results - data_profiling: Data types, missing values, and unique value counts - outlier_detection: Outlier identification and statistical anomalies

### `correlation_analysis`
**Description**: Perform comprehensive correlation analysis with statistical significance testing.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `method` (str, optional): Parameter for method (default: pearson)
- `columns` (Any, optional): Parameter for columns

**Returns**: Dictionary containing: - correlation_matrix: Full correlation matrix with coefficient values - significance_tests: P-values and statistical significance indicators - correlation_insights: Strong correlations and dependency patterns - visualization_data: Data formatted for correlation heatmaps and plots

### `hypothesis_testing`
**Description**: Perform comprehensive statistical hypothesis testing with multiple test types and advanced analysis.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `test_type` (str): Parameter for test_type
- `column1` (str): Parameter for column1
- `column2` (Any, optional): Parameter for column2
- `alpha` (float, optional): Parameter for alpha (default: 0.05)

**Returns**: Dictionary containing: - test_results: Statistical test results including test statistic and p-value - effect_size: Effect size measures and practical significance assessment - confidence_intervals: Confidence intervals for parameters and differences - interpretation: Statistical interpretation and practical conclusions

### `handle_missing_data`
**Description**: Handle missing data with comprehensive strategies and statistical methods.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `strategy` (str, optional): Parameter for strategy (default: detect)
- `method` (Any, optional): Parameter for method
- `columns` (Any, optional): Parameter for columns

**Returns**: Dictionary containing: - missing_data_report: Detailed analysis of missing data patterns - imputation_results: Results of imputation with quality metrics - data_completeness: Before/after comparison of data completeness - strategy_recommendations: Suggested approaches for optimal data handling

### `clean_data`
**Description**: Perform comprehensive data cleaning with advanced quality improvement techniques.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `remove_duplicates` (bool, optional): Parameter for remove_duplicates (default: False)
- `detect_outliers` (bool, optional): Parameter for detect_outliers (default: False)
- `convert_types` (bool, optional): Parameter for convert_types (default: False)

**Returns**: Dictionary containing: - cleaning_report: Detailed summary of cleaning operations performed - data_quality_metrics: Before/after data quality comparison - outlier_analysis: Outlier detection results and recommendations - type_conversion_log: Data type changes and optimization results

### `groupby_operations`
**Description**: Perform sophisticated groupby operations with comprehensive aggregation options.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `group_by` (Any): Parameter for group_by
- `operations` (Any): Parameter for operations
- `filter_condition` (Any, optional): Parameter for filter_condition

**Returns**: Dictionary containing: - grouped_results: Results of groupby operations with aggregated data - group_statistics: Statistics about group sizes and distributions - aggregation_summary: Summary of all aggregation operations performed - performance_metrics: Groupby operation performance and optimization insights

### `merge_datasets`
**Description**: Merge and join datasets with comprehensive integration capabilities.

**Parameters**:
- `left_file` (str): Parameter for left_file
- `right_file` (str): Parameter for right_file
- `join_type` (str, optional): Parameter for join_type (default: inner)
- `left_on` (Any, optional): Parameter for left_on
- `right_on` (Any, optional): Parameter for right_on
- `on` (Any, optional): Parameter for on

**Returns**: Dictionary containing: - merged_data: Results of the merge operation - merge_statistics: Statistics about the merge operation and data overlap - data_quality_report: Quality assessment of the merged dataset - relationship_analysis: Analysis of data relationships and join effectiveness

### `pivot_table`
**Description**: Create sophisticated pivot tables with comprehensive aggregation options.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `index` (Any): Parameter for index
- `columns` (Any, optional): Parameter for columns
- `values` (Any, optional): Parameter for values
- `aggfunc` (str, optional): Parameter for aggfunc (default: mean)

**Returns**: Dictionary containing: - pivot_results: The pivot table with aggregated data - summary_statistics: Statistical summary of the pivot operation - data_insights: Key insights and patterns from the pivot analysis - visualization_data: Data formatted for pivot table visualization

### `time_series_operations`
**Description**: Perform comprehensive time series operations with advanced temporal analysis.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `date_column` (str): Parameter for date_column
- `operation` (str): Parameter for operation
- `window_size` (Any, optional): Parameter for window_size
- `frequency` (Any, optional): Parameter for frequency

**Returns**: Dictionary containing: - time_series_results: Results of the time series operation - temporal_analysis: Trend and seasonality analysis - statistical_summary: Time series statistical properties - forecasting_insights: Patterns and insights for forecasting applications

### `validate_data`
**Description**: Perform comprehensive data validation with advanced constraint checking and quality assessment.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `validation_rules` (Any): Parameter for validation_rules

**Returns**: Dictionary containing: - validation_results: Detailed validation results for each column and rule - data_quality_score: Overall data quality score and assessment - violation_summary: Summary of validation violations and error patterns - recommendations: Suggested actions for data quality improvement

### `filter_data`
**Description**: Perform advanced data filtering with sophisticated boolean indexing and conditional expressions.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `filter_conditions` (Any): Parameter for filter_conditions
- `output_file` (Any, optional): Parameter for output_file

**Returns**: Dictionary containing: - filtered_data: Results of filtering operation with matching records - filter_statistics: Summary of filtering results including row counts - data_quality_report: Quality assessment of filtered dataset - performance_metrics: Filtering operation performance and efficiency

### `optimize_memory`
**Description**: Perform advanced memory optimization for large datasets with intelligent strategies.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `optimize_dtypes` (bool, optional): Parameter for optimize_dtypes (default: True)
- `chunk_size` (Any, optional): Parameter for chunk_size

**Returns**: Dictionary containing: - memory_optimization_results: Before/after memory usage comparison - dtype_optimization_log: Details of data type changes and memory savings - chunking_strategy: Optimal chunking recommendations for large datasets - performance_metrics: Speed and efficiency improvements achieved

### `profile_data`
**Description**: Perform comprehensive data profiling with detailed statistical analysis and quality assessment.

**Parameters**:
- `file_path` (str): Parameter for file_path
- `include_correlations` (bool, optional): Parameter for include_correlations (default: False)
- `sample_size` (Any, optional): Parameter for sample_size

**Returns**: Dictionary containing: - data_profile: Comprehensive dataset overview including shape, types, and statistics - column_analysis: Detailed analysis of each column including distributions - data_quality_metrics: Missing values, duplicates, and data quality indicators - correlation_matrix: Variable correlations (if include_correlations is True)


## Key Features

### **Universal Data I/O**
- Load and save data in multiple formats (CSV, Excel, JSON, Parquet, HDF5)
- Intelligent format detection and encoding handling
- Memory-efficient processing for large datasets
- Automatic data type optimization

### **Statistical Analysis**
- Comprehensive statistical summaries with distribution analysis
- Correlation analysis (Pearson, Spearman, Kendall)
- Hypothesis testing (t-tests, chi-square, ANOVA)
- Advanced statistical inference with confidence intervals

### **Data Cleaning & Quality**
- Advanced missing data handling with multiple imputation strategies
- Intelligent outlier detection (IQR, Z-score, Isolation Forest)
- Duplicate removal with fuzzy matching
- Data validation with customizable business rules

### **Data Transformation**
- Sophisticated groupby operations with multiple aggregations
- Dataset merging with all SQL-style joins
- Pivot tables and cross-tabulations
- Complex data reshaping and transformation

### **Time Series Operations**
- Specialized time series analysis and resampling
- Rolling window calculations with customizable functions
- Lag feature creation for predictive modeling
- Seasonality detection and trend analysis

### **Performance Optimization**
- Memory optimization with intelligent dtype conversion
- Chunked processing for datasets exceeding memory
- Parallel processing for CPU-intensive operations
- Progress tracking for long-running operations

### **Beautiful Output Formatting**
- Structured, readable output with rich formatting
- Comprehensive operation summaries with insights
- Color-coded status indicators and progress tracking
- Detailed metadata and performance metrics

### **Standardized MCP Interface**
- Full MCP JSON-RPC protocol compliance
- Seamless integration with language models
- Comprehensive error handling and validation
- Extensive tool descriptions with usage guidance

## Installation & Setup

### Prerequisites
- **Python 3.10+** (required for latest features)
- **[UV](https://docs.astral.sh/uv/)** package manager (recommended)
- **Linux/macOS** environment (for optimal compatibility)

### Quick Start

1. **Navigate to Pandas Directory**
```bash
cd /path/to/scientific-mcps/Pandas
```

2. **Install Dependencies with UV**
```bash
# Install all dependencies and create virtual environment
uv sync

# Or install specific packages
uv add fastmcp pandas numpy scipy openpyxl pyarrow tables rich tabulate
```

3. **Run the MCP Server**
```bash
# Direct execution
uv run pandas-mcp

# Or with Python module
uv run python -m src.server
```

## Integration Options

### **Claude Desktop Integration**
Add to your Claude Desktop `settings.json`:
```json
{
  "mcpServers": {
    "pandas-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/scientific-mcps/Pandas",
        "run", 
        "pandas-mcp"
      ]
    }
  }
}
```

### **WARP Client Integration**
Configure in your WARP configuration (e.g., `bin/confs/Gemini.yaml`):
```yaml
MCP:
  - Pandas
  # - Other MCPs...
```

Run with:
```bash
python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
```

### **Claude CLI Integration**
```bash
claude add mcp pandas -- uv --directory ~/path/to/scientific-mcps/Pandas run pandas-mcp
```

## Comprehensive Capabilities

### **Data Loading & Saving**
| Tool | Description | Formats |
|------|-------------|---------|
| `load_data` | Load data with intelligent format detection | CSV, Excel, JSON, Parquet, HDF5 |
| `save_data` | Export with compression and optimization | All formats + SQL databases |

### **Statistical Analysis**
| Tool | Description | Features |
|------|-------------|----------|
| `statistical_summary` | Comprehensive statistical analysis | Descriptive stats, distributions, outliers |
| `correlation_analysis` | Relationship analysis between variables | Pearson, Spearman, Kendall methods |
| `hypothesis_testing` | Statistical inference and testing | t-tests, chi-square, ANOVA, normality |

### **Data Quality & Cleaning**
| Tool | Description | Methods |
|------|-------------|---------|
| `handle_missing_data` | Missing data detection and imputation | Mean, median, forward/backward fill, regression |
| `clean_data` | Comprehensive data cleaning | Outlier detection, duplicate removal, type conversion |
| `validate_data` | Data validation with business rules | Range checks, pattern matching, consistency |

### **Data Transformation**
| Tool | Description | Operations |
|------|-------------|------------|
| `groupby_operations` | Advanced grouping and aggregation | Multiple group columns, custom aggregations |
| `merge_datasets` | Dataset joining and merging | Inner, outer, left, right joins |
| `pivot_table` | Pivot tables and cross-tabulations | Multi-level indexing, custom aggregations |
| `filter_data` | Advanced data filtering | Boolean indexing, complex conditions |

### **Time Series Analysis**
| Tool | Description | Features |
|------|-------------|----------|
| `time_series_operations` | Comprehensive time series analysis | Resampling, rolling windows, lag features |

### **Performance & Optimization**
| Tool | Description | Benefits |
|------|-------------|----------|
| `optimize_memory` | Memory usage optimization | Dtype optimization, chunking, sparse arrays |
| `profile_data` | Data profiling and analysis | Shape, types, quality metrics, correlations |

## Usage Examples

### **Basic Data Analysis**
```python
# Load and analyze employee data
result = load_data("/data/employees.csv", encoding="utf-8")
stats = statistical_summary("/data/employees.csv", 
                           columns=["salary", "age", "years_experience"],
                           include_distributions=True)
```

### **Data Cleaning Pipeline**
```python
# Comprehensive data cleaning
missing_handled = handle_missing_data("/data/dataset.csv", 
                                     strategy="mean", 
                                     columns=["price", "quantity"])

cleaned = clean_data("/data/dataset.csv", 
                    remove_duplicates=True, 
                    detect_outliers=True,
                    convert_types=True)
```

### **Advanced Transformations**
```python
# Group sales data by region and category
grouped = groupby_operations("/data/sales.csv", 
                            group_by=["region", "category"], 
                            operations={"revenue": "sum", "quantity": "mean"})

# Create pivot table for cross-analysis
pivot = pivot_table("/data/sales.csv", 
                   index=["date"], 
                   columns=["category"], 
                   values=["revenue"],
                   aggfunc="sum")
```

### **Time Series Analysis**
```python
# Resample time series to monthly frequency
resampled = time_series_operations("/data/timeseries.csv", 
                                  date_column="timestamp", 
                                  operation="resample",
                                  frequency="M")

# Calculate rolling averages
rolling = time_series_operations("/data/timeseries.csv", 
                                date_column="timestamp",
                                operation="rolling_mean",
                                window_size=7)
```

### **Memory Optimization**
```python
# Optimize large dataset memory usage
optimized = optimize_memory("/data/large_dataset.csv", 
                           optimize_dtypes=True, 
                           chunk_size=10000)
```

## Project Structure

```text
Pandas/
├── pyproject.toml              # Project metadata & UV dependencies
├── README.md                   # This documentation
├── .gitignore                  # Git ignore patterns
├── pytest.ini                  # Pytest configuration
├── uv.lock                     # Dependency lock file
├── sample_data.csv             # Sample employee dataset (30 records)
├── sample_data_filtered.csv    # Filtered sample data output
├── src/                        # Source code
│   ├── server.py               # Main MCP server with FastMCP and direct implementation calls
│   └── implementation/         # Core functionality modules
│       ├── __init__.py         # Package initialization
│       ├── data_io.py          # Universal data I/O operations
│       ├── pandas_statistics.py # Statistical analysis
│       ├── data_cleaning.py    # Data cleaning and preprocessing
│       ├── data_profiling.py   # Data profiling and exploration
│       ├── transformations.py  # Data transformation operations
│       ├── time_series.py      # Time series analysis
│       ├── filtering.py        # Data filtering and sampling
│       ├── memory_optimization.py # Memory optimization
│       ├── validation.py       # Data validation and testing
│       └── output_formatter.py # Beautiful output formatting
├── tests/                      # Test suite
│   ├── __init__.py             # Test package initialization
│   └── test_capabilities.py    # Unit tests for capabilities
└── docs/                       # Documentation
```

## Supported Data Formats

| Format | Extensions | Features |
|--------|------------|----------|
| **CSV** | `.csv`, `.tsv` | Encoding detection, delimiter inference, custom parsing |
| **Excel** | `.xlsx`, `.xls` | Multiple sheets, custom ranges, format preservation |
| **JSON** | `.json`, `.jsonl` | Nested structures, custom orientations, large file handling |
| **Parquet** | `.parquet` | Columnar storage, compression, metadata preservation |
| **HDF5** | `.h5`, `.hdf5` | Hierarchical data, dataset and group management |
| **Pickle** | `.pkl`, `.pickle` | Python object serialization, complex data structures |

## Testing

### Run All Tests
```bash
uv run pytest tests/ -v
```

### Run Specific Test Files
```bash
# Test capabilities
uv run pytest tests/test_capabilities.py -v

# Test capabilities
uv run pytest tests/test_capabilities.py -v
```

### Test Coverage
```bash
uv run pytest tests/ --cov=src --cov-report=html
```

### Load Sample Data Test
```bash
# Test with the included sample dataset
uv run python -c "
from src.implementation.data_io import load_data_file
result = load_data_file('sample_data.csv')
print(f'Loaded {len(result)} records successfully!')
"
```

## Configuration

Configure the server through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PANDAS_MAX_ROWS` | Maximum rows to process | 100000 |
| `PANDAS_CHUNK_SIZE` | Default chunk size for large datasets | 10000 |
| `PANDAS_MEMORY_LIMIT` | Memory limit in MB | 1000 |
| `PANDAS_CACHE_SIZE` | Cache size for repeated operations | 100 |
| `PANDAS_TEMP_DIR` | Temporary directory for intermediate files | `/tmp` |

## Dependencies

Core dependencies managed through `pyproject.toml` with UV:

### **MCP & Server Framework**
- `fastmcp>=0.1.0` - Fast MCP server implementation
- `fastapi>=0.104.0` - Modern web framework for APIs
- `pydantic>=2.0.0` - Data validation and settings management

### **Data Science Stack**
- `pandas>=2.2.0` - Core data manipulation library
- `numpy>=1.24.0` - Numerical computing foundation
- `scipy>=1.11.0` - Scientific computing and statistics
- `scikit-learn>=1.3.0` - Machine learning algorithms

### **File Format Support**
- `openpyxl>=3.1.0` - Excel file handling
- `xlrd>=2.0.0` - Legacy Excel file support
- `pyarrow>=15.0.0` - Parquet and Arrow format support
- `tables>=3.9.0` - HDF5 file format support
- `sqlalchemy>=2.0.0` - SQL database connectivity

### **Utilities & Formatting**
- `rich>=13.0.0` - Beautiful terminal formatting
- `tabulate>=0.9.0` - Table formatting
- `psutil>=5.9.0` - System and process utilities
- `python-dotenv>=1.0.0` - Environment variable management

## Beautiful Output Features

The server provides structured, visually appealing output with:

- **Rich Formatting**: Color-coded status indicators and progress bars
- **Comprehensive Summaries**: Detailed operation results with insights
- **Metadata Tracking**: Performance metrics and execution details
- **Success Indicators**: Clear success/failure status with explanations
- **Structured Data**: Organized output with consistent formatting
- **Actionable Insights**: Recommendations and next steps

## Error Handling

Comprehensive error handling with detailed messages:

- **File Operations**: Not found, permission issues, format errors
- **Data Types**: Type conversion failures, schema mismatches
- **Memory Issues**: Graceful handling with chunking fallbacks
- **Statistical Errors**: Edge cases, insufficient data warnings
- **Validation Errors**: Specific constraint violations with guidance

## Performance Features

- **Memory Optimization**: Efficient data types and sparse arrays
- **Chunked Processing**: Handle datasets exceeding memory limits
- **Lazy Evaluation**: Efficient computation chains
- **Parallel Processing**: CPU-intensive operations
- **Caching**: Repeated operations optimization
- **Progress Tracking**: Long-running operation monitoring

## Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Add tests** for new functionality
4. **Ensure tests pass**: `uv run pytest`
5. **Submit** a pull request

### Development Setup
```bash
# Clone and setup development environment
git clone <repository-url>
cd Pandas
uv sync --dev
uv run pre-commit install
```

## License

This project is part of the **Jarvis Scientific MCPs** collection and follows the same licensing terms.

<div align="center">

**Built with Pandas • Powered by UV • MCP Protocol**

*For questions and support, please refer to the main Jarvis documentation.*

</div>
