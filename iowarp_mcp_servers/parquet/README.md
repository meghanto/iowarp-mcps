# Parquet MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)

**Part of [IoWarp MCPs](https://iowarp.github.io/iowarp-mcps/) - Gnosis Research Center**

Model Context Protocol (MCP) server for Apache Parquet files. Provides metadata extraction, column-based operations, and data filtering for AI agents.

## Quick Start

```bash
# From the monorepo
cd iowarp-mcps/iowarp_mcp_servers/parquet
uv run parquet-mcp
```

## Key Features

- 16KB payload limit with error messages and suggested slice sizes
- JSON filtering with compound/nested operations (AND/OR/NOT, comparisons, NULL checks, IN clauses)
- Column projection and pagination
- 7 aggregation operations (min, max, mean, sum, count, std, count_distinct)
- Structured JSON error responses
- Tested on 131M+ row datasets
- 192 tests

## Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- PyArrow library for Parquet file processing

### Setup and Run

```bash
# Clone the repository
git clone https://github.com/iowarp/iowarp-mcps.git
cd iowarp-mcps/iowarp_mcp_servers/parquet

# Install dependencies
uv sync

# Run the server
uv run parquet-mcp
```

### MCP Client Integration

<details>
<summary><b>Cursor</b></summary>

Create `.cursor/mcp.json` in the parquet server directory:

```json
{
  "mcpServers": {
    "parquet-mcp": {
      "command": "uv",
      "args": ["run", "parquet-mcp"],
      "disabled": false,
      "env": {}
    }
  }
}
```

**Note**: This runs from the current directory, so Cursor must be opened in the `parquet/` directory.

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
# From the parquet directory
cd iowarp-mcps/iowarp_mcp_servers/parquet
claude mcp add parquet-mcp -- uv run parquet-mcp
```

</details>

## Available Tools

### 1. summarize_tool

Get metadata about a Parquet file without loading data.

**Parameters:**
- `file_path` (str): Path to the Parquet file

**Returns:** JSON with schema, row count, row groups, and file size

### 2. read_slice_tool

Read a horizontal slice of rows with optional column projection and advanced filtering.

**Parameters:**
- `file_path` (str): Path to the Parquet file
- `start_row` (int): Starting row index (inclusive, 0-based)
- `end_row` (int): Ending row index (exclusive)
- `columns` (list[str], optional): List of columns to include
- `filter_json` (str, optional): JSON filter specification

**16KB Context Protection:** If the slice exceeds 16KB, returns error with suggested safe parameters.

### 3. get_column_preview_tool

Preview values from a specific column with pagination support.

**Parameters:**
- `file_path` (str): Path to the Parquet file
- `column_name` (str): Name of the column to preview
- `start_index` (int, optional): Starting index for pagination (default: 0)
- `max_items` (int, optional): Maximum items to return (default: 100, max: 100)

### 4. aggregate_column_tool

Compute statistical aggregations on columns with optional filtering and row ranges.

**Parameters:**
- `file_path` (str): Path to the Parquet file
- `column_name` (str): Column to aggregate
- `operation` (str): One of: min, max, mean, sum, count, std, count_distinct
- `filter_json` (str, optional): JSON filter specification
- `start_row` (int, optional): Starting row for range constraint
- `end_row` (int, optional): Ending row for range constraint

## Filter Format

JSON-based filtering.

### Simple Filters

```json
{"column": "temperature", "op": "less", "value": 25.0}
{"column": "sensor_id", "op": "equal", "value": 42}
{"column": "status", "op": "in", "values": ["active", "pending"]}
{"column": "error_code", "op": "is_null"}
```

### Compound Filters

```json
{
  "and": [
    {"column": "temperature", "op": "greater", "value": 20.0},
    {"column": "temperature", "op": "less", "value": 30.0}
  ]
}
```

### Supported Operations

| Operation | Description |
|-----------|-------------|
| equal | Equals |
| not_equal | Not equals |
| less | Less than |
| less_equal | Less than or equal |
| greater | Greater than |
| greater_equal | Greater than or equal |
| in, is_in | Value in list |
| is_null | Column is NULL |
| is_not_null, is_valid | Column is not NULL |
| and | Logical AND |
| or | Logical OR |
| not | Logical NOT |

## Testing

192 tests.

```bash
# Run all tests
uv run pytest tests/ -v

# Quick smoke test (exclude slow tests)
uv run pytest tests/ -v -m "not slow"

# Test specific suite
uv run pytest tests/test_filtering.py -v
```

**Note on Test Datasets**: The repository includes trimmed datasets for basic testing. Tests requiring the full IceCube datasets are automatically skipped.

## Evaluation

The `evaluation.xml` file contains 10 validation questions that test advanced filtering and aggregation capabilities. To run the full evaluation and get expected outputs, download the complete IceCube Neutrino datasets:

- `batch_1.parquet` through `batch_6.parquet` (~160MB each)
- `train_meta.parquet` (~3.5GB)

**Dataset Source**: [IceCube Neutrino Path Least Squares - Kaggle](https://www.kaggle.com/code/solverworld/icecube-neutrino-path-least-squares-1-214/input)

Place these files in the `datasets/` directory to enable full evaluation testing.

## Architecture

```
parquet/                              # iowarp_mcp_servers/parquet/
├── src/parquet_mcp/
│   ├── server.py                     # FastMCP server with @mcp.tool decorators
│   └── capabilities/
│       └── parquet_handler.py        # Core implementations
├── tests/                            # 192 tests
├── datasets/                         # Test Parquet files (44KB trimmed)
├── pyproject.toml                    # Package configuration
└── README.md                         # This file
```

## Performance

Tested on IceCube Neutrino dataset (131M+ rows, 830MB):

| Operation | Time | Notes |
|-----------|------|-------|
| Summarize | <1s | Metadata only |
| Read slice (100 rows) | <1s | Direct offset |
| Filtered slice | 2-5s | Depends on selectivity |
| Aggregation (min/max) | <10s | Full scan |

## License

MIT License - see LICENSE for details

## Resources

- **IoWarp MCPs Website**: https://iowarp.github.io/iowarp-mcps/
- **Model Context Protocol**: https://modelcontextprotocol.io/
- **Apache Parquet**: https://parquet.apache.org/
- **PyArrow Documentation**: https://arrow.apache.org/docs/python/

## Support

- **Zulip Chat**: https://grc.zulipchat.com/join/bepp44mnzwjnvyewhzumxhnh/
- **GitHub Issues**: https://github.com/iowarp/iowarp-mcps/issues
- **Email**: grc@illinoistech.edu
