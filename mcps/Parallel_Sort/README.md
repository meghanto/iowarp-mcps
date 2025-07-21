# Parallel Sort MCP - High-Performance Parallel Sorting for LLMs
 
 
## Description
 
Parallel Sort MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to perform high-performance parallel sorting operations on large datasets. This server provides advanced sorting algorithms, performance optimization tools, and scalable data processing capabilities with seamless integration with AI coding assistants.
**Key Features:**
- **High-Performance Sorting**: Parallel merge sort, quick sort, and radix sort algorithms with multi-threading support
- **Scalable Data Processing**: Handle large datasets with memory-efficient algorithms and chunked processing
- **Multiple Data Formats**: Support for CSV, JSON, binary files, and in-memory data structures
- **Performance Analytics**: Execution time analysis, memory usage tracking, and algorithm comparison
- **Customizable Parameters**: Thread count, chunk size, and algorithm selection for optimal performance
- **MCP Integration**: Full Model Context Protocol compliance for seamless LLM integration
 
 
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
    "parallel-sort-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
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
    "parallel-sort-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
    }
  }
}
```
 
</details>
 
<details>
<summary><b>Install in Claude Code</b></summary>
 
Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.
 
```sh
claude mcp add parallel-sort-mcp -- uvx iowarp-mcps parallel-sort
```
 
</details>
 
<details>
<summary><b>Install in Claude Desktop</b></summary>
 
Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.
 
```json
{
  "mcpServers": {
    "parallel-sort-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Parallel_Sort run parallel-sort-mcp --help
```
 
**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Parallel_Sort run parallel-sort-mcp --help
```
 
**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Parallel_Sort run parallel-sort-mcp --help
```
 
</details>
 
## Available Actions

### `parallel_merge_sort`
**Description**: Perform parallel merge sort on large datasets with configurable thread count and memory optimization.

**Parameters**:
- `data_file` (str): Path to input data file (CSV, JSON, or binary)
- `output_file` (str): Path for sorted output file
- `num_threads` (int, optional): Number of parallel threads (default: CPU count)
- `chunk_size` (int, optional): Size of data chunks for processing (default: auto)

**Returns**: Dictionary with sorting results, execution time, and performance metrics.

### `parallel_quick_sort`
**Description**: Execute parallel quicksort algorithm with pivot optimization and load balancing.

**Parameters**:
- `data_file` (str): Path to input data file
- `output_file` (str): Path for sorted output file
- `pivot_strategy` (str, optional): Pivot selection strategy ('median', 'random', 'first')
- `num_threads` (int, optional): Number of parallel threads

**Returns**: Dictionary with sorting results and algorithm performance analysis.

### `radix_sort`
**Description**: Perform high-speed radix sort for integer and string data with parallel bucket processing.

**Parameters**:
- `data_file` (str): Path to input data file
- `output_file` (str): Path for sorted output file
- `data_type` (str): Data type ('int', 'string', 'float')
- `radix_base` (int, optional): Radix base for sorting (default: 10)

**Returns**: Dictionary with sorting results and radix-specific performance metrics.

### `compare_algorithms`
**Description**: Compare performance of different sorting algorithms on the same dataset.

**Parameters**:
- `data_file` (str): Path to input data file
- `algorithms` (list): List of algorithms to compare ['merge_sort', 'quick_sort', 'radix_sort']
- `num_threads` (int, optional): Number of threads for parallel algorithms

**Returns**: Dictionary with comparative performance analysis and recommendations.

### `sort_memory_analysis`
**Description**: Analyze memory usage patterns during sorting operations with profiling data.

**Parameters**:
- `data_file` (str): Path to input data file
- `algorithm` (str): Sorting algorithm to analyze
- `profile_detail` (str, optional): Profiling detail level ('basic', 'detailed')

**Returns**: Dictionary with memory usage statistics and optimization recommendations.

### `benchmark_performance`
**Description**: Run comprehensive performance benchmarks across multiple data sizes and types.

**Parameters**:
- `data_sizes` (list): List of data sizes to benchmark
- `data_types` (list): List of data types to test
- `algorithms` (list): Algorithms to benchmark

**Returns**: Dictionary with comprehensive benchmark results and scaling analysis.

## Examples
 
### 1. Large Dataset Parallel Sorting
```
I have a large CSV file at /data/customer_records.csv with 10 million records. Sort this data efficiently using parallel merge sort and analyze the performance.
```

**Tools called:**
- `parallel_merge_sort` - Sort the large dataset using parallel algorithms
- `sort_memory_analysis` - Analyze memory usage during sorting

This prompt will:
- Use `parallel_merge_sort` to efficiently sort the large dataset with optimal thread usage
- Analyze memory consumption using `sort_memory_analysis`
- Provide performance metrics and optimization recommendations
- Generate sorted output with execution statistics

### 2. Algorithm Performance Comparison
```
Compare the performance of parallel merge sort, quick sort, and radix sort on my dataset /data/numerical_data.csv to determine the best algorithm for my use case.
```

**Tools called:**
- `compare_algorithms` - Compare sorting algorithm performance
- `benchmark_performance` - Run comprehensive benchmarks

This prompt will:
- Execute multiple sorting algorithms using `compare_algorithms`
- Generate comprehensive benchmarks using `benchmark_performance`
- Provide detailed performance analysis and recommendations
- Compare execution times, memory usage, and scalability

### 3. High-Performance Integer Sorting
```
Sort the integer data in /data/sensor_readings.csv using radix sort for optimal performance, and analyze the memory efficiency.
```

**Tools called:**
- `radix_sort` - Perform high-speed radix sort on integer data
- `sort_memory_analysis` - Analyze memory usage patterns

This prompt will:
- Use `radix_sort` to efficiently sort integer data with parallel bucket processing
- Analyze memory efficiency using `sort_memory_analysis`
- Provide radix-specific performance metrics
- Generate optimized sorted output

### 4. Multi-Threaded Quicksort Optimization
```
Sort /data/mixed_dataset.json using parallel quicksort with median pivot strategy and 8 threads, then analyze the load balancing efficiency.
```

**Tools called:**
- `parallel_quick_sort` - Execute parallel quicksort with optimization
- `benchmark_performance` - Analyze thread utilization and performance

This prompt will:
- Execute parallel quicksort using `parallel_quick_sort` with median pivot strategy
- Analyze thread utilization using `benchmark_performance`
- Provide load balancing efficiency metrics
- Generate performance optimization recommendations

### 5. Comprehensive Sorting Benchmark Suite
```
Run a complete performance analysis on /data/test_dataset.csv testing all available algorithms across different thread counts and data sizes.
```

**Tools called:**
- `benchmark_performance` - Run comprehensive sorting benchmarks
- `compare_algorithms` - Compare all available algorithms
- `sort_memory_analysis` - Analyze memory usage across algorithms

This prompt will:
- Execute comprehensive benchmarks using `benchmark_performance`
- Compare all algorithms using `compare_algorithms`
- Analyze memory patterns using `sort_memory_analysis`
- Generate detailed performance reports with scaling analysis

### 6. Memory-Optimized Large File Sorting
```
Sort the large file /data/big_data.csv (50GB) using memory-efficient chunked processing and provide detailed memory usage analysis.
```

**Tools called:**
- `parallel_merge_sort` - Sort with chunked processing
- `sort_memory_analysis` - Monitor memory usage during operation

This prompt will:
- Use `parallel_merge_sort` with optimized chunk sizes for large files
- Monitor memory usage using `sort_memory_analysis`
- Provide memory optimization strategies
- Generate efficient sorted output with minimal memory footprint
 