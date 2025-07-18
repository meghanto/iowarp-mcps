# Pandas MCP Server

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)](https://github.com/modelcontextprotocol)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive **Model Context Protocol (MCP)** server for advanced data analysis and manipulation using Pandas. This server provides LLMs with powerful data science capabilities including statistical analysis, data cleaning, transformation, time series operations, and comprehensive data quality assessment with **beautiful, structured output formatting**.

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
- **Python 3.12+** (required for latest features)
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
uv run python -m pandasmcp.server
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
├── test_all_capabilities.py    # Comprehensive functionality tests
├── create_sample_data.py       # Sample data generation
├── data/                       # Sample datasets
│   ├── employees.csv           # Employee dataset (1000 records)
│   ├── sales.parquet           # Sales data in Parquet format
│   ├── weather.xlsx            # Weather data in Excel format
│   └── inventory.h5            # Inventory data in HDF5 format
├── src/pandasmcp/              # Source code
│   ├── __init__.py             # Package initialization
│   ├── server.py               # Main MCP server with FastMCP
│   ├── mcp_handlers.py         # MCP protocol handlers
│   ├── utils/                  # Utility modules
│   │   ├── output_formatter.py # Beautiful output formatting
│   │   └── __init__.py
│   └── capabilities/           # Core functionality modules
│       ├── data_io.py          # Universal data I/O operations
│       ├── statistics.py       # Statistical analysis
│       ├── data_cleaning.py    # Data cleaning and preprocessing
│       ├── data_profiling.py   # Data profiling and exploration
│       ├── transformations.py  # Data transformation operations
│       ├── time_series.py      # Time series analysis
│       ├── filtering.py        # Data filtering and sampling
│       ├── memory_optimization.py # Memory optimization
│       └── validation.py       # Data validation and testing
├── tests/                      # Test suite
│   ├── test_capabilities.py    # Unit tests for capabilities
│   ├── test_mcp_handlers.py    # Integration tests for MCP handlers
│   └── conftest.py             # Test fixtures and configuration
└── uv.lock                     # Dependency lock file
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

### Run All Capability Tests
```bash
uv run python test_all_capabilities.py
```

### Run Unit Tests
```bash
uv run pytest tests/ -v
```

### Test Coverage
```bash
uv run pytest tests/ --cov=pandasmcp --cov-report=html
```

### Load Sample Data Test
```bash
# Test with the included employee dataset
uv run python -c "
from pandasmcp.capabilities.data_io import load_data_file
result = load_data_file('data/employees.csv')
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
5. **Run capability tests**: `uv run python test_all_capabilities.py`
6. **Submit** a pull request

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
