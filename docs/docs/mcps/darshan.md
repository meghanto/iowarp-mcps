---
title: Darshan MCP
description: "Darshan MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to analyze HPC application I/O performance through Darshan profiler trace files. This server provides advanced I/O analysis capabilities, performance bottleneck identification, and comp..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Darshan"
  icon="⚡"
  category="Utilities"
  description="Darshan MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to analyze HPC application I/O performance through Darshan profiler trace files. This server provides advanced I/O analysis capabilities, performance bottleneck identification, and comprehensive reporting tools with seamless integration with AI coding assistants."
  version="0.1.0"
  actions={["load_darshan_log", "get_job_summary", "analyze_file_access_patterns", "get_io_performance_metrics", "analyze_posix_operations", "analyze_mpiio_operations", "identify_io_bottlenecks", "get_timeline_analysis", "compare_darshan_logs", "generate_io_summary_report", "load_darshan_log", "get_job_summary", "analyze_file_access_patterns", "get_io_performance_metrics", "analyze_posix_operations", "analyze_mpiio_operations", "identify_io_bottlenecks", "get_timeline_analysis", "compare_darshan_logs", "generate_io_summary_report"]}
  platforms={["claude", "cursor", "vscode"]}
>

## Advanced Features


### Utility Functions
Essential utility functions for scientific computing:
- **Data Transformation**: Convert and process data efficiently
- **Automation**: Automate repetitive tasks
- **Integration**: Easy integration with other tools

### Performance Optimized
- **Fast Processing**: Optimized algorithms for speed
- **Memory Efficient**: Smart memory management
- **Scalable**: Handles large workloads efficiently


## Available Actions


#### `load_darshan_log`
Load and parse a Darshan log file to extract I/O performance metrics and metadata. Returns basic information about the trace file including job details, file access patterns, and available modules.

**Usage Example:**
```python
# Use load_darshan_log function
result = load_darshan_log()
print(result)
```


#### `get_job_summary`
Get comprehensive job-level summary from a loaded Darshan log including execution time, number of processes, total I/O volume, and performance metrics.

**Usage Example:**
```python
# Use get_job_summary function
result = get_job_summary()
print(result)
```


#### `analyze_file_access_patterns`
Analyze file access patterns from the trace including which files were accessed, access types (read/write), sequential vs random access patterns, and file size distributions.

**Usage Example:**
```python
# Use analyze_file_access_patterns function
result = analyze_file_access_patterns()
print(result)
```


#### `get_io_performance_metrics`
Extract detailed I/O performance metrics including bandwidth, IOPS, average request sizes, and timing information for read and write operations.

**Usage Example:**
```python
# Use get_io_performance_metrics function
result = get_io_performance_metrics()
print(result)
```


#### `analyze_posix_operations`
Analyze POSIX I/O operations from the trace including read/write system calls, file operations (open, close, seek), and their frequency and timing patterns.

**Usage Example:**
```python
# Use analyze_posix_operations function
result = analyze_posix_operations()
print(result)
```


#### Additional Actions
This MCP provides 15 additional actions. Refer to the MCP server documentation for complete details.


## Integration Examples


### Utility Operations
```python
# Use Darshan utilities
result = perform_operation("input_data")
optimized = optimize_result(result)

# Chain operations
processed = process_data(input_data)
final_result = finalize_processing(processed)
```

### Automation Workflow
```python
# Automate repetitive tasks
for item in input_list:
    processed = process_item(item)
    validate_result(processed)
    store_result(processed)
```


</MCPDetail>
